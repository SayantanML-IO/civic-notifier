import smtplib
import os  # To access Environment Variables
from email.mime.text import MIMEText

def send_email_alert(subject, body, config):
    if not config['notifications']['send_email']:
        return

    # SECURITY UPDATE: Fetch ALL sensitive info from Environment Variables
    sender_email = os.getenv('SENDER_EMAIL')
    receiver_email = os.getenv('RECEIVER_EMAIL')
    password = os.getenv('EMAIL_PASSWORD')
    
    # Check if any credentials are missing
    if not sender_email or not receiver_email or not password:
        print("Error: Missing Email Credentials! Make sure SENDER_EMAIL, RECEIVER_EMAIL, and EMAIL_PASSWORD are set in your .env file.")
        return

    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = sender_email
    msg['To'] = receiver_email

    try:
        with smtplib.SMTP(config['notifications']['smtp_server'], config['notifications']['smtp_port']) as server:
            server.starttls()
            server.login(sender_email, password)
            server.send_message(msg)
            print("Notification email sent successfully!")
    except Exception as e:
        print(f"Failed to send email. Error: {e}")