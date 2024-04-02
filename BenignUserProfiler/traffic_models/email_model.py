#!/usr/bin/env python3

import email
import time
import imaplib
import os
import smtplib
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from .traffic_model import TrafficModel


class SMTPModel(TrafficModel):
    def __str__(self):
        return "SMTP"

    def verify(self) -> bool:
        for key in ["sender", "password", "receivers", "emails"]:
            if key not in self.model_config:
                print(f">>> Error in SMTP model: No '{key}' specified in the config!")
                return False

        if "emails" in self.model_config:
            for email in self.model_config["emails"]:
                for key in ["subject", "text"]:
                    if key not in email:
                        print(f">>> Error in SMTP model: No '{key}' specified in the emails config!"
                              f" email: {email}")
                        return False

        return True

    def generate(self) -> None:
        try:
            server = smtplib.SMTP_SSL('smtp.gmail.com')
            port = 465
            server.connect("smtp.gmail.com", port)
        except Exception as e:
            print(f">>> Error in SMTP model.")
            print(e)
            return

        sender = self.model_config["sender"]
        password = self.model_config["password"]
        receivers = self.model_config["receivers"]

        for email in self.model_config["emails"]:
            try:
                message = MIMEMultipart()
                message['Subject'] = email["subject"]
                message['From'] = sender
                message['To'] = ", ".join(receivers)
                message.attach(MIMEText(email["text"]))

                for attachment in email["attachments"]:
                    with open(attachment, "rb") as attached_file:
                        part = MIMEApplication(attached_file.read(), Name = os.path.basename(attachment))
                    part['Content-Disposition'] = f'attachment; filename="{os.path.basename(attachment)}"'
                    message.attach(part)

                server.login(sender, password)
                text = message.as_string()
                server.sendmail(sender, receivers, text)
            except Exception as e:
                print(f">>> Error in SMTP model. email: {email}")
                print(e)
                continue
            if "wait_after" in email:
                time.sleep(email["wait_after"])

        server.quit()


class IMAPModel(TrafficModel):
    def __str__(self):
        return "IMAP"

    def verify(self) -> bool:
        for key in ["username", "password", "attachments_dir"]:
            if key not in self.model_config:
                print(f">>> Error in IMAP model: No '{key}' specified in the config!")
                return False
        return True

    def generate(self) -> None:
        username = self.model_config["username"]
        password = self.model_config["password"]

        try:
            mail = imaplib.IMAP4_SSL("imap.gmail.com")
            mail.login(username, password)
            status, messages = mail.select("INBOX")
            _, selected_mails = mail.search(None, 'UnSeen')
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
                    if part.get_content_maintype() == 'multipart':
                        continue
                    if part.get('Content-Disposition') is None:
                        continue

                    filename = part.get_filename()
                    attachment_path = os.path.join(self.model_config["attachments_dir"], filename)
                    if not os.path.isfile(attachment_path):
                        with open(attachment_path, 'wb') as attached_file:
                            attached_file.write(part.get_payload(decode=True))
        except Exception as e:
            print(f">>> Error in IMAP model.")
            print(e)

        mail.close()
        mail.logout()