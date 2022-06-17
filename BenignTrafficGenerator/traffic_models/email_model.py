#!/usr/bin/env python3

import smtplib
from email.message import EmailMessage
from .traffic_model import TrafficModel


class EmailModel(TrafficModel):
    def __init__(self, model_config: dict):
        # TODO: verify the model config: e.g. type, link, browser are mandatory
        self.__model_config = model_config

    def generate(self) -> None:
        pass


class SMTPModel(EmailModel):
    def __init__(self, model_config: dict):
        # TODO: verify the model config: e.g. type, link, browser are mandatory
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
