import os
import time
import requests
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
from dotenv import load_dotenv
import requests
load_dotenv(os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env'))
LOG_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'outputs', 'logs', 'sms_delivery.log')
def log_action(message):
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    with open(LOG_FILE, 'a', encoding='utf-8') as f:
        f.write(f"[{timestamp}] {message}\n")
    print(message)
def send_department_email(district_name, stats, target_email, risk_prob):
    """Sends a formal SMTP email to the health department."""
    sender_email = os.getenv("SENDER_EMAIL")
    sender_password = os.getenv("SENDER_PASSWORD")
    if not sender_email or not sender_password:
        log_action("EMAIL SKIPPED: Missing SMTP credentials in .env file.")
        return False

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = target_email
    msg['Subject'] = f"URGENT: High Dropout Risk Detected in {district_name}"

    body = f"""
    District Health Official,

    Our AI systems have flagged {district_name} for a HIGH Infant Mortality Risk (Probability: {risk_prob*100:.1f}%).
    
    Current Infrastructure Stats:
    - Population: {stats['POPULATION']}
    - BCG Starts: {stats['BCG']}
    - ASHA Sessions: {stats['IS_ASHA']}
    - Dropout Gap: {stats['dropout_gap_percent']:.2f}%

    ACTION REQUIRED: Please reallocate ASHA workers and review cold-chain logistics in this sector immediately.
    """
    msg.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, sender_password)
        server.send_message(msg)
        server.quit()
        log_action(f"EMAIL SUCCESS: Alert sent to {target_email}")
        return True
    except Exception as e:
        log_action(f"EMAIL FAILED: {str(e)}")
        return False

def trigger_whatsapp_blast(district_name, phone_numbers_string):
    """Pings the local Node.js server to send WhatsApp messages."""
    WHATSAPP_GATEWAY_URL=os.getenv("WHATSAPP_SERVER_URL")
    numbers = [n.strip() for n in phone_numbers_string.split(',') if n.strip()]
    message_text = (
        f"*Health Alert: {district_name}*\n\n"
        f"Our records show a high vaccination dropout risk in your area. "
        f"If your child has received the BCG vaccine, please ensure they receive "
        f"their DPT and Polio boosters immediately. Visit your nearest Govt. Health Center."
    )
    
    payload = {
        "numbers": numbers,
        "message": message_text
    }

    try:
        log_action(f"Connecting to WhatsApp Gateway for {len(numbers)} contacts...")
        response = requests.post(WHATSAPP_GATEWAY_URL, json=payload, timeout=30)
        
        if response.status_code == 200:
            log_action("WHATSAPP BATCH: Request accepted by Node.js server.")
            return "WhatsApp Sent"
        else:
            log_action(f"WHATSAPP ERROR: Gateway returned {response.status_code}")
            return "Gateway Error"
    except Exception as e:
        log_action(f"WHATSAPP FAILED: Is the Node.js server running? {str(e)}")
        return "Connection Failed"