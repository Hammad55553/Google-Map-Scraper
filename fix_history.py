import re

with open("frontend/api/email_sender.py", "r") as f:
    email_content = f.read()

# Add ContactHistory to email_sender imports
if "ContactHistory" not in email_content:
    email_content = email_content.replace("from database import Lead", "from database import Lead, ContactHistory")
    email_content = email_content.replace("import datetime", "import datetime\nfrom sqlalchemy.exc import IntegrityError")

# Update loop to filter duplicates
old_filter = """        for lead in leads_with_email:
            if lead.status == "Contacted":
                continue
            if lead.email.lower() not in unique_emails:"""
new_filter = """        for lead in leads_with_email:
            if lead.status in ["Contacted", "Duplicate"]:
                continue
            if lead.email.lower() not in unique_emails:"""
email_content = email_content.replace(old_filter, new_filter)

# Insert into ContactHistory
old_success = """                # Update database status permanently
                lead.status = "Contacted"
                db.commit()"""

new_success = """                # Update database status permanently
                lead.status = "Contacted"
                try:
                    history = ContactHistory(email=lead.email.lower(), contacted_at=str(datetime.datetime.now()))
                    db.add(history)
                    db.commit()
                except IntegrityError:
                    db.rollback() # Email already in history
                except Exception:
                    db.rollback()"""
email_content = email_content.replace(old_success, new_success)

with open("frontend/api/email_sender.py", "w") as f:
    f.write(email_content)

# Update index.py to use ContactHistory
with open("frontend/api/index.py", "r") as f:
    index_content = f.read()

if "ContactHistory" not in index_content:
    index_content = index_content.replace("from database import SessionLocal, Lead", "from database import SessionLocal, Lead, ContactHistory")

# Modify Scraper (run_scraper function)
old_handle_lead = """        def handle_lead(item):
            # Score Lead (Lead Potential Score)"""
new_handle_lead = """        def handle_lead(item):
            # Score Lead (Lead Potential Score)"""
# Wait, I'll just use a more direct replacement for the scraper to load history once
old_scraper_start = """        db = SessionLocal()
        # Delete old leads for fresh search
        db.query(Lead).delete()
        db.commit()

        def handle_lead(item):"""
new_scraper_start = """        db = SessionLocal()
        
        # Load all previously contacted emails into memory
        contacted_emails = {h.email.lower() for h in db.query(ContactHistory.email).all()}
        
        # Delete old leads for fresh search
        db.query(Lead).delete()
        db.commit()

        def handle_lead(item):"""
index_content = index_content.replace(old_scraper_start, new_scraper_start)

# In run_scraper handle_lead
old_lead_status = 'status="New"'
new_lead_status = 'status="Duplicate" if item.get("Email") and item["Email"].lower() in contacted_emails else "New"'
index_content = index_content.replace(old_lead_status, new_lead_status, 1)

# Modify Import (import_leads_csv function)
old_import_start = """        # Clear existing leads
        db.query(Lead).delete()
        
        for _, row in df.iterrows():"""
new_import_start = """        # Load history
        contacted_emails = {h.email.lower() for h in db.query(ContactHistory.email).all()}
        
        # Clear existing leads
        db.query(Lead).delete()
        
        for _, row in df.iterrows():"""
index_content = index_content.replace(old_import_start, new_import_start)

old_import_status = 'status=get_val("Status"),'
new_import_status = 'status="Duplicate" if get_val("Email").lower() in contacted_emails else get_val("Status"),'
index_content = index_content.replace(old_import_status, new_import_status)

with open("frontend/api/index.py", "w") as f:
    f.write(index_content)

