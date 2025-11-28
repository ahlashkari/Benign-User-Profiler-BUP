#!/usr/bin/env python3

import time
import random
import os
import tempfile
import requests
import paramiko
import subprocess
from pathlib import Path
from datetime import datetime
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from .base_browser import BaseBrowserModule

class CustomServiceModule(BaseBrowserModule):
    def __init__(self, headless=False):
        super().__init__(headless)
        self.temp_dir = tempfile.mkdtemp()
        self.generated_files = []
        self.downloaded_files = []

    def execute(self, config):
        try:
            base_url = config.get("custom_service_url", "http://192.168.1.55")
            username = config.get("scp_username", "capwifi")
            password = config.get("scp_password", "bccc1234")
            scp_host = config.get("scp_host", "192.68.1.55")
            upload_path = config.get("scp_upload_path", "~/file-server-uploads")

            self._generate_txt_files(3)

            print(f">>> Visiting custom service: {base_url}")

            additional_args = ["-new-tab"] if self.os_type == "Linux" else []
            if not self.browser_command(base_url, additional_args):
                print(">>> Failed to open the main page")
                return False

            print(">>> Successfully opened main page, scrolling...")
            time.sleep(random.uniform(3, 5))

            scroll_count = random.randint(3, 6)
            for i in range(scroll_count):
                print(f">>> Scrolling down ({i+1}/{scroll_count})")
                self.scroll_down(1)
                time.sleep(random.uniform(2, 4))

            guide_url = urljoin(base_url, "/guide")
            print(f">>> Visiting guide: {guide_url}")

            additional_args = ["-new-tab"] if self.os_type == "Linux" else []
            if not self.browser_command(guide_url, additional_args):
                print(">>> Failed to open guide page")
                self.close_browser()
                return False

            print(">>> Successfully opened guide page, scrolling...")
            time.sleep(random.uniform(3, 5))

            scroll_count = random.randint(4, 7)
            for i in range(scroll_count):
                print(f">>> Scrolling down guide page ({i+1}/{scroll_count})")
                self.scroll_down(1)
                time.sleep(random.uniform(2, 4))

            print("\n" + "="*50)
            print(">>> STARTING API FILE UPLOAD")
            print("="*50)
            upload_result = self._upload_file_to_api(base_url)
            if upload_result:
                print(">>> API UPLOAD COMPLETED SUCCESSFULLY")
            else:
                print(">>> API UPLOAD FAILED")
            print("="*50 + "\n")
            time.sleep(random.uniform(3, 5))

            print(f">>> Visiting main page again: {base_url}")
            additional_args = ["-new-tab"] if self.os_type == "Linux" else []
            if not self.browser_command(base_url, additional_args):
                print(">>> Failed to return to main page")
                self.close_browser()
                return False

            print(">>> Successfully returned to main page")
            time.sleep(random.uniform(3, 5))

            report_url = urljoin(base_url, "/report")
            print(f">>> Visiting report page to download: {report_url}")

            additional_args = ["-new-tab"] if self.os_type == "Linux" else []
            if not self.browser_command(report_url, additional_args):
                print(">>> Failed to access report page")
                self.close_browser()
                return False

            print(">>> Report download should be initiated automatically")
            download_time = random.uniform(2, 5)
            print(f">>> Waiting {download_time:.1f} seconds for download to complete...")
            time.sleep(download_time)

            files_url = urljoin(base_url, "/files")
            print(f">>> Visiting files page: {files_url}")

            additional_args = ["-new-tab"] if self.os_type == "Linux" else []
            if not self.browser_command(files_url, additional_args):
                print(">>> Failed to access files page")
                self.close_browser()
                return False

            print(">>> Successfully opened files page")
            time.sleep(random.uniform(3, 5))

            scroll_count = random.randint(2, 4)
            for i in range(scroll_count):
                print(f">>> Scrolling files page ({i+1}/{scroll_count})")
                self.scroll_down(1)
                time.sleep(random.uniform(2, 4))

            print(">>> Parsing HTML to find download links")
            try:
                response = requests.get(files_url)
                soup = BeautifulSoup(response.text, 'html.parser')

                download_links = soup.find_all('a', class_='download-link')

                if not download_links:
                    download_links = soup.find_all('a', href=True)
                    print(f">>> No specific download-link class found, using all {len(download_links)} links")
                else:
                    print(f">>> Found {len(download_links)} download links with class='download-link'")

                download_paths = [link['href'] for link in download_links if 'href' in link.attrs]

                if len(download_paths) == 0:
                    print(">>> No download links found in page HTML")
                    all_links = soup.find_all('a', href=True)
                    download_paths = [link['href'] for link in all_links if '.' in link['href']]
                    print(f">>> Fallback: found {len(download_paths)} potential file links")

                print(f">>> Found these download paths: {download_paths[:5]}")

                download_paths_to_use = random.sample(download_paths, min(3, len(download_paths))) if download_paths else []

            except Exception as e:
                print(f">>> Error parsing HTML: {e}")
                print(">>> Using fallback download paths")
                download_paths_to_use = [
                    f"/downloads/file_{random.randint(1000, 9999)}.txt",
                    f"/downloads/file_{random.randint(1000, 9999)}.pdf"
                ]

            for download_path in download_paths_to_use:
                download_url = urljoin(base_url, download_path)
                file_name = os.path.basename(download_path)

                print(f">>> Downloading file: {file_name} from {download_url}")

                additional_args = ["-new-tab"] if self.os_type == "Linux" else []
                if not self.browser_command(download_url, additional_args):
                    print(f">>> Failed to download {file_name}")
                    continue

                print(f">>> Download initiated for {file_name}")
                download_time = random.uniform(2, 6)
                print(f">>> Waiting {download_time:.1f} seconds for download...")
                time.sleep(download_time)

                time.sleep(random.uniform(5, 10))

            print("\n" + "="*50)
            print(">>> STARTING SCP FILE UPLOAD")
            print(f">>> Host: {scp_host}, Username: {username}, Path: {upload_path}")
            print("="*50)
            scp_result = self._upload_to_scp_server(scp_host, username, password, upload_path)
            if scp_result:
                print(">>> SCP UPLOAD COMPLETED SUCCESSFULLY")
            else:
                print(">>> SCP UPLOAD FAILED")
            print("="*50 + "\n")

            print(">>> Closing browser")
            self.close_browser()
            return True

        except Exception as e:
            print(f">>> Error in CustomServiceModule: {e}")
            self.close_browser()
            return False

    def _generate_txt_files(self, count=3):

        print(f">>> Generating {count} random text files")

        for i in range(count):
            file_path = os.path.join(self.temp_dir, f"upload_file_{i}.txt")

            content_types = [
                "System monitoring log data",
                "Application configuration settings",
                "Test results from automated testing",
                "Network scan results",
                "Service status report"
            ]

            try:
                with open(file_path, 'w') as f:
                    f.write(f"Test file created at {datetime.now()}\n")
                    f.write(f"Purpose: {random.choice(content_types)}\n")
                    f.write(f"File ID: {random.randint(10000, 99999)}\n")
                    f.write("-" * 40 + "\n\n")

                    for j in range(random.randint(30, 100)):
                        f.write(f"Line {j}: Data entry at timestamp {time.time()} with value {random.random():.6f}\n")

                self.generated_files.append(file_path)
                print(f">>> Created file: {file_path}")

            except Exception as e:
                print(f">>> Error generating file: {e}")

        return self.generated_files

    def _upload_file_to_api(self, base_url):

        if not self.generated_files:
            print(">>> No files available for upload")
            return False

        upload_url = urljoin(base_url, "/api/upload")
        file_to_upload = random.choice(self.generated_files)

        print(f">>> POST API Upload: {file_to_upload} -> {upload_url}")
        print(f">>> File size: {os.path.getsize(file_to_upload)} bytes")

        try:
            if not os.path.exists(file_to_upload):
                print(f">>> Error: File {file_to_upload} does not exist")
                return False

            with open(file_to_upload, 'rb') as f:
                files = {'file': (os.path.basename(file_to_upload), f, 'text/plain')}

                headers = {
                    'User-Agent': random.choice(self.user_agents),
                }

                print(f">>> Sending POST request with file '{os.path.basename(file_to_upload)}'")
                print(f">>> Parameter name: 'file'")

                start_time = time.time()
                response = requests.post(
                    url=upload_url,
                    files=files,
                    headers=headers,
                    timeout=30
                )
                end_time = time.time()
                upload_time = end_time - start_time

                print(f">>> Upload took {upload_time:.2f} seconds")
                print(f">>> Response status code: {response.status_code}")
                print(f">>> Response headers: {response.headers}")

                if response.status_code == 200 or response.status_code == 201:
                    print(f">>> File upload successful via POST")
                    try:
                        print(f">>> Response content: {response.text[:200]}")
                    except:
                        print(">>> Could not display response content")
                    return True
                else:
                    print(f">>> File upload failed, status code: {response.status_code}")
                    print(f">>> Response: {response.text[:200]}")

                    print(">>> Trying alternative parameter name 'file'")
                    with open(file_to_upload, 'rb') as f2:
                        alt_files = {'file': (os.path.basename(file_to_upload), f2, 'text/plain')}
                        alt_response = requests.post(upload_url, files=alt_files, headers=headers)

                        if alt_response.status_code == 200 or alt_response.status_code == 201:
                            print(f">>> Alternate upload successful, status code: {alt_response.status_code}")
                            return True

                    return False

        except Exception as e:
            print(f">>> Error uploading file: {e}")
            return False

    def _upload_to_scp_server(self, host, username, password, remote_path):

        if not self.generated_files:
            print(">>> No files available for SCP upload")
            return False

        file_to_upload = random.choice(self.generated_files)

        print(f">>> Preparing to upload file to SCP server: {host}")
        print(f">>> Username: {username}, Remote path: {remote_path}")

        try:
            password_file = os.path.join(self.temp_dir, "scp_password.txt")
            with open(password_file, 'w') as f:
                f.write(password)
            os.chmod(password_file, 0o600)

            destination = f"{username}@{host}:{remote_path}"

            try:
                print(f">>> Attempting SCP upload with sshpass: {file_to_upload} -> {destination}")
                command = f"sshpass -f {password_file} scp -o StrictHostKeyChecking=no {file_to_upload} {destination}"

                print(f">>> Running command: {command}")
                start_time = time.time()

                process = subprocess.Popen(
                    command,
                    shell=True,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True
                )

                stdout, stderr = process.communicate(timeout=30)

                end_time = time.time()
                upload_time = end_time - start_time
                file_size_mb = os.path.getsize(file_to_upload) / (1024 * 1024)

                if process.returncode == 0:
                    print(f">>> Upload completed successfully in {upload_time:.2f} seconds")
                    print(f">>> Uploaded {file_size_mb:.2f} MB")

                    if upload_time > 0:
                        speed = file_size_mb / upload_time
                        print(f">>> Average upload speed: {speed:.2f} MB/s")
                else:
                    print(f">>> Upload failed with code {process.returncode}")
                    if stdout:
                        print(f">>> Command output: {stdout}")
                    if stderr:
                        print(f">>> Command error: {stderr}")
                    raise Exception(f"SCP command failed with code {process.returncode}")

            except (subprocess.SubprocessError, FileNotFoundError) as e:
                print(f">>> Error with sshpass approach: {e}")
                print(">>> Falling back to expect script method")

                expect_script = os.path.join(self.temp_dir, "scp_expect.exp")
                with open(expect_script, 'w') as f:
                    f.write(f'''#!/usr/bin/expect -f
                    set timeout 30
                    spawn scp -o StrictHostKeyChecking=no {file_to_upload} {destination}
                    expect "password:" {{ send "{password}\\r" }}
                    expect eof
                    ''')
                os.chmod(expect_script, 0o700)

                print(f">>> Running expect script for SCP upload")
                process = subprocess.run(
                    expect_script,
                    shell=True,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True
                )

                if process.returncode == 0:
                    print(">>> Upload completed successfully with expect script")
                else:
                    print(f">>> Upload with expect script failed: {process.stderr}")
                    raise Exception("SCP with expect script failed")

            try:
                os.remove(password_file)
                if os.path.exists(expect_script):
                    os.remove(expect_script)
            except Exception as e:
                print(f">>> Warning: Could not clean up temporary files: {e}")

            return True

        except Exception as e:
            print(f">>> Error during SCP upload: {e}")
            return False