from fastapi import FastAPI, BackgroundTasks, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from pydantic import BaseModel
from database import SessionLocal, Lead
import asyncio
import uuid
import random
from datetime import datetime
from scraper import run_scraper
from pitch_generator import generate_bilingual_pitch

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

def update_progress(current, total):
    scrape_status["progress"] = current
    scrape_status["total"] = total
    scrape_status["message"] = f"Loaded {current}/{total} items..."

def real_scraper_task(req: ScrapeRequest):
    global scrape_status
    scrape_status["status"] = "scraping"
    scrape_status["progress"] = 0
    scrape_status["message"] = "Initializing scraper..."
    
    search_query = f"{req.category} in {req.city}, {req.country}"
    
    def update_progress(msg, prog):
        scrape_status["message"] = msg
        scrape_status["progress"] = prog

    try:
        db = SessionLocal()
        # Clear old leads at the start of the search
        db.query(Lead).delete()
        db.commit()

        def handle_lead(item):
            # Filter: Only keep businesses that DO NOT have a website
            if item.get("Has Website"):
                return
                
            # Score Lead (Data Completeness Score)
            score = 0
            if item["Phone"]: score += 20
            if item["WhatsApp Link"]: score += 20
            if item["Rating"] > 0: score += 20
                
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
                status="New"
            )
            db.add(new_lead)
            db.commit()

        # Scrape and stream
        run_scraper(search_query, limit=5000, progress_callback=update_progress, on_lead_found=handle_lead)
        
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
from index import app
from fastapi.responses import StreamingResponse
from database import SessionLocal, Lead
from excel_export import generate_excel_from_leads
import datetime

@app.get("/api/export")
def export_leads():
    db = SessionLocal()
    leads = db.query(Lead).all()
    db.close()
    
    excel_file = generate_excel_from_leads(leads)
    
    date_str = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"Leads_{date_str}.xlsx"
    
    return StreamingResponse(
        excel_file,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )
