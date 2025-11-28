#!/usr/bin/env python3

import time
import random
import os
import requests
import subprocess
from .base_browser import BaseBrowserModule

class ImageDownloadModule(BaseBrowserModule):
    def execute(self, config):
        if "download_urls" in config:
            return self._download_from_urls(config)

        download_sources = config.get("download_sources", [
            "https://www.pexels.com",
            "https://pixabay.com",
            "https://unsplash.com"
        ])

        source = random.choice(download_sources)

        search_terms = config.get("download_search_terms", 
                              ["nature", "city", "technology", "business"])
        search_term = random.choice(search_terms)

        output_dir = os.path.expanduser("~/output-benign/image_downloads")
        os.makedirs(output_dir, exist_ok=True)

        try:
            print(f">>> Attempting direct download of {search_term} image from {source}")

            if "unsplash.com" in source:
                api_url = f"https://api.unsplash.com/search/photos?query={search_term}&per_page=10"
                headers = {"Authorization": "Client-ID 8bJR5zKvpU6oZ5L6z5bM-qRcpDL88JvugPJ-87x3Mjg"}

                response = requests.get(api_url, headers=headers)
                if response.status_code == 200:
                    data = response.json()
                    if data["results"]:
                        image = random.choice(data["results"])
                        image_url = image["urls"]["regular"]

                        img_response = requests.get(image_url, stream=True)
                        if img_response.status_code == 200:
                            filename = f"unsplash_{int(time.time())}.jpg"
                            file_path = os.path.join(output_dir, filename)

                            with open(file_path, 'wb') as f:
                                for chunk in img_response.iter_content(1024):
                                    f.write(chunk)

                            print(f">>> Successfully downloaded image to {file_path}")
                            return True

            elif "pexels.com" in source:
                api_url = f"https://api.pexels.com/v1/search?query={search_term}&per_page=20"
                headers = {"Authorization": "563492ad6f91700001000001b76a00743e3a43918c9dbd7a12d95a71"}

                response = requests.get(api_url, headers=headers)
                if response.status_code == 200:
                    data = response.json()
                    if data["photos"]:
                        photo = random.choice(data["photos"])
                        image_url = photo["src"]["medium"]

                        img_response = requests.get(image_url, stream=True)
                        if img_response.status_code == 200:
                            filename = f"pexels_{int(time.time())}.jpg"
                            file_path = os.path.join(output_dir, filename)

                            with open(file_path, 'wb') as f:
                                for chunk in img_response.iter_content(1024):
                                    f.write(chunk)

                            print(f">>> Successfully downloaded image to {file_path}")
                            return True

            elif "pixabay.com" in source:
                api_url = f"https://pixabay.com/api/?key=34249090-a56e0bf4b095a0e31ee5627ea&q={search_term}&image_type=photo&per_page=10"

                response = requests.get(api_url)
                if response.status_code == 200:
                    data = response.json()
                    if data["hits"]:
                        image = random.choice(data["hits"])
                        image_url = image["webformatURL"]

                        img_response = requests.get(image_url, stream=True)
                        if img_response.status_code == 200:
                            filename = f"pixabay_{int(time.time())}.jpg"
                            file_path = os.path.join(output_dir, filename)

                            with open(file_path, 'wb') as f:
                                for chunk in img_response.iter_content(1024):
                                    f.write(chunk)

                            print(f">>> Successfully downloaded image to {file_path}")
                            return True

            print(">>> Direct download failed, falling back to browser method")
        except Exception as e:
            print(f">>> Error with direct download: {e}")
            print(">>> Falling back to browser method")

        search_url = None
        if "unsplash.com" in source:
            search_url = f"https://unsplash.com/s/photos/{search_term.replace(' ', '-')}"
        elif "pexels.com" in source:
            search_url = f"https://www.pexels.com/search/{search_term.replace(' ', '%20')}/"
        elif "pixabay.com" in source:
            search_url = f"https://pixabay.com/images/search/{search_term.replace(' ', '%20')}/"
        else:
            search_url = source

        if not self.browser_command(search_url):
            print(">>> Failed to launch browser for image download")
            return False

        print(f">>> Browsing {source} for media")
        print(f">>> Searching for: {search_term}")

        time.sleep(random.uniform(3, 6))

        scroll_count = random.randint(2, 5)
        print(f">>> Scrolling through search results ({scroll_count} scrolls)")
        self.scroll_down(scroll_count)

        print(">>> Selecting an image to view")
        image_positions = [
            (500, 500),
            (400, 450),
            (600, 450),
            (400, 650),
            (600, 650)
        ]
        pos = random.choice(image_positions)
        self.click(pos[0], pos[1])

        time.sleep(random.uniform(3, 8))
        print(">>> Looking at details for a selected image")
        time.sleep(random.uniform(5, 10))

        print(">>> Attempting to download the image using right-click")
        self.right_click(500, 500)
        time.sleep(1)

        print(">>> Pressing down arrow key twice")
        self.press_key("Down")
        time.sleep(0.2)
        self.press_key("Down")
        time.sleep(0.2)

        self.press_key("Return")
        time.sleep(2)

        filename = f"image_{int(time.time())}.jpg"
        file_path = os.path.join(output_dir, filename)

        time.sleep(1)
        if self.os_type == "Linux":
            subprocess.run(["xdotool", "type", file_path], 
                         check=False,
                         stdout=subprocess.DEVNULL, 
                         stderr=subprocess.DEVNULL)
            time.sleep(1)

            subprocess.run(["xdotool", "key", "Return"], 
                         check=False,
                         stdout=subprocess.DEVNULL, 
                         stderr=subprocess.DEVNULL)
        elif self.os_type == "Windows":
            ps_script = f'''
            Add-Type -AssemblyName System.Windows.Forms
            [System.Windows.Forms.SendKeys]::SendWait("{file_path}")
            Start-Sleep -Seconds 1
            [System.Windows.Forms.SendKeys]::SendWait("{{ENTER}}")
            '''
            subprocess.run(["powershell", "-Command", ps_script], 
                         shell=True,
                         stdout=subprocess.DEVNULL, 
                         stderr=subprocess.DEVNULL)

        download_time = random.uniform(2, 5)
        print(f">>> Waiting {download_time:.1f} seconds for download to complete")
        time.sleep(download_time)

        print(f">>> Image saved to: {file_path}")

        self.close_browser()
        return True

    def _download_from_urls(self, config):

        download_urls = config.get("download_urls", [])
        if not download_urls:
            print(">>> No download URLs provided")
            return False

        output_dir = os.path.expanduser("~/output-benign/media_downloads")
        os.makedirs(output_dir, exist_ok=True)

        print(f">>> Found {len(download_urls)} URLs to download")
        successful_downloads = 0

        for i, url in enumerate(download_urls):
            try:
                print(f">>> Downloading file {i+1}/{len(download_urls)}: {url}")

                filename = os.path.basename(url)
                if not filename or "?" in filename or len(filename) < 4:
                    if ".jpg" in url.lower() or ".jpeg" in url.lower():
                        ext = ".jpg"
                    elif ".png" in url.lower():
                        ext = ".png"
                    elif ".gif" in url.lower():
                        ext = ".gif"
                    elif ".mp4" in url.lower() or ".mov" in url.lower():
                        ext = ".mp4"
                    elif ".mp3" in url.lower() or ".wav" in url.lower():
                        ext = ".mp3"
                    elif ".pdf" in url.lower():
                        ext = ".pdf"
                    else:
                        ext = ".bin"

                    filename = f"download_{int(time.time())}_{i}{ext}"

                file_path = os.path.join(output_dir, filename)

                response = requests.get(url, stream=True)
                if response.status_code == 200:
                    total_size = int(response.headers.get('content-length', 0))
                    downloaded = 0

                    with open(file_path, 'wb') as f:
                        start_time = time.time()
                        for chunk in response.iter_content(chunk_size=8192):
                            if chunk:
                                f.write(chunk)
                                downloaded += len(chunk)

                                if total_size > 0 and downloaded % 524288 == 0:
                                    percent = (downloaded / total_size) * 100
                                    elapsed = time.time() - start_time
                                    if elapsed > 0:
                                        speed = downloaded / (1024 * elapsed)
                                        print(f">>> Progress: {percent:.1f}% ({downloaded/1024/1024:.1f} MB) - {speed:.1f} KB/s")

                    download_time = time.time() - start_time
                    print(f">>> Successfully downloaded {filename} ({os.path.getsize(file_path)/1024/1024:.2f} MB in {download_time:.1f} seconds)")
                    successful_downloads += 1

                    time.sleep(random.uniform(1, 3))
                else:
                    print(f">>> Failed to download: HTTP {response.status_code}")

                if i < len(download_urls) - 1:
                    wait_time = random.uniform(2, 5)
                    print(f">>> Waiting {wait_time:.1f} seconds before next download...")
                    time.sleep(wait_time)

            except Exception as e:
                print(f">>> Error downloading {url}: {e}")

        print(f">>> Media download complete. Successfully downloaded {successful_downloads}/{len(download_urls)} files to {output_dir}")
        return True