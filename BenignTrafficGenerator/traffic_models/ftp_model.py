#!/usr/bin/env python3

from .traffic_model import TrafficModel
from ftplib import FTP_TLS

class FTPModel(TrafficModel):
    def __init__(self, model_config: dict):
        # TODO: verify the model config
        self.__model_config = model_config

    def generate(self) -> None:
        host = self.__model_config["address"]
        downloads = self.__model_config["downloads"] if "downloads" in self.__model_config else []
        uploads = self.__model_config["uploads"] if "uploads" in self.__model_config else []
        username = self.__model_config["username"]
        password = self.__model_config["password"]

        with FTP_TLS(host=host) as ftp:
            ftp.login(username, password)
            ftp.dir()

            # TODO: add wait_after
            # TODO: use with open instead of open(filename, ...)
            for download in downloads:
                ftp.cwd('/pub/')          #change directory to /pub/
                files = ftp.dir()
                print(files)

                # Downloading the robots.txt file
                filename='robots.txt'
                ftp.retrbinary("RETR " + filename, open(filename, 'wb').write)
                print(download)

            for upload in uploads:
                ftp.cwd('/pub/')          #change directory to /pub/
                files = ftp.dir()
                print(files)

                # Downloading the robots.txt file
                filename='robots.txt'
                ftp.storbinary("STOR " + filename, open(filename, 'rb').read())
                print(upload)
