#!/usr/bin/env python3

import time
import paramiko
from .traffic_model import TrafficModel


class SSHModel(TrafficModel):
    def __init__(self, model_config: dict):
        # TODO: verify the model config: e.g. type, link, browser are mandatory
        self.__model_config = model_config

    def generate(self) -> None:
        host = self.__model_config["address"]
        port = self.__model_config["port"] if "port" in self.__model_config else 22
        username = self.__model_config["username"]
        password = self.__model_config["password"]

        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(host, port, username, password)
        # TODO: add wait_after
        for command in self.__model_config["commands"]:
            stdin, stdout, stderr = ssh.exec_command(command["str"])
