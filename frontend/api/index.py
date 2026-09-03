from fastapi import FastAPI, BackgroundTasks, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from fastapi import UploadFile, File
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from pydantic import BaseModel
from database import SessionLocal, Lead, ContactHistory
import asyncio
import uuid
import random
import datetime
import io
import pandas as pd
from scraper import run_scraper
from pitch_generator import generate_bilingual_pitch
from excel_export import generate_excel_from_leads

app = FastAPI()

from calling import router as calling_router
app.include_router(calling_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class ScrapeRequest(BaseModel):
    country: str
    state: str
    city: str
    category: str
    radius: str

class PitchUpdateRequest(BaseModel):
    pitch: str

# Global state for tracking scraping progress
scrape_status = {
    "status": "idle",
    "progress": 0,
    "total": 50, # New limit of 50
    "message": ""
}

def update_progress(current, total, message=""):
    scrape_status["progress"] = current
    scrape_status["total"] = total
    scrape_status["message"] = message or f"Loaded {current}/{total} items..."

def real_scraper_task(req: ScrapeRequest):
    global scrape_status
    scrape_status["status"] = "scraping"
    scrape_status["progress"] = 0
    scrape_status["message"] = "Initializing scraper..."
    
    search_query = f"{req.category} in {req.city}, {req.state}, {req.country}"
    
    def update_progress(current, total, message=""):
        scrape_status["progress"] = int((current / total) * 100) if total > 0 else 0
        scrape_status["message"] = message or f"Processing item {current} of {total}"

    try:
        db = SessionLocal()
        # Clear old leads at the start of the search
        db.query(Lead).delete()
        db.commit()
        
        # Load all previously contacted emails for fast duplicate checking
        contacted_emails = {h.email.lower() for h in db.query(ContactHistory.email).all()}

        def handle_lead(item):
            # Score Lead (Lead Potential Score)
            # We give high priority (preference) to leads WITHOUT a website
            score = 0
            if not item.get("Has Website"): 
                score += 50  # Huge boost for not having a website
            
            if item["Phone"]: score += 20
            if item["WhatsApp Link"]: score += 20
            if item["Rating"] > 0: score += 10
                
            grade = "A+" if score >= 80 else ("B" if score >= 60 else ("C" if score >= 40 else "D"))
            
            pitch = generate_bilingual_pitch(item['Name'], req.country)
            
            new_lead = Lead(
                place_id=str(uuid.uuid4()),
                business_name=item["Name"],
                category=req.category,
                city=req.city,
                rating=item["Rating"],
                reviews_count=0,
                phone=item["Phone"],
                whatsapp_link=item["WhatsApp Link"],
                has_website=item["Has Website"],
                website=item.get("Website URL", ""),
                email=item.get("Email", ""),
                address=item.get("Address", ""),
                map_url=item.get("Map URL", ""),
                booking_detected=False,
                lead_score=score,
                lead_grade=grade,
                recommended_pitch=pitch,
                status="Duplicate" if item.get("Email") and item["Email"].lower() in contacted_emails else "New"
            )
            db.add(new_lead)
            db.commit()

        # Scrape and stream
        cancel_fn = lambda: scrape_status.get("cancel", False)
        run_scraper(search_query, limit=500, progress_callback=update_progress, on_lead_found=handle_lead, cancel_check=cancel_fn)
        
        db.close()
        scrape_status["status"] = "idle"
        scrape_status["progress"] = 100
        scrape_status["message"] = "Scraping complete!"
    except Exception as e:
        print(f"Scraper error: {e}")
        scrape_status["status"] = "error"
        scrape_status["message"] = f"Error: {str(e)}"

@app.post("/api/scrape")
def start_scraping(req: ScrapeRequest, background_tasks: BackgroundTasks):
    background_tasks.add_task(real_scraper_task, req)
    return {"message": "Scraping started in background"}

@app.get("/api/scrape/status")
def get_scrape_status():
    return scrape_status

# Global state for tracking email campaign progress
email_campaign_status = {
    "status": "idle",
    "message": "",
    "progress": 0,
    "sent_ids": []
}

class EmailCampaignRequest(BaseModel):
    gmail_address: str
    app_password: str

def run_email_campaign_task(req: EmailCampaignRequest):
    global email_campaign_status
    email_campaign_status["status"] = "running"
    email_campaign_status["message"] = "Initializing campaign..."
    email_campaign_status["progress"] = 0
    email_campaign_status["sent_ids"] = []
    
    def update_status(msg, current=0, total=0, sent_lead_id=None):
        email_campaign_status["message"] = msg
        if total > 0:
            email_campaign_status["progress"] = int((current / total) * 100)
        if sent_lead_id is not None:
            email_campaign_status["sent_ids"].append(sent_lead_id)
        print(f"Email Campaign: {msg}")
        
    db = SessionLocal()
    leads = db.query(Lead).all()
    db.close()
    
    # We must import email_sender dynamically or locally to avoid circular imports if any, but since it's just a file, we'll do it safely
    from email_sender import send_bulk_emails
    asyncio.run(send_bulk_emails(req.gmail_address, req.app_password, leads, update_status))
    
    email_campaign_status["status"] = "idle"

@app.post("/api/emails/campaign")
def start_email_campaign(req: EmailCampaignRequest, background_tasks: BackgroundTasks):
    if email_campaign_status["status"] == "running":
        return {"error": "A campaign is already running"}
    background_tasks.add_task(run_email_campaign_task, req)
    return {"message": "Email campaign started"}

@app.get("/api/emails/status")
def get_email_status():
    return email_campaign_status

@app.get("/api/leads")
def get_leads(db: Session = Depends(get_db)):
    leads = db.query(Lead).order_by(Lead.lead_score.desc()).all()
    return leads

@app.put("/api/leads/{lead_id}/pitch")
def update_lead_pitch(lead_id: int, req: PitchUpdateRequest, db: Session = Depends(get_db)):
    lead = db.query(Lead).filter(Lead.id == lead_id).first()
    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found")
    lead.recommended_pitch = req.pitch
    db.commit()
    return {"message": "Pitch updated successfully"}

@app.delete("/api/leads")
def clear_leads(db: Session = Depends(get_db)):
    db.query(Lead).delete()
    db.commit()
    return {"message": "All leads cleared"}

@app.post("/api/scrape/stop")
def stop_scraping():
    scrape_status["cancel"] = True
    return {"message": "Stop signal sent"}

@app.get("/api/export")
def export_leads():
    db = SessionLocal()
    leads = db.query(Lead).all()
    db.close()
    
    excel_file = generate_excel_from_leads(leads)
    date_str = datetime.datetime.now().strftime("%Y%m%d_%H%M")
    
    if leads and leads[0].category and leads[0].city:
        cat_clean = leads[0].category.replace(' ', '_').replace('/', '')
        city_clean = leads[0].city.replace(' ', '_').replace('/', '')
        filename = f"{cat_clean}_{city_clean}_{date_str}.xlsx"
    else:
        filename = f"Leads_{date_str}.xlsx"
    
    return StreamingResponse(
        excel_file,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )

@app.post("/api/import")
async def import_leads_csv(file: UploadFile = File(...), db: Session = Depends(get_db)):
    try:
        contents = await file.read()
        if file.filename.endswith('.csv'):
            df = pd.read_csv(io.BytesIO(contents))
        else:
            df = pd.read_excel(io.BytesIO(contents), engine='openpyxl')
            
        contacted_emails = {h.email.lower() for h in db.query(ContactHistory.email).all()}
        db.query(Lead).delete()
        
        for _, row in df.iterrows():
            def get_val(col_name, default=""):
                val = row.get(col_name)
                if pd.isna(val): return default
                return str(val).strip()

            phone_val = get_val("Phone")
            if phone_val.startswith("'"):
                phone_val = phone_val[1:]
                
            try:
                rating_val = float(get_val("Rating", 0))
            except:
                rating_val = 0.0
            try:
                reviews_val = int(float(get_val("Reviews Count", 0)))
            except:
                reviews_val = 0
            try:
                score_val = int(float(get_val("Lead Score", 0)))
            except:
                score_val = 0
                
            lead = Lead(
                place_id=str(uuid.uuid4()),
                business_name=get_val("Business Name"),
                category=get_val("Category"),
                city=get_val("City"),
                rating=rating_val,
                reviews_count=reviews_val,
                phone=phone_val,
                whatsapp_link=get_val("WhatsApp Link"),
                has_website=get_val("Website") not in ["", "False", "false", "0"],
                website=get_val("Website"),
                email=get_val("Email"),
                address=get_val("Address"),
                map_url=get_val("Map URL"),
                lead_score=score_val,
                lead_grade=get_val("Lead Grade"),
                status="Duplicate" if get_val("Email") and get_val("Email").lower() in contacted_emails else get_val("Status") or "New",
                recommended_pitch=get_val("Recommended Pitch")
            )
            db.add(lead)
            
        db.commit()
        return {"message": f"Successfully imported {len(df)} leads"}
        
    except Exception as e:
        return {"error": str(e)}


# ==================================================================
# JOB HUNT TAB — Search tech companies & send job applications
# ==================================================================
from job_scraper import run_job_scraper
from job_pitch_generator import generate_job_pitch
from resume_generator import generate_resume_pdf

job_status = {
    "status": "idle",
    "progress": 0,
    "total": 0,
    "message": "",
    "cancel": False
}

job_companies = []  # In-memory store for job hunt results

class JobSearchRequest(BaseModel):
    query: str  # e.g. "React Native software company" or "software company London"
    limit: int = 30

class JobApplyRequest(BaseModel):
    gmail_address: str = "hammadaslam78612@gmail.com"
    app_password: str = "tqmb xojp sjux yjjm"
    custom_pitch: str = ""

def job_scraper_task(req: JobSearchRequest):
    global job_status, job_companies
    job_status["status"] = "scraping"
    job_status["progress"] = 0
    job_status["cancel"] = False
    job_status["message"] = "Starting job search..."
    job_companies.clear()

    def on_progress(current, total, msg=""):
        job_status["progress"] = int((current / total) * 100) if total > 0 else 0
        job_status["total"] = total
        job_status["message"] = msg or f"Processing {current}/{total}..."

    def on_company(item):
        job_companies.append(item)

    try:
        cancel_fn = lambda: job_status.get("cancel", False)
        run_job_scraper(
            query=req.query,
            limit=req.limit,
            progress_callback=on_progress,
            on_company_found=on_company,
            cancel_check=cancel_fn
        )
        job_status["status"] = "idle"
        job_status["progress"] = 100
        job_status["message"] = f"Done! Found {len(job_companies)} companies."
    except Exception as e:
        job_status["status"] = "error"
        job_status["message"] = f"Error: {str(e)}"

@app.post("/api/jobs/scrape")
def start_job_scrape(req: JobSearchRequest, background_tasks: BackgroundTasks):
    background_tasks.add_task(job_scraper_task, req)
    return {"message": "Job search started"}

@app.get("/api/jobs/status")
def get_job_status():
    return job_status

@app.get("/api/jobs/pitch/preview")
def preview_job_pitch():
    # Return a sample pitch with [Company Name]
    sample = generate_job_pitch("[Company Name]")
    return {"pitch": sample}

@app.get("/api/jobs/resume/download")
def download_resume():
    from fastapi.responses import Response
    pdf_bytes = generate_resume_pdf()
    return Response(content=pdf_bytes, media_type="application/pdf", headers={"Content-Disposition": "inline; filename=Hammad_Aslam_CV.pdf"})

@app.get("/api/jobs/companies")
def get_job_companies():
    return job_companies

@app.post("/api/jobs/stop")
def stop_job_scrape():
    job_status["cancel"] = True
    return {"message": "Stop signal sent"}

job_apply_status = {
    "status": "idle",
    "message": "",
    "progress": 0,
    "sent": []
}

def send_job_applications_task(req: JobApplyRequest):
    global job_apply_status
    import smtplib
    from email.mime.text import MIMEText
    from email.mime.multipart import MIMEMultipart
    from email.mime.base import MIMEBase
    from email import encoders

    job_apply_status["status"] = "running"
    job_apply_status["sent"] = []
    job_apply_status["progress"] = 0

    targets = [c for c in job_companies if c.get("email")]
    total = len(targets)
    if total == 0:
        job_apply_status["status"] = "idle"
        job_apply_status["message"] = "No companies with emails found."
        return

    try:
        resume_pdf = generate_resume_pdf()
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(req.gmail_address, req.app_password)

        for idx, company in enumerate(targets):
            try:
                job_apply_status["message"] = f"Sending to {company['name']} ({idx+1}/{total})..."
                job_apply_status["progress"] = int(((idx + 1) / total) * 100)

                # Use custom pitch if provided, otherwise generate one
                pitch = req.custom_pitch.replace("[Company Name]", company["name"]) if req.custom_pitch else generate_job_pitch(company["name"])

                import re
                html_body = re.sub(r'\*(.*?)\*', r'<b>\1</b>', pitch)
                html_body = html_body.replace('\n', '<br>')

                msg = MIMEMultipart()
                msg["From"] = req.gmail_address
                msg["To"] = company["email"]
                msg["Subject"] = f"React Native / Full-Stack Developer — Open to Remote Opportunities"

                msg.attach(MIMEText(f"""
                <html><body style="font-family:Arial,sans-serif;line-height:1.7;color:#333;max-width:640px">
                {html_body}
                </body></html>
                """, "html"))

                # Attach resume PDF
                part = MIMEBase("application", "octet-stream")
                part.set_payload(resume_pdf)
                encoders.encode_base64(part)
                part.add_header("Content-Disposition", 'attachment; filename="Hammad_Aslam_CV.pdf"')
                msg.attach(part)

                server.send_message(msg)
                job_apply_status["sent"].append(company["email"])

                import time; time.sleep(2)  # avoid Gmail rate limit

            except Exception as e:
                print(f"Failed to send to {company.get('email')}: {e}")

        server.quit()
        job_apply_status["status"] = "idle"
        job_apply_status["message"] = f"Done! Sent {len(job_apply_status['sent'])}/{total} applications."
    except Exception as e:
        job_apply_status["status"] = "error"
        job_apply_status["message"] = f"SMTP Error: {str(e)}"

@app.post("/api/jobs/apply")
def send_job_applications(req: JobApplyRequest, background_tasks: BackgroundTasks):
    if job_apply_status["status"] == "running":
        return {"error": "Applications already being sent"}
    background_tasks.add_task(send_job_applications_task, req)
    return {"message": "Sending applications..."}

@app.get("/api/jobs/apply/status")
def get_job_apply_status():
    return job_apply_status

