import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

class EmailService:
    @staticmethod
    def send_confirmation_email(to_email, name, message, title=None):
        smtp_server = "smtp.gmail.com"
        smtp_port = 465
        sender_email = os.getenv('SMTP_EMAIL', '')
        sender_password = os.getenv('SMTP_PASSWORD', '')

        template_path = os.path.join(
            os.path.abspath(os.path.dirname(__file__)),
            'templates',
            'confirmation_email_template.html'
        )

        with open(template_path, "r") as file:
            html_content = file.read()

        html_content = html_content.replace("{{name}}", name)
        html_content = html_content.replace("{{title}}", title)
        html_content = html_content.replace("{{message}}", message)

        msg = MIMEMultipart("alternative")
        msg["Subject"] = "AC Contato"
        msg["From"] = sender_email
        msg["To"] = to_email

        msg.attach(MIMEText(html_content, "html"))

        try:
            with smtplib.SMTP_SSL(smtp_server, smtp_port) as server:
                server.ehlo()
                server.login(sender_email, sender_password)
                server.sendmail(sender_email, to_email, msg.as_string())
                server.close()
            print(f"HTML email sent to {to_email}")
        except Exception as e:
            print(f"Failed to send email: {e}")