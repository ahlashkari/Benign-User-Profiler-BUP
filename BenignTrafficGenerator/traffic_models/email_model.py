#!/usr/bin/env python3

import email
import imaplib
import smtplib
from email.message import EmailMessage
from .traffic_model import TrafficModel


class SMTPModel(TrafficModel):
    def __init__(self, model_config: dict):
        # TODO: verify the model config
        self.__model_config = model_config

    def generate(self) -> None:
        # TODO: check other mail servers
        server = smtplib.SMTP_SSL('smtp.gmail.com')
        port = 465
        server.connect("smtp.gmail.com", port)
        sender = self.__model_config["sender"]
        password = self.__model_config["password"]
        receivers = self.__model_config["receivers"]

        # TODO: add wait_after
        # TODO: add frequency, start_time, and time_interval
        for email in self.__model_config["emails"]:
            message = EmailMessage()
            message.set_content(email["text"])
            message['Subject'] = email["subject"]
            message['From'] = sender
            message['To'] = ", ".join(receivers)
            server.login(sender, password)
            text = message.as_string()
            server.sendmail(sender, receivers, text)
        server.quit()


class IMAPModel(TrafficModel):
    def __init__(self, model_config: dict):
        # TODO: verify the model config
        self.__model_config = model_config

    def generate(self) -> None:
        # TODO: check other mail servers
        # TODO: check to read attachments
        # TODO: check to read specific number of emails
        # TODO: add try catch
        username = self.__model_config["username"]
        password = self.__model_config["password"]

        mail = imaplib.IMAP4_SSL("imap.gmail.com")
        mail.login(username, password)
        status, messages = mail.select("INBOX")
        _, selected_mails = mail.search(None, 'ALL')
        for num in selected_mails[0].split():
            _, data = mail.fetch(num, '(RFC822)')
            _, bytes_data = data[0]

            email_message = email.message_from_bytes(bytes_data)
            print("\n")
            print(40 * "=")

            print("Subject: ",email_message["subject"])
            print("To:", email_message["to"])
            print("From: ",email_message["from"])
            print("Date: ",email_message["date"])
            for part in email_message.walk():
                if part.get_content_type() == "text/plain" or \
                        part.get_content_type() == "text/html":
                    message = part.get_payload(decode=True)
                    print("Message: \n", message.decode())
                    print(40 * "=", "\n")
                    break
        mail.close()
        mail.logout()
