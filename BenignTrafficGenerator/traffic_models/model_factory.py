#!/usr/bin/env python3

from .traffic_model import TrafficModel
from .http_model import HTTPModel


class ModelFactory(object):
    def create_model(self, model_config: dict) -> TrafficModel:
        # TODO: change it to use enum
        if model_config["type"] == "HTTP" or model_config["type"] == "HTTPS":
            return HTTPModel(model_config)
        print(f">>>> Error occured, unknown type '{model_config['type']}' !")
        return None
