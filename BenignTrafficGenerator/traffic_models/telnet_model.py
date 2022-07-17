#!/usr/bin/env python3

from telnetlib import Telnet
from .traffic_model import TrafficModel


class TelnetModel(TrafficModel):
    def __init__(self, model_config: dict):
        self.__model_config = model_config

    def generate(self) -> None:
        host = self.__model_config["host"]
        username = self.__model_config["username"]
        password = self.__model_config["password"] if "password" in self.__model_config else None

        tn = Telnet(host)
        tn.read_until(b"login: ")
        tn.write(username.encode('ascii') + b"\n")
        if password is not None:
            tn.read_until(b"Password: ")
            tn.write(password.encode('ascii') + b"\n")

        for command in self.__model_config["commands"]:
            tn.write(command["str"].encode("ascii") + b"\n")

        tn.write(b"exit\n")
        tn.read_all().decode('ascii')
        tn.close()
