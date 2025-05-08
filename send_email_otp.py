import random
import smtplib
from email.message import EmailMessage

# Store OTPs temporarily
otp_storage = {}

# ✅ Use your Gmail & App Password here
SENDER_EMAIL = "eshwarsaikuntala@gmail.com"
SENDER_PASSWORD = "rqhy zjqv ydxc yinf"  # ⚠️ Replace with your App Password

def generate_otp():
    """Generate a 6-digit OTP"""
    return str(random.randint(100000, 999999))

def send_otp_via_email(email):
    """Generate and send OTP to the given email"""
    otp = generate_otp()
    otp_storage[email] = otp  # Store OTP for verification

    msg = EmailMessage()
    msg.set_content(f"Your OTP is: {otp}")
    msg["Subject"] = "OTP Verification"
    msg["From"] = SENDER_EMAIL
    msg["To"] = email

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            print("🔄 Connecting to Gmail SMTP Server...")
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            print("✅ Logged in successfully!")
            server.send_message(msg)
            print(f"✅ OTP sent successfully to {email}")
    except smtplib.SMTPAuthenticationError:
        print("❌ Authentication Error: Check your email/password (Use App Password!)")
    except smtplib.SMTPException as e:
        print(f"❌ Email Sending Error: {e}")

def verify_otp(email, user_otp):
    """Verify the user-entered OTP"""
    if email in otp_storage and otp_storage[email] == user_otp:
        print("✅ OTP verified successfully!")
        return True
    else:
        print("❌ Invalid OTP. Try again.")
        return False

# ✅ Run a test (Uncomment to check)
send_otp_via_email("your_test_email@gmail.com")  # Replace with your test email
