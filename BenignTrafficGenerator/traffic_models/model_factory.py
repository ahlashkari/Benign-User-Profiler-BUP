#!/usr/bin/env python3

from selenium import webdriver
from .traffic_model import TrafficModel
from .http_model import HTTPModel
from .ssh_model import SSHModel
from .cmd_model import CMDModel
from .email_model import SMTPModel, IMAPModel
from .ftp_model import FTPModel
from .db_model import MongoDBModel


class ModelFactory(object):
    def __init__(self):
        self.firefox_driver = webdriver.Firefox()

    def create_model(self, model_config: dict) -> TrafficModel:
        # TODO: change it to use enum
        if model_config["type"] == "HTTP" or model_config["type"] == "HTTPS":
            return HTTPModel(model_config, self.firefox_driver)
        if model_config["type"] == "SSH":
            return SSHModel(model_config)
        if model_config["type"] == "CMD":
            return CMDModel(model_config)
        if model_config["type"] == "SMTP":
            return SMTPModel(model_config)
        if model_config["type"] == "IMAP":
            return IMAPModel(model_config)
        if model_config["type"] == "FTP":
            return FTPModel(model_config)
        if model_config["type"] == "SFTP":
            return FTPModel(model_config=model_config, ssl=True)
        if model_config["type"] == "MongoDB":
            return MongoDBModel(model_config)

        print(f">>>> Error occured, unknown type '{model_config['type']}' !")
        return None
