import imaplib
import email
from email.header import decode_header
email_user = input("Enter your email address: ")
email_pass = input("Enter your email password: ")

imap_url = "imap-mail.outlook.com"
mail = imaplib.IMAP4_SSL(imap_url)
try:
    mail.login(email_user, email_pass)
    print("Login successful!")
except imaplib.IMAP4.error:
    print("Login failed. Please check your credentials.")
    exit()

mail.select("Inbox")
result, data = mail.search(None, "ALL")

mail_ids = data[0].split()
latest_email_id = mail_ids[::]

for i in latest_email_id:
    result, message_data = mail.fetch(i, "(RFC822)")
    if result != "OK":
        print(f"Could not fetch email {i}")
        continue
    # Retrieve and parse email content
    msg = email.message_from_bytes(message_data[0][1])
    # Subject
    subject, encoding = decode_header(msg["Subject"])[0]
    if isinstance(encoding, bytes):
        subject = subject.decode(encoding or "utf-8", errors="ignore")
    # Body
    if msg.is_multipart():
        for part in msg.walk():
            if part.get_content_type() == "text/plain":
                charset = part.get_content_charset()
                body = part.get_payload(decode=True).decode(charset or "utf-8", errors="ignore")
                break
    else:
        charset = msg.get_content_charset()
        body = msg.get_payload(decode=True).decode(charset or "utf-8", errors="ignore")
    print(f'-----New Email-----\nSubject: {subject}\nBody: {body}\n')
