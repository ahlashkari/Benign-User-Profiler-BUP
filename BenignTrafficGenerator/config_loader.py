#!/usr/bin/env python3

import json

class ConfigLoader:
    def __init__(self, config_file_address: str) -> list:
        self.config_file_address = config_file_address
        self.traffics_configs = []
        self.read_config_file()

    def read_config_file(self):
        try:
            with open(self.config_file_address) as config_file:
                self.traffics_configs = json.loads(config_file.read())
        except Exception as error:
            print(f">> Error in config file!: {error}")
