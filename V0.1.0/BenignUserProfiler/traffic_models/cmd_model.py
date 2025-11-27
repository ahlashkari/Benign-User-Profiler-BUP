#!/usr/bin/env python3

import time
import subprocess
from .traffic_model import TrafficModel


class CMDModel(TrafficModel):
    def __str__(self):
        return "CMD"

    def verify(self) -> bool:
        for key in ["commands"]:
            if key not in self.model_config:
                print(f">>> Error in CMD model: No '{key}' specified in the config!")
                return False
        return True

    def generate(self) -> None:
        for command in self.model_config["commands"]:
            try:
                subprocess.run(command["str"], shell=True)
                if "wait_after" in command:
                    time.sleep(command["wait_after"])
            except Exception as e:
                print(f">>> Error in CMD model. command: {command['str']}")
                print(e)
                continue
