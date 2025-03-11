import os
import smtplib
import logging

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

class EmailService:
    @staticmethod
    def send_confirmation_email(to_email: str, name: str, message: str, title: str = None) -> None:
        smtp_server = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
        smtp_port = int(os.getenv('SMTP_PORT', '465'))
        sender_email = os.getenv('SMTP_EMAIL', '')
        sender_password = os.getenv('SMTP_PASSWORD', '')

        if not sender_email or not sender_password:
            logger.error("Sender email or password is not set in environment variables")
            return

        template_path = os.path.join(
            os.path.abspath(os.path.dirname(__file__)),
            'templates',
            'confirmation_email_template.html'
        )

        try:
            with open(template_path, "r") as file:
                html_content = file.read()
        except Exception as e:
            logger.error(f"Failed to read email template: {e}")
            return

        html_content = html_content.replace("{{name}}", name)
        html_content = html_content.replace("{{title}}", title if title else "AC Contato")
        html_content = html_content.replace("{{message}}", message)

        plain_text = f"Olá {name},\n\n{message}\n\nAtenciosamente,\nEquipe AC Contato"

        msg = MIMEMultipart("alternative")
        subject = title if title else "AC Contato"

        msg["Subject"] = subject
        msg["From"] = sender_email
        msg["To"] = to_email
        msg["Reply-To"] = sender_email
        msg["X-Mailer"] = "Python EmailService"

        part1 = MIMEText(plain_text, "plain")
        part2 = MIMEText(html_content, "html")
        msg.attach(part1)
        msg.attach(part2)

        try:
            with smtplib.SMTP_SSL(smtp_server, smtp_port) as server:
                server.ehlo()
                server.login(sender_email, sender_password)
                server.sendmail(sender_email, to_email, msg.as_string())
                server.close()
            logger.info(f"HTML email sent successfully to {to_email}")
        except smtplib.SMTPException as smtp_error:
            logger.error(f"SMTP error occurred: {smtp_error}")
        except Exception as e:
            logger.error(f"Failed to send email: {e}")