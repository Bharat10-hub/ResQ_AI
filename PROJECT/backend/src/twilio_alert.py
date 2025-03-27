import os
from twilio.rest import Client
import re

# Load credentials from environment variables
TWILIO_SID = "TWILIO_SID"
TWILIO_AUTH_TOKEN = "TWILIO_AUTH_TOKEN"
TWILIO_PHONE_NUMBER = "TWILIO_PHONE_NUMBER"

def is_valid_e164(number):
    return re.match(r'^\+\d{10,15}$', number)

def send_sos(message, recipient):
    if not TWILIO_SID or not TWILIO_AUTH_TOKEN or not TWILIO_PHONE_NUMBER:
        return {"error": "Twilio credentials are missing!"}

    # Validate recipient number
    if not is_valid_e164(recipient):
        return {"error": "Invalid recipient phone number. Use E.164 format: +91987XXXXXXX"}

    try:
        client = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)
        msg = client.messages.create(
            body=message,
            from_=TWILIO_PHONE_NUMBER, 
            to="RECIPIENT PHONE NUMBER"  
        )
        return {"status": "sent", "message_sid": msg.sid}
    except Exception as e:
        print("\n🚨 Twilio Error:", str(e))  # Debugging
        return {"error": str(e)}