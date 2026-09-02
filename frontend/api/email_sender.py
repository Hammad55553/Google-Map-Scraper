import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import asyncio

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
        update_status_callback("No emails to send.")
        return

    update_status_callback(f"Connecting to Gmail SMTP server...")
    
    try:
        # Setup SMTP connection
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, app_password)
        
        success_count = 0
        for idx, lead in enumerate(leads_with_email):
            update_status_callback(f"Sending email {idx + 1}/{total} to {lead.business_name}...")
            
            try:
                msg = MIMEMultipart()
                msg['From'] = sender_email
                msg['To'] = lead.email
                msg['Subject'] = f"Quick question for {lead.business_name}"
                
                # We use the recommended pitch as the email body
                body = lead.recommended_pitch
                msg.attach(MIMEText(body, 'plain'))
                
                server.send_message(msg)
                success_count += 1
                
                # Small delay to avoid Gmail rate limits
                await asyncio.sleep(2)
                
            except Exception as e:
                print(f"Failed to send email to {lead.email}: {e}")
                
        server.quit()
        update_status_callback(f"Campaign complete! Successfully sent {success_count} emails.")
        
    except Exception as e:
        print(f"SMTP Connection Error: {e}")
        update_status_callback(f"Error connecting to Gmail: {str(e)}. Check your App Password.")
