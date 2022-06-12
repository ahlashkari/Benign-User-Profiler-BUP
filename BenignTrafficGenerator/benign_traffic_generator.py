#!/usr/bin/python3

from .traffic_models.model_factory import ModelFactory
from .traffic_generator import TrafficGenerator
from .config_loader import ConfigLoader

class BenignTrafficGenerator(object):
    def __init__(self, config_file_address: str):
        print("You initiated Benign Traffic Generator!")
        self.config_file_address = config_file_address

    def run(self):
        print("> Reading traffics configs from", self.config_file_address)
        config_loader = ConfigLoader(self.config_file_address)
        traffics_models = []
        print("> Creating traffic models based on the configs")
        model_factory = ModelFactory()

        for traffic_config in config_loader.traffics_configs:
            traffic_model = model_factory.create_model(traffic_config)
            if traffic_model is not None:
                traffics_models.append(traffic_model)

        print("> Starting to generate traffics...")
        traffic_generator = TrafficGenerator()
        traffic_generator.start(traffics_models)
        print("> All traffics has generated!")

