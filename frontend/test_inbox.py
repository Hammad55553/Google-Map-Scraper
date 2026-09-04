import imaplib, email
from email.header import decode_header
import os

gmail_address = os.environ.get("NEXT_PUBLIC_JOBS_GMAIL", "hammadaslam78612@gmail.com")
app_password = os.environ.get("NEXT_PUBLIC_JOBS_PASSWORD", "tqmb xojp sjux yjjm")

try:
    mail = imaplib.IMAP4_SSL("imap.gmail.com")
    mail.login(gmail_address, app_password)
    mail.select("inbox")
    status, messages = mail.search(None, "ALL")
    email_ids = messages[0].split()[-3:]
    for i in email_ids:
        res, msg_data = mail.fetch(i, "(RFC822)")
        for response_part in msg_data:
            if isinstance(response_part, tuple):
                msg = email.message_from_bytes(response_part[1])
                print("Raw From:", msg.get("From"))
                print("Raw Subject:", msg.get("Subject"))
except Exception as e:
    print(e)
