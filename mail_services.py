import smtplib
from email.message import EmailMessage

SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

SENDER_EMAIL = "ceosaikiran@gmail.com"
SENDER_PASSWORD = "vuss pvuv totf jaob"


def send_otp(receiver_email, otp):
    message = EmailMessage()
    message["Subject"] = "LearnHub - OTP Verification"
    message["From"] = SENDER_EMAIL
    message["To"] = receiver_email

    message.set_content(
        "Hello,\n\n"
        "Your LearnHub verification OTP is: " + str(otp) + "\n\n"
        "This OTP is for account verification/login.\n"
        "Please do not share it with anyone.\n\n"
        "Regards,\n"
        "LearnHub\n"
        "Learning Management System"
    )

    try:
        server = smtplib.SMTP(
            SMTP_SERVER,
            SMTP_PORT,
            timeout=20
        )
        server.starttls()
        server.login(
            SENDER_EMAIL,
            SENDER_PASSWORD
        )
        server.send_message(message)
        server.quit()
        return True

    except Exception as error:
        print("SMTP Error:", error)
        return False


def send_otp_email(receiver_email, otp):
    return send_otp(receiver_email, otp)
