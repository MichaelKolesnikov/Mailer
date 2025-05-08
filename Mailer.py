import os
import smtplib
import ssl
import uuid
from email.mime.image import MIMEImage
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.utils import formatdate
import markdown
from markdown.extensions.extra import extensions

from MailerConfig import MailerConfig


class Mailer:
    def __init__(self, mailer_config: MailerConfig):
        self.smtp_server = mailer_config.smtp_server
        self.port = mailer_config.port
        self.sender_email = mailer_config.sender_email
        self.sender_app_password = mailer_config.sender_app_password
        self.images = {}

    def add_image(self, image_path: str):
        cid = str(uuid.uuid4())
        self.images[cid] = image_path
        return cid

    def send_message(self, receiver_email, subject, html_body):
        message = MIMEMultipart()
        message["From"] = self.sender_email
        message["To"] = receiver_email
        message["Subject"] = subject
        message["Message-ID"] = f"<{uuid.uuid4()}@{self.smtp_server}>"  # Unique ID
        message["Date"] = formatdate(localtime=True)  # Proper timestamp
        # message.attach(MIMEText(body, "plain"))

        message.attach(MIMEText(html_body, "html"))

        for cid, image_path in self.images.items():
            with open(image_path, "rb") as img_file:
                img = MIMEImage(img_file.read())
                img.add_header("Content-ID", f"<{cid}>")
                img.add_header("Content-Disposition", "inline", filename=os.path.basename(image_path))
                message.attach(img)

        context = ssl.create_default_context()
        with smtplib.SMTP(self.smtp_server, self.port) as server:
            server.starttls(context=context)
            server.login(self.sender_email, self.sender_app_password)
            server.sendmail(self.sender_email, receiver_email, message.as_string())
