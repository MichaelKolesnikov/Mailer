import smtplib
import ssl
import uuid
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.utils import formatdate

from MailerConfig import MailerConfig


class Mailer:
    def __init__(self, mailer_config: MailerConfig):
        self.smtp_server = mailer_config.smtp_server
        self.port = mailer_config.port 
        self.sender_email = mailer_config.sender_email
        self.sender_app_password = mailer_config.sender_app_password

    def send_message(self, receiver_email, subject, body):
        message = MIMEMultipart()
        message["From"] = self.sender_email
        message["To"] = receiver_email
        message["Subject"] = subject
        message["Message-ID"] = f"<{uuid.uuid4()}@{self.smtp_server}>"  # Unique ID
        message["Date"] = formatdate(localtime=True)  # Proper timestamp
        # message.attach(MIMEText(body, "plain"))

        # html_body = markdown.markdown(body)
        message.attach(MIMEText(body, "plain"))
        # MIME -- это кодировка чего-то графического с помощью текста, разобраться

        context = ssl.create_default_context()
        with smtplib.SMTP(self.smtp_server, self.port) as server:
            server.starttls(context=context)
            server.login(self.sender_email, self.sender_app_password)
            server.sendmail(self.sender_email, receiver_email, message.as_string())
