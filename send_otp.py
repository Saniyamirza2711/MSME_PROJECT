import smtplib
from email.message import EmailMessage
import random

# Sender Email (Use a Gmail account with App Password enabled)
SENDER_EMAIL = "eshwarsaikuntala@gmail.com"
SENDER_PASSWORD = "iqsr ilzp fatw joad"  # Use an App Password, not your real password

# Admin Email (Receiver)
ADMIN_EMAIL = "eshwarsaikuntala@gmail.com"  

def generate_otp():
    """Generates a 6-digit OTP."""
    return str(random.randint(100000, 999999))

def send_otp(otp):
    """Sends OTP via Email instead of SMS."""
    msg = EmailMessage()
    msg.set_content(f"Your OTP for stock reorder is: {otp}")
    msg["Subject"] = "OTP Verification"
    msg["From"] = SENDER_EMAIL
    msg["To"] = ADMIN_EMAIL

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            server.send_message(msg)
        print("OTP Sent Successfully via Email!")
    except Exception as e:
        print("Failed to send OTP:", str(e))

# Test function (Remove in production)
if __name__ == "__main__":
    otp = generate_otp()
    send_otp(otp)
