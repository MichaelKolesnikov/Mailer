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
        subject_template = subject_file.read()

    with open("body.txt") as body_file:
        body_template = body_file.read()

    with open("addressees1.csv", 'r', encoding='utf-8') as file:
        headers = file.readline()
        reader = csv.reader(file)
        for row in reader:
            full_name, email_address, first_name, last_name, affiliation = row

            try:
                mailer.send_message(
                    receiver_email=email_address,
                    subject=subject_template
                        .replace(
                        "{full_name_with_affiliation}",
                        (full_name or f"{first_name} {last_name}") + ("" if not affiliation else f", {affiliation}")
                    ),
                    body=body_template
                        .replace("{first_name}", first_name)
                        .replace("{last_name}", last_name)
                        .replace("{full_name}", full_name)
                        .replace("{affiliation}", affiliation)
                )
                print(f"Email to {email_address} sent successfully!")
            except Exception as e:
                print(e)


if __name__ == "__main__":
    main()
