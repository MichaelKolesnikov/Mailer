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

    with open("people.csv", 'r', encoding='utf-8') as file:
        headers = file.readline()
        reader = csv.reader(file)
        for row in reader:
            email_address, first_name, last_name, affiliation = row

            try:
                with open("subject.txt") as subject_file:
                    subject = subject_file.read()

                with open("body.md") as body_file:
                    body = f"**Dear {first_name} {last_name},**\n" + body_file.read()

                mailer.send_message(
                    receiver_email=email_address,
                    subject=subject,
                    body=body
                )
                print(f"Email to {email_address} sent successfully!")
            except Exception as e:
                print(e)


if __name__ == "__main__":
    main()
