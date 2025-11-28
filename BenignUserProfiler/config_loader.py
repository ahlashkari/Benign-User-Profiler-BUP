#!/usr/bin/env python3

import json
import os

class ConfigLoader:
    def __init__(self):
        self.traffics_configs = {}

    def load(self, config_file_address: str) -> dict:
        self.config_file_address = config_file_address
        try:
            with open(self.config_file_address) as config_file:
                self.traffics_configs = json.loads(config_file.read())
            return self.traffics_configs
        except Exception as error:
            print(f">>> Error in config file!: {error}")
            print(f">>> Config file path: {os.path.abspath(self.config_file_address)}")
            return None