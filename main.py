import time
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

    with open("People.csv", 'r', encoding='utf-8') as file:
        delivery_counter = 0
        headers = file.readline()
        reader = csv.reader(file)
        for row in reader:
            if delivery_counter > 500:
                break
            email,first_name,last_name,full_name,affiliation,country,career_position,data_source = row
            if not first_name:
                continue
            affiliation = affiliation.split('\n')[0]
            time.sleep(2)
            try:
                mailer.send_message(
                    receiver_email=email,
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
                print(f"Email to {email} sent successfully!")
            except Exception as e:
                print(e)
            delivery_counter += 1


if __name__ == "__main__":
    main()
