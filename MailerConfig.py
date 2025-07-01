class MailerConfig:
    def __init__(self, sender_email, sender_app_password, smtp_server = "smtp.gmail.com", port = 587):
        self.smtp_server = smtp_server
        self.port = port
        self.sender_email = sender_email
        self.sender_app_password = sender_app_password
