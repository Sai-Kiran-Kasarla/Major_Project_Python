import smtplib
from email.message import EmailMessage
import streamlit as st


SENDER_EMAIL = st.secrets["SENDER_EMAIL"]
APP_PASSWORD = st.secrets["APP_PASSWORD"]


def send_otp_email(receiver_email, otp):
    """
    Send an OTP email to the specified receiver.
    """
    message = EmailMessage()

    message["Subject"] = "LearnHub OTP Verification"
    message["From"] = SENDER_EMAIL
    message["To"] = receiver_email

    message.set_content(
        f"""
Hello,

Your LearnHub OTP is:

{otp}

Please use this OTP to complete your verification.

Regards,
LearnHub Team
"""
    )

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(SENDER_EMAIL, APP_PASSWORD)
            server.send_message(message)

        return True

    except Exception as e:
        print(f"Email sending error: {e}")
        return False


def send_otp(receiver_email, otp):
    """
    Compatibility wrapper for existing code that uses send_otp.
    """
    return send_otp_email(receiver_email, otp)