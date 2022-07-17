#!/usr/bin/env python3

import requests, json, sys, base64, tempfile, subprocess, time
from .traffic_model import TrafficModel


class TelnetModel(TrafficModel):
    def __init__(self, model_config: dict):
        self.__model_config = model_config

    def generate(self) -> None:
        host = self.__model_config["host"]
        username = self.__model_config["username"]
        password = self.__model_config["password"] if "password" in self.__model_config else None


        OPENVPN_PATH = "openvpn"
        VPNGATE_API_URL = "http://www.vpngate.net/api/iphone/"
        DEFAULT_COUNTRY = "US"
        SELECTED_COUNTRY = ""
        DEFAULT_SERVER = 0
        YES = False

        if len(sys.argv) > 1:
            if sys.argv[1] == "-y":
                YES = True
            else:
                SELECTED_COUNTRY = sys.argv[1]

        servers = []
        try:
            print("[-] Trying to get server's informations...")
            servers = sorted(getServers(), key=lambda server: int(server["Score"]), reverse=True)
        except:
            print("[!] Failed to get server's informations from vpngate.")
            sys.exit(1)

        if not servers:
            print("[!] There is no running server on vpngate.")
            sys.exit(1)

        print("[-] Got server's informations.")

        countries = sorted(getCountries(servers))

        if not SELECTED_COUNTRY:
            printCountries(countries)

        selected_country = selectCountry(countries)

        print("[-] Gethering %s servers..." % (selected_country, ))

        selected_servers = [server for server in servers if server['CountryShort'] == selected_country]
        printServers(selected_servers)
        selected_server = selectServer(selected_servers)

        print("[-] Generating .ovpn file of %s..." % (selected_server["IP"], ))

        ovpn_path = saveOvpn(selected_server)

        print("[-] Connecting to %s..." % (selected_server["IP"], ))

        connect(ovpn_path)

    def getServers():
        servers = []
        server_strings = requests.get(VPNGATE_API_URL).text
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

    def getCountries(server):
        return set((server['CountryShort'], server['CountryLong']) for server in servers)

    def printCountries(countries):
        print("    Connectable countries:")
        newline = False
        for country in countries:
            print("    %-2s) %-25s" % (country[0], country[1])),
            if newline:
                print('\n'),
            newline = not newline
        if newline:
            print('\n'),

    def printServers(servers):
        print("  Connectable Servers:")
        for i in range(len(servers)):
            server = servers[i]

            ipreq = requests.get("https://ipinfo.io/%1s" % (server['IP']))
            ipinfo = json.loads(ipreq.text)

            print("    %2d) %-15s [%6.2f Mbps, ping:%4s ms, score: %3s, hostname: ," % (i,
                                                                            server['IP'],
                                                                            float(server['Speed'])/10**6,
                                                                            server['Ping'],
                                                                            server['Score']))#,
                                                                            #                                                                        ipinfo['hostname']))

            print("                          city: %1s, region: %2s, org: %3s ]\n" % (ipinfo['city'], ipinfo['region'], ipinfo['org'].split(' ', 1)[1]))

    def selectCountry(countries):
        selected = SELECTED_COUNTRY
        default_country = DEFAULT_COUNTRY
        short_countries = list(country[0] for country in countries)
        if not default_country in short_countries:
            default_country = short_countries[0]
        if YES:
            selected = default_country
        while not selected:
            try:
                selected = input("[?] Select server's country to connect [%s]: " % (default_country, )).strip().upper()
            except:
                print("[!] Please enter short name of the country.")
                selected = ""
            if selected == "":
                selected = default_country
            elif not selected in short_countries:
                print("[!] Please enter short name of the country.")
                selected = ""
        return selected

    def selectServer(servers):
        selected = -1
        default_server = DEFAULT_SERVER
        if YES:
            selected = default_server
        while selected == -1:
            try:
                selected = input("[?] Select server's number to connect [%d]: " % (default_server, )).strip()
            except:
                print("[!] Please enter vaild server's number.")
                selected = -1
            if selected == "":
                selected = default_server
    #        elif not selected.isdigit() or int(selected) >= len(servers):
            elif  int(selected) >= len(servers):
                print("[!] Please enter vaild server's number.")
                selected = -1
        return servers[int(selected)]

    def saveOvpn(server):
        _, ovpn_path = tempfile.mkstemp()
        ovpn = open(ovpn_path, 'w')
        ovpn.write(str(base64.b64decode(server["OpenVPN_ConfigData_Base64"])))
        ovpn.write(str('\nscript-security 2\nup /etc/openvpn/update-resolv-conf\ndown /etc/openvpn/update-resolv-conf'.encode()))
        ovpn.close()
        return ovpn_path

    def connect(ovpn_path):
        openvpn_process = subprocess.Popen(['sudo', OPENVPN_PATH, '--config', ovpn_path])
        try:
            while True:
                time.sleep(600)
        # termination with Ctrl+C
        except:
            try:
                openvpn_process.kill()
            except:
                pass
            while openvpn_process.poll() != 0:
                time.sleep(1)
            print("[=] Disconnected OpenVPN.")
