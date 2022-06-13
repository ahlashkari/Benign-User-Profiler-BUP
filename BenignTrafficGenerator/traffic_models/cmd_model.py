#!/usr/bin/env python3

import time
import subprocess
from .traffic_model import TrafficModel


class CMDModel(TrafficModel):
    def __init__(self, model_config: dict):
        # TODO: verify the model config: e.g. type, link, browser are mandatory
        self.__model_config = model_config

    def generate(self) -> None:
        # TODO: add wait_after
        for command in self.__model_config["commands"]:
            subprocess.run(command["str"], shell=True)
