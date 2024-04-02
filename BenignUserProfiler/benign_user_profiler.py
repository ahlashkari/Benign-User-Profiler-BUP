#!/usr/bin/python3

from multiprocessing import Manager
from .traffic_models.model_factory import ModelFactory
from .traffic_generator import TrafficGenerator
from .config_loader import ConfigLoader
from .scheduler import Scheduler

class BenignUserProfiler(object):
    def __init__(self, config_file_address: str, headless: bool, number_of_threads: int):
        print("You initiated Benign Traffic Generator!")
        self.__config_file_address = config_file_address
        self.__headless = headless
        self.__number_of_threads = number_of_threads

    def run(self):
        print(f"> Reading traffics configs from {self.__config_file_address}...")
        config_loader = ConfigLoader(self.__config_file_address)
        traffics_models = []
        print("> Creating traffic models based on the configs...")
        model_factory = ModelFactory(self.__headless)

        for traffic_config in config_loader.traffics_configs:
            traffic_model = model_factory.create_model(traffic_config)
            if traffic_model is not None:
                traffics_models.append(traffic_model)

        print("> Scheduling the tasks...")
        scheduler = Scheduler(traffics_models)
        print("> Starting to generate traffics...")
        traffic_generator = TrafficGenerator(scheduler, self.__number_of_threads)
        traffic_generator.start()
        print("> All traffics has generated!")