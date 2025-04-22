import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def load_email_template(template_name, replacements):
    template_path = os.path.join(
        os.path.abspath(os.path.dirname(__file__)),
        'templates',
        template_name
    )

    try:
        with open(template_path, "r") as file:
            html_content = file.read()

        for placeholder, value in replacements.items():
            html_content = html_content.replace(f"{{{{{placeholder}}}}}", value)

        return html_content
    except FileNotFoundError:
        raise Exception(f"Template file {template_name} not found.")


def send_email(to_email, subject, html_content):
    # Get SMTP configuration from environment variables with defaults
    smtp_server = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
    smtp_port = int(os.getenv('SMTP_PORT', '465'))
    smtp_use_tls = os.getenv('SMTP_USE_TLS', 'false').lower() == 'true'
    sender_email = os.getenv('SMTP_EMAIL', '')
    sender_password = os.getenv('SMTP_PASSWORD', '')
    sender_name = os.getenv('SMTP_SENDER_NAME', 'WhatsTime')

    if not sender_email or not sender_password:
        raise Exception("SMTP credentials are not set in environment variables.")

    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = f"{sender_name} <{sender_email}>"
    msg["To"] = to_email
    msg.attach(MIMEText(html_content, "html"))

    try:
        if smtp_use_tls:
            # Use TLS connection
            server = smtplib.SMTP(smtp_server, smtp_port)
            server.starttls()
        else:
            # Use SSL connection
            server = smtplib.SMTP_SSL(smtp_server, smtp_port)
        
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, to_email, msg.as_string())
        server.quit()
        print(f"Email sent successfully to {to_email}")
    except Exception as e:
        print(f"Failed to send email: {e}")
        raise Exception(f"Failed to send email: {e}")


def send_confirmation_email(to_email, name, message, title):
    replacements = {
        "to_email": to_email,
        "name": name,
        "message": message,
        "title": title,
    }
    html_content = load_email_template('confirmation_email_template.html', replacements)
    send_email(to_email, subject="AC Contato", html_content)
    