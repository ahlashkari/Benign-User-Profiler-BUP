#!/usr/bin/env python3

import time
from ftplib import FTP_TLS, FTP
from pathlib import Path
from .traffic_model import TrafficModel

class FTPModel(TrafficModel):
    def __init__(self, ssl=False):
        self.__ssl = ssl

    def __str__(self):
        return "FTP/S"

    def verify(self) -> bool:
        for key in ["address", "username", "password"]:
            if key not in self.model_config:
                print(f">>> Error in FTP/S model: No '{key}' specified in the config!")
                return False

        if "downloads" in self.model_config:
            for download in self.model_config["downloads"]:
                for key in ["path", "output_dir", "file_name"]:
                    if key not in download:
                        print(f">>> Error in FTP/S model: No '{key}' specified in the downloads"
                              f" config! download: {download}")
                        return False

        if "uploads" in self.model_config:
            for upload in self.model_config["uploads"]:
                for key in ["path", "input_dir", "file_name"]:
                    if key not in upload:
                        print(f">>> Error in FTP/S model: No '{key}' specified in the uploads"
                              f" config! upload: {upload}")
                        return False

        return True

    def generate(self) -> None:
        host = self.model_config["address"]
        downloads = self.model_config["downloads"] if "downloads" in self.model_config else []
        uploads = self.model_config["uploads"] if "uploads" in self.model_config else []
        username = self.model_config["username"]
        password = self.model_config["password"]

        try:
            ftp = FTP_TLS(host=host) if self.__ssl else FTP(host=host)
            ftp.login(username, password)
            if self.__ssl:
                ftp.prot_p()
        except Exception as e:
            print(f">>> Error in FTP/S model.")
            print(e)
            return

        for download in downloads:
            try:
                ftp.cwd(download["path"])
                output_dir = Path(download["output_dir"])
                output_file = output_dir / download["file_name"]
                ftp.retrbinary("RETR " + download["file_name"],
                            open(output_file, 'wb').write)
            except Exception as e:
                print(f">>> Error in FTP/S model, download: {download}")
                print(e)
                continue
            if "wait_after" in download:
                time.sleep(download["wait_after"])

        for upload in uploads:
            try:
                ftp.cwd(upload["path"])
                input_dir = Path(upload["input_dir"])
                input_file = input_dir / upload["file_name"]
                ftp.storbinary("STOR " + upload["file_name"],
                            open(input_file, 'rb'))
            except Exception as e:
                print(f">>> Error in FTP/S model, upload: {upload}")
                print(e)
                continue
            if "wait_after" in upload:
                time.sleep(upload["wait_after"])
