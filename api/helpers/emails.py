import imaplib
import email
from email.header import decode_header
from .encrypter import encrypt_to_base64
# IMAP server settings for Gmail
IMAP_SERVER = 'imap.gmail.com'
IMAP_PORT = 993

# Your Gmail credentials (replace with your actual Gmail address and app password)
GMAIL_USERNAME = 'christinchristma6@gmail.com'
GMAIL_PASSWORD = 'ncbvfpxdfnxjsxmv'

def fetch_emails():
    # Connect to Gmail's IMAP server using SSL
    mail = imaplib.IMAP4_SSL(IMAP_SERVER, IMAP_PORT)
    
    try:
        # Login to Gmail
        mail.login(GMAIL_USERNAME, GMAIL_PASSWORD)

        # Select the inbox
        mail.select('inbox')

        # Search for latest emails (10 most recent)
        status, response = mail.search(None, 'ALL')
        if status == 'OK':
            email_list = []
            email_ids = response[0].split()
            for i in reversed(email_ids[-10:]):  # Fetch the 10 most recent emails
                status, msg = mail.fetch(i, '(RFC822)')
                if status == 'OK':
                    for response_part in msg:
                        if isinstance(response_part, tuple):
                            # Parse email content
                            email_msg = email.message_from_bytes(response_part[1])
                            subject = decode_header(email_msg['Subject'])[0][0]
                            if isinstance(subject, bytes):
                                subject = subject.decode()
                            sender = email_msg.get('From')
                            message = ""

                            # Process email parts
                            for part in email_msg.walk():
                                content_type = part.get_content_type()
                                content_disposition = str(part.get("Content-Disposition"))

                                if "attachment" not in content_disposition:
                                    # Extract email body
                                    body = part.get_payload(decode=True)
                                    if body:
                                        try:
                                            # Decode the payload if it's bytes
                                            message += body.decode()
                                        except UnicodeDecodeError:
                                            # Handle decoding errors as needed
                                            message += str(body)

                            email_list.append({
                                "subject": subject,
                                "from": sender,
                                "message": encrypt_to_base64(message)
                            })
            return email_list

    except imaplib.IMAP4.error as e:
        print(f'Error: {e}')
        return []
    
    finally:
        # Logout from Gmail
        mail.logout()











if __name__ == '__main__':
    fetched_emails = fetch_emails()
    for email_data in fetched_emails:
        print(f"Subject: {email_data['subject']}")
        print(f"From: {email_data['from']}")
        print(f"Message: {email_data['message']}")
        print('---')
