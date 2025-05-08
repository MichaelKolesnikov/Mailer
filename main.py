from os import getenv
import csv

from dotenv import load_dotenv

from MailerConfig import MailerConfig
from Mailer import Mailer


load_dotenv()


def main():
    sender_email = getenv("SENDER_EMAIL")
    sender_app_password = getenv("SENDER_APP_PASSWORD")
    mailer_config = MailerConfig(sender_email, sender_app_password)
    mailer = Mailer(mailer_config)

    with open("subject.txt") as subject_file:
        subject = subject_file.read()

    logo_cid = mailer.add_image("logo.png")
    with open("body.html") as body_file:
        body_main = body_file.read()
    body_main = body_main.replace("{logo_cid}", str(logo_cid))

    with open("people.csv", 'r', encoding='utf-8') as file:
        headers = file.readline()
        reader = csv.reader(file)
        for row in reader:
            email_address, first_name, last_name, affiliation = row
            try:
                cur_body = body_main.replace("{first_name}", first_name).replace("{last_name}", last_name)
                mailer.send_message(
                    receiver_email=email_address,
                    subject=subject,
                    html_body=cur_body
                )
                print(f"Email to {email_address} sent successfully!")
            except Exception as e:
                print(e)


if __name__ == "__main__":
    main()
