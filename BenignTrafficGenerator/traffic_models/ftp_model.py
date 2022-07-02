#!/usr/bin/env python3

from ftplib import FTP_TLS, FTP
from pathlib import Path
from .traffic_model import TrafficModel

class FTPModel(TrafficModel):
    def __init__(self, model_config: dict, ssl=False):
        # TODO: verify the model config
        self.__model_config = model_config
        self.__ssl = ssl

    # TODO: add wait_after
    # TODO: use with open instead of open(filename, ...)
    # TODO: add log
    # TODO: add port
    def generate(self) -> None:
        host = self.__model_config["address"]
        downloads = self.__model_config["downloads"] if "downloads" in self.__model_config else []
        uploads = self.__model_config["uploads"] if "uploads" in self.__model_config else []
        username = self.__model_config["username"]
        password = self.__model_config["password"]

        ftp = FTP_TLS(host=host) if self.__ssl else FTP(host=host)
        ftp.login(username, password)
        if self.__ssl:
            ftp.prot_p()

        for download in downloads:
            ftp.cwd(download["path"])
            output_dir = Path(download["output_dir"])
            output_file = output_dir / download["file_name"]
            ftp.retrbinary("RETR " + download["file_name"],
                           open(output_file, 'wb').write)

        for upload in uploads:
            ftp.cwd(upload["path"])
            input_dir = Path(download["output_dir"])
            input_file = output_dir / download["file_name"]
            ftp.storbinary("STOR " + download["file_name"],
                           open(input_file, 'rb').read())
