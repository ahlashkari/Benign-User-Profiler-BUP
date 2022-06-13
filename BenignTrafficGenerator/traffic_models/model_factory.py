#!/usr/bin/env python3

from selenium import webdriver
from .traffic_model import TrafficModel
from .http_model import HTTPModel
from .ssh_model import SSHModel
from .cmd_model import CMDModel


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

        print(f">>>> Error occured, unknown type '{model_config['type']}' !")
        return None
