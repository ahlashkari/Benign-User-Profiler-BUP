
import time
import os
import random
import tempfile
from ftplib import FTP_TLS, FTP, all_errors
from pathlib import Path
from datetime import datetime
from .traffic_model import TrafficModel

class FTPModel(TrafficModel):
    def __init__(self, ssl=False):
        super().__init__()
        self.__ssl = ssl
        self.temp_dir = tempfile.mkdtemp()
        self.protocol = "FTPS" if ssl else "FTP"

    def __str__(self):
        return self.protocol

    def verify(self) -> bool:
        for key in ["address", "username", "password"]:
            if key not in self.model_config:
                print(f">>> Error in {self.protocol} model: No '{key}' specified in the config!")
                return False

        if not any(key in self.model_config for key in ["downloads", "uploads", "browse", "simulate"]):
            print(f">>> Error in {self.protocol} model: No operations specified. Use 'downloads', 'uploads', 'browse', or 'simulate'.")
            return False

        if "downloads" in self.model_config:
            for download in self.model_config["downloads"]:
                for key in ["path", "output_dir", "file_name"]:
                    if key not in download:
                        print(f">>> Error in {self.protocol} model: No '{key}' specified in the downloads"
                              f" config! download: {download}")
                        return False

        if "uploads" in self.model_config:
            for upload in self.model_config["uploads"]:
                for key in ["path", "input_dir", "file_name"]:
                    if key not in upload:
                        print(f">>> Error in {self.protocol} model: No '{key}' specified in the uploads"
                              f" config! upload: {upload}")
                        return False

        return True

    def generate(self) -> None:
        host = self.model_config["address"]
        port = self.model_config.get("port", 21)
        username = self.model_config["username"]
        password = self.model_config["password"]

        if self.model_config.get("simulate", False):
            self._simulate_ftp_operations()
            return

        downloads = self.model_config.get("downloads", [])
        uploads = self.model_config.get("uploads", [])
        browse_dirs = self.model_config.get("browse", [])

        ftp = None
        try:
            print(f">>> Connecting to {self.protocol} server: {host}:{port}")

            if self.__ssl:
                ftp = FTP_TLS(host=host, timeout=30)
                ftp.connect(host, port)
            else:
                ftp = FTP(host=host, timeout=30)
                ftp.connect(host, port)

            print(f">>> Connected to {host}. Logging in as {username}...")
            ftp.login(username, password)

            if self.__ssl:
                print(">>> Enabling secure data connection...")
                ftp.prot_p()

            print(f">>> Successfully logged in as {username}")

            welcome = ftp.getwelcome()
            print(f">>> Server welcome: {welcome}")

            try:
                system_info = ftp.sendcmd("SYST")
                print(f">>> Server system: {system_info}")
            except:
                pass

            if browse_dirs:
                self._browse_directories(ftp, browse_dirs)

            if downloads:
                self._download_files(ftp, downloads)

            if uploads:
                self._upload_files(ftp, uploads)

            print(f">>> Closing {self.protocol} connection...")
            ftp.quit()
            print(f">>> {self.protocol} session completed successfully")

        except all_errors as e:
            print(f">>> Error in {self.protocol} connection/operations:")
            print(f">>> {type(e).__name__}: {str(e)}")
        except Exception as e:
            print(f">>> Unexpected error in {self.protocol} model:")
            print(f">>> {type(e).__name__}: {str(e)}")
        finally:
            if ftp:
                try:
                    ftp.quit()
                except:
                    try:
                        ftp.close()
                    except:
                        pass

    def _browse_directories(self, ftp, browse_dirs):

        print(f"\n>>> Browsing {self.protocol} directories...")

        if not browse_dirs:
            browse_dirs = ["."]

        for dir_path in browse_dirs:
            try:
                print(f"\n>>> Changing to directory: {dir_path}")
                ftp.cwd(dir_path)

                print(f">>> Listing contents of: {dir_path}")
                file_list = []
                ftp.dir(file_list.append)

                if file_list:
                    print(">>> Directory contents:")
                    for item in file_list[:10]:
                        print(f">>>   {item}")
                    if len(file_list) > 10:
                        print(f">>>   ... and {len(file_list) - 10} more items")
                else:
                    print(">>> Directory is empty")

                try:
                    cwd = ftp.pwd()
                    print(f">>> Current directory: {cwd}")
                except:
                    pass

                time.sleep(random.uniform(1, 3))

            except all_errors as e:
                print(f">>> Error browsing directory {dir_path}: {e}")
                continue

    def _download_files(self, ftp, downloads):

        print(f"\n>>> Starting {self.protocol} downloads...")

        for download in downloads:
            try:
                remote_path = download["path"]
                output_dir = Path(download.get("output_dir", self.temp_dir))
                file_name = download["file_name"]

                os.makedirs(output_dir, exist_ok=True)

                print(f">>> Changing to directory: {remote_path}")
                ftp.cwd(remote_path)

                output_file = output_dir / file_name

                try:
                    file_size = ftp.size(file_name)
                    print(f">>> File size: {file_size} bytes")
                except:
                    print(">>> Could not determine file size")

                print(f">>> Downloading: {file_name} to {output_file}")
                start_time = time.time()

                with open(output_file, 'wb') as f:
                    ftp.retrbinary(f"RETR {file_name}", f.write)

                end_time = time.time()
                download_time = end_time - start_time
                file_size_mb = os.path.getsize(output_file) / (1024 * 1024)

                print(f">>> Download completed in {download_time:.2f} seconds")
                print(f">>> Downloaded {file_size_mb:.2f} MB")

                if download_time > 0:
                    speed = file_size_mb / download_time
                    print(f">>> Average download speed: {speed:.2f} MB/s")

                if "wait_after" in download:
                    wait_time = download["wait_after"]
                    print(f">>> Waiting {wait_time} seconds before next operation...")
                    time.sleep(wait_time)
                else:
                    time.sleep(random.uniform(1, 3))

            except all_errors as e:
                print(f">>> Error downloading {download.get('file_name')}: {e}")
                continue
            except Exception as e:
                print(f">>> Unexpected error during download: {e}")
                continue

    def _upload_files(self, ftp, uploads):

        print(f"\n>>> Starting {self.protocol} uploads...")

        for upload in uploads:
            try:
                remote_path = upload["path"]
                input_dir = Path(upload.get("input_dir", self.temp_dir))
                file_name = upload["file_name"]

                input_file = input_dir / file_name
                if not os.path.exists(input_file):
                    print(f">>> File {input_file} not found, creating a test file")
                    os.makedirs(input_dir, exist_ok=True)

                    with open(input_file, 'w') as f:
                        f.write(f"Test file created on {datetime.now()}\n")
                        f.write(f"This is a test file for FTP upload testing.\n")
                        for i in range(100):
                            f.write(f"Line {i}: {random.randint(1000, 9999)}\n")

                print(f">>> Changing to directory: {remote_path}")
                ftp.cwd(remote_path)

                print(f">>> Uploading: {input_file} to {remote_path}/{file_name}")
                start_time = time.time()

                with open(input_file, 'rb') as f:
                    ftp.storbinary(f"STOR {file_name}", f)

                end_time = time.time()
                upload_time = end_time - start_time
                file_size_mb = os.path.getsize(input_file) / (1024 * 1024)

                print(f">>> Upload completed in {upload_time:.2f} seconds")
                print(f">>> Uploaded {file_size_mb:.2f} MB")

                if upload_time > 0:
                    speed = file_size_mb / upload_time
                    print(f">>> Average upload speed: {speed:.2f} MB/s")

                if "wait_after" in upload:
                    wait_time = upload["wait_after"]
                    print(f">>> Waiting {wait_time} seconds before next operation...")
                    time.sleep(wait_time)
                else:
                    time.sleep(random.uniform(1, 3))

            except all_errors as e:
                print(f">>> Error uploading {upload.get('file_name')}: {e}")
                continue
            except Exception as e:
                print(f">>> Unexpected error during upload: {e}")
                continue

    def _simulate_ftp_operations(self):

        host = self.model_config["address"]
        port = self.model_config.get("port", 21)
        username = self.model_config["username"]

        print(f">>> [SIMULATION] Connecting to {self.protocol} server: {host}:{port}")
        print(f">>> [SIMULATION] Logging in as {username}...")
        print(f">>> [SIMULATION] Successfully logged in")
        print(f">>> [SIMULATION] Server welcome: Welcome to FTP service")

        if "browse" in self.model_config:
            browse_dirs = self.model_config["browse"]
            print(f"\n>>> [SIMULATION] Browsing directories: {browse_dirs}")

            for dir_path in browse_dirs:
                print(f">>> [SIMULATION] Changing to directory: {dir_path}")
                print(f">>> [SIMULATION] Listing contents of: {dir_path}")

                listing_count = random.randint(5, 15)
                print(f">>> [SIMULATION] Directory contains {listing_count} items")

                for i in range(min(listing_count, 5)):
                    item_type = random.choice(["d", "-"])
                    item_name = random.choice([
                        "documents", "images", "reports", "backup", "data", 
                        "file.txt", "image.jpg", "report.pdf", "data.csv", "config.xml"
                    ])
                    item_size = random.randint(1024, 1024*1024*10)
                    print(f">>> [SIMULATION] {item_type}rw-r--r--  1 user group {item_size:10d} Jan 01 2024 {item_name}")

                browse_time = random.uniform(1, 3)
                print(f">>> [SIMULATION] Browsing for {browse_time:.1f} seconds...")
                time.sleep(browse_time)

        if "downloads" in self.model_config:
            downloads = self.model_config["downloads"]
            print(f"\n>>> [SIMULATION] Starting downloads: {len(downloads)} files")

            for download in downloads:
                file_name = download["file_name"]
                output_dir = download.get("output_dir", self.temp_dir)
                remote_path = download["path"]

                print(f">>> [SIMULATION] Changing to directory: {remote_path}")
                print(f">>> [SIMULATION] Downloading: {file_name} to {output_dir}")

                file_size_mb = random.uniform(0.1, 50)
                download_speed = random.uniform(0.5, 10)
                download_time = file_size_mb / download_speed

                print(f">>> [SIMULATION] File size: {file_size_mb:.2f} MB")
                print(f">>> [SIMULATION] Downloading at {download_speed:.2f} MB/s")
                print(f">>> [SIMULATION] Estimated time: {download_time:.2f} seconds")

                time.sleep(min(download_time, 5))

                print(f">>> [SIMULATION] Download completed")

                if "wait_after" in download:
                    wait_time = min(download["wait_after"], 3)
                    print(f">>> [SIMULATION] Waiting {wait_time} seconds...")
                    time.sleep(wait_time)

        if "uploads" in self.model_config:
            uploads = self.model_config["uploads"]
            print(f"\n>>> [SIMULATION] Starting uploads: {len(uploads)} files")

            for upload in uploads:
                file_name = upload["file_name"]
                input_dir = upload.get("input_dir", self.temp_dir)
                remote_path = upload["path"]

                print(f">>> [SIMULATION] Changing to directory: {remote_path}")
                print(f">>> [SIMULATION] Uploading: {input_dir}/{file_name} to {remote_path}")

                file_size_mb = random.uniform(0.1, 20)
                upload_speed = random.uniform(0.2, 5)
                upload_time = file_size_mb / upload_speed

                print(f">>> [SIMULATION] File size: {file_size_mb:.2f} MB")
                print(f">>> [SIMULATION] Uploading at {upload_speed:.2f} MB/s")
                print(f">>> [SIMULATION] Estimated time: {upload_time:.2f} seconds")

                time.sleep(min(upload_time, 5))

                print(f">>> [SIMULATION] Upload completed")

                if "wait_after" in upload:
                    wait_time = min(upload["wait_after"], 3)
                    print(f">>> [SIMULATION] Waiting {wait_time} seconds...")
                    time.sleep(wait_time)

        print(f"\n>>> [SIMULATION] Closing {self.protocol} connection")
        print(f">>> [SIMULATION] {self.protocol} session completed successfully")
