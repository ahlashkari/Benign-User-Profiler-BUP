#!/usr/bin/env python3

from datetime import datetime
from selenium import webdriver
from selenium.webdriver import FirefoxOptions
from webdriver_manager.firefox import GeckoDriverManager
from .traffic_model import TrafficModel
from .http_model import HTTPModel
from .ssh_model import SSHModel
from .cmd_model import CMDModel
from .email_model import SMTPModel, IMAPModel
from .ftp_model import FTPModel


class ModelFactory(object):
    def __init__(self, headless: bool):
        firefox_options = FirefoxOptions()
        if headless:
            firefox_options.add_argument("--headless")
        # TODO: check parallelism with having only one browser, it will probably have some problems
        self.firefox_driver = webdriver.Firefox(options=firefox_options)

    def create_model(self, model_config: dict) -> TrafficModel:
        model_type = model_config["type"].upper()
        model: TrafficModel
        if model_type == "HTTP" or model_type == "HTTPS":
            model = HTTPModel(self.firefox_driver)
        elif model_type == "SSH":
            model = SSHModel()
        elif model_type == "CMD":
            model = CMDModel()
        elif model_type == "SMTP":
            model = SMTPModel()
        elif model_type == "IMAP":
            model = IMAPModel()
        elif model_type == "FTP":
            model = FTPModel()
        elif model_type == "SFTP":
            model = FTPModel(True)
        else:
            print(f">>> Error occured in creating models, unknown type '{model_config['type']}'!")
            return None
        model.model_config = model_config
        if not model.verify():
            print(f">>> Error occured in {model} model! Ignoring this model.")
            return None

        if "start_time" in model_config:
            model.start_time = datetime.strptime(model_config["start_time"],
                                                 model_config["start_time_format"])
        if "frequency" in model_config:
            model.frequency = model_config["frequency"]
        if "time_interval" in model_config:
            model.time_interval = model_config["time_interval"]
        return model