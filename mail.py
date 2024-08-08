import smtplib
import ssl
from dotenv import load_dotenv
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

class MailSender:
    # Load environment variables
    load_dotenv()
    MAIL_EMAIL = os.getenv("MAIL_EMAIL")
    MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")
    MAIL_PORT = os.getenv("MAIL_PORT")
    MAIL_RECEIVER = os.getenv("MAIL_RECEIVER")
    MAIL_FILE = os.getenv("MAIL_FILE")
    
    @staticmethod
    def login():
        context = ssl.create_default_context()
        
        try:
            server = smtplib.SMTP_SSL("smtp.gmail.com", MailSender.MAIL_PORT, context=context)
            server.login(MailSender.MAIL_EMAIL, MailSender.MAIL_PASSWORD)
            print("Logged in successfully")
            return server
        except Exception as e:
            print(f"Failed to login: {e}")
            return None

    @staticmethod   
    def sendMail(filename):
        server = MailSender.login()
        if server is None:
            print("Login failed, email not sent.")
            return

        subject = "USOM Bugünün yasaklı siteleri"
        body = "dosya : "
        sender_email = MailSender.MAIL_EMAIL
        receiver_email = MailSender.MAIL_RECEIVER

        message = MIMEMultipart()
        message["From"] = sender_email
        message["To"] = receiver_email
        message["Subject"] = subject
        message["Bcc"] = receiver_email

        # Add body to email
        message.attach(MIMEText(body, "plain"))

        try:
            with open(filename, "rb") as attachment:
                # Add file as application/octet-stream
                # Email client can usually download this automatically as attachment
                part = MIMEBase("application", "octet-stream")
                part.set_payload(attachment.read())
            
            encoders.encode_base64(part)

            part.add_header(
                "Content-Disposition",
                f"attachment; filename= {filename}",
            )

            message.attach(part)
            text = message.as_string()

            server.sendmail(sender_email, receiver_email, text)
            print("Email sent successfully")
        except Exception as e:
            print(f"Failed to send email: {e}")
        finally:
            server.quit()
            print("Server connection closed")
