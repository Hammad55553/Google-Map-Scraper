with open("frontend/api/email_sender.py", "r") as f:
    content = f.read()

old_loop = """        success_count = 0
        for idx, lead in enumerate(leads_with_email):
            update_status_callback(f"Sending email {idx + 1}/{total} to {lead.business_name}...", idx + 1, total, None)"""

new_loop = """        success_count = 0
        
        # Deduplicate and filter out already contacted leads
        unique_emails = set()
        filtered_leads = []
        for lead in leads_with_email:
            if lead.status == "Contacted":
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
            update_status_callback(f"Sending email {idx + 1}/{total} to {lead.business_name}...", idx + 1, total, None)"""

content = content.replace(old_loop, new_loop)

old_success = """                server.send_message(msg)
                success_count += 1
                
                # Update status with lead_id so UI can show the tick mark!
                update_status_callback(f"Sent successfully to {lead.business_name}", idx + 1, total, lead.id)"""

new_success = """                server.send_message(msg)
                success_count += 1
                
                # Update database status permanently
                lead.status = "Contacted"
                db.commit()
                
                # Update status with lead_id so UI can show the tick mark!
                update_status_callback(f"Sent successfully to {lead.business_name}", idx + 1, total, lead.id)"""
                
content = content.replace(old_success, new_success)

with open("frontend/api/email_sender.py", "w") as f:
    f.write(content)

