import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import asyncio
import datetime
from sqlalchemy.exc import IntegrityError
from email_template import get_email_template
from database import SessionLocal, ContactHistory

async def send_bulk_emails(sender_email: str, app_password: str, leads: list, update_status_callback):
    """
    Sends emails to a list of leads using Gmail SMTP.
    """
    if not leads:
        update_status_callback("No leads with valid emails found.")
        return

    # Filter leads that have emails
    leads_with_email = [lead for lead in leads if lead.email and lead.email.strip()]
    total = len(leads_with_email)
    
    if total == 0:
        update_status_callback("No emails to send.", 0, 0, None)
        return

    update_status_callback(f"Connecting to Gmail SMTP server...", 0, total, None)
    
    try:
        # Setup SMTP connection
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, app_password)
        
        success_count = 0
        
        # Deduplicate and filter out already contacted leads
        unique_emails = set()
        filtered_leads = []
        for lead in leads_with_email:
            if lead.status in ["Contacted", "Duplicate"]:
                continue
            if lead.email.lower() not in unique_emails:
                unique_emails.add(lead.email.lower())
                filtered_leads.append(lead)
                
        leads_with_email = filtered_leads
        total = len(leads_with_email)
        
        if total == 0:
            server.quit()
            update_status_callback("No new/unique emails to send.", 0, 0, None)
            return

        for idx, lead in enumerate(leads_with_email):
            update_status_callback(f"Sending email {idx + 1}/{total} to {lead.business_name}...", idx + 1, total, None)
            
            try:
                msg = MIMEMultipart()
                msg['From'] = sender_email
                msg['To'] = lead.email
                msg['Subject'] = f"Quick question for {lead.business_name}"
                
                # Convert WhatsApp Markdown (*bold*) to HTML (<b>bold</b>)
                import re
                html_body = lead.recommended_pitch
                # Replace *text* with <b>text</b>
                html_body = re.sub(r'\*(.*?)\*', r'<b>\1</b>', html_body)
                # Convert newlines to <br> for HTML email
                html_body = html_body.replace('\n', '<br>')
                
                # Wrap in basic HTML structure with modern font
                final_html = get_email_template(html_body)
                
                msg.attach(MIMEText(final_html, 'html'))
                
                server.send_message(msg)
                success_count += 1
                
                # Update database status permanently
                lead.status = "Contacted"
                try:
                    db = SessionLocal()
                    history = ContactHistory(email=lead.email.lower(), contacted_at=str(datetime.datetime.now()))
                    db.add(history)
                    db.commit()
                    db.close()
                except IntegrityError:
                    db.rollback()
                    db.close()
                except Exception:
                    pass
                
                # Update status with lead_id so UI can show the tick mark!
                update_status_callback(f"Sent successfully to {lead.business_name}", idx + 1, total, lead.id)
                
                # Small delay to avoid Gmail rate limits
                await asyncio.sleep(2)
                
            except Exception as e:
                print(f"Failed to send email to {lead.email}: {e}")
                
        server.quit()
        update_status_callback(f"Campaign complete! Successfully sent {success_count} emails.", total, total, None)
        
    except Exception as e:
        print(f"SMTP Connection Error: {e}")
        update_status_callback(f"Error connecting to Gmail: {str(e)}. Check your App Password.", 0, 0, None)
