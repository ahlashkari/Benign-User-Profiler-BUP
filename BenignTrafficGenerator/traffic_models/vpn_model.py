#!/usr/bin/env python3

import base64
import json
import random
import requests
import subprocess
import sys
import tempfile
import time
from threading import Timer
from .traffic_model import TrafficModel


class VPNModel(TrafficModel):
    def __init__(self, model_config: dict):
        self.__model_config = model_config

    def generate(self) -> None:
        self.OPENVPN_PATH = "openvpn"
        duration = self.__model_config["duration"]
        username = self.__model_config["username"] if "username" in self.__model_config else None
        password = self.__model_config["password"] if "password" in self.__model_config else None
        config_file = self.__model_config["config_file"] if "config_file" in self.__model_config else None
        if config_file is not None:
            self.connect(config_file, duration, username, password)
        else:
            self.connect_to_random_network(duration)

    def connect_to_random_network(self, duration):
        self.VPNGATE_API_URL = "http://www.vpngate.net/api/iphone/"
        servers = []
        try:
            print("[-] Trying to get server's informations...")
            servers = sorted(self.getServers(), key=lambda server: int(server["Score"]), reverse=True)
        except:
            print("[!] Failed to get server's informations from vpngate.")
            return

        if not servers:
            print("[!] There is no running server on vpngate.")
            return

        print("[-] Got server's informations.")

        random_number = random.randint(0, len(servers) - 1)
        selected_server = servers[random_number]

        print("[-] Generating .ovpn file of %s..." % (selected_server["IP"], ))
        ovpn_path = self.saveOvpn(selected_server)
        print("[-] Connecting to %s..." % (selected_server["IP"], ))
        self.connect(ovpn_path, duration)

    def getServers(self):
        servers = []
        server_strings = requests.get(self.VPNGATE_API_URL).text
        for server_string in server_strings.replace("\r", "").split('\n')[2:-2]:
            (HostName, IP, Score, Ping, Speed, CountryLong, CountryShort, NumVpnSessions, Uptime, TotalUsers, TotalTraffic, LogType, Operator, Message, OpenVPN_ConfigData_Base64) = server_string.split(',')
            server = {
                'HostName': HostName,
                'IP': IP,
                'Score': Score,
                'Ping': Ping,
                'Speed': Speed,
                'CountryLong': CountryLong,
                'CountryShort': CountryShort,
                'NumVpnSessions': NumVpnSessions,
                'Uptime': Uptime,
                'TotalUsers': TotalUsers,
                'TotalTraffic': TotalTraffic,
                'LogType': LogType,
                'Operator': Operator,
                'Message': Message,
                'OpenVPN_ConfigData_Base64': OpenVPN_ConfigData_Base64
            }
            servers.append(server)
        return servers

    def saveOvpn(self, server):
        _, ovpn_path = tempfile.mkstemp()
        ovpn = open(ovpn_path, 'w')
        ovpn.write(str(base64.b64decode(server["OpenVPN_ConfigData_Base64"])))
        ovpn.write(str('\nscript-security 2\nup /etc/openvpn/update-resolv-conf\ndown /etc/openvpn/update-resolv-conf'.encode()))
        ovpn.close()
        return ovpn_path

    def connect(self, ovpn_path, duration, username=None, password=None):
        command = f'sudo {self.OPENVPN_PATH} --config {ovpn_path}'
        if username is not None and password is not None:
            command += ' --auth-user-pass <(echo -e "{username}\\n{password}")'
        elif password is not None:
            command += ' --auth-user-pass <(echo -e "{username}")'

        openvpn_process = subprocess.Popen(['bash', command], shell=True)

        print(f"Running the VPN for {duration} seconds...")
        timer = Timer(duration, openvpn_process.kill)
        try:
            timer.start()
            stdout, stderr = openvpn_process.communicate()
        finally:
            timer.cancel()
