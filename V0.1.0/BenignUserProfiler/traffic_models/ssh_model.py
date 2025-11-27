#!/usr/bin/env python3

from datetime import datetime
import time
import paramiko
from .traffic_model import TrafficModel


class SSHModel(TrafficModel):
    def __str__(self):
        return "SSH"

    def verify(self) -> bool:
        for key in ["username", "address"]:
            if key not in self.model_config:
                print(f">>> Error in SSH model: No '{key}' specified in the config!")
                return False
        if "password" not in self.model_config and "private_key" not in self.model_config:
            print(f">>> Error in SSH model: No 'private_key' or 'password' specified in the config!")
            return False
        return True

    def generate(self) -> None:
        host = self.model_config["address"]
        port = self.model_config["port"] if "port" in self.model_config else 22
        username = self.model_config["username"]
        password = self.model_config["password"] if "password" in self.model_config else None
        private_key = self.model_config["private_key"] if "private_key" in self.model_config else None

        try:
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            if password is None:
                private_key_file = paramiko.RSAKey.from_private_key_file(private_key)
                ssh.connect(username=username, hostname=host, port=port, pkey=private_key_file)
            else:
                ssh.connect(username=username, hostname=host, password=password, port=port)
                
        except Exception as e:
            print(f">>> Error in SSH model.")
            print(e)
            return

        for command in self.model_config["commands"]:
            try:
                stdin, stdout, stderr = ssh.exec_command(command["str"])
                print(stdout.read())
                print(f"STD ERROR:\n{stderr.read()}")
                if "wait_after" in command:
                    time.sleep(command["wait_after"])
            except Exception as e:
                print(f">>> Error in SSH model commands: {command['str']}")
                print(e)
                print(f"STD ERROR:\n{stderr.read()}")
                continue
        ssh.close()
