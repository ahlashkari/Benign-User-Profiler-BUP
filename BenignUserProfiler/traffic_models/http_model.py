#!/usr/bin/env python3

import time
import random
import platform
import subprocess
import os
import requests
import tempfile
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin
from datetime import datetime
from .traffic_model import TrafficModel
from ..web_modules import get_module

class HTTPModel(TrafficModel):
    def __init__(self, browser_type=None, driver=None, headless=False):
        super().__init__()
        self.user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.5 Safari/605.1.15",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/114.0",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:109.0) Gecko/20100101 Firefox/113.0"
        ]
        self.download_dir = tempfile.mkdtemp()
        self.visited_urls = set()
        self.use_real_browser = False
        self.driver = None
        self.headless = headless
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': random.choice(self.user_agents),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1'
        })

    def __str__(self):
        return "HTTP/S"

    def generate(self) -> None:
        if not self._is_within_work_hours():
            print(">>> Current time is outside work hours. Skipping task.")
            return

        try:    
            if "website" in self.model_config:
                website = self.model_config["website"].lower()

                if website == "youtube":
                    module = get_module("youtube", self.headless)
                    module.execute(self.model_config)
                elif website == "download":
                    module = get_module("download", self.headless)
                    module.execute(self.model_config)
                elif website == "soundcloud":
                    module = get_module("soundcloud", self.headless)
                    module.execute(self.model_config)
                elif website == "google":
                    module = get_module("web", self.headless)
                    self.model_config["website"] = "https://www.google.com"
                    module.execute(self.model_config)
                elif website == "firefox_search":
                    module = get_module("firefox_search", self.headless)
                    module.execute(self.model_config)
                elif website == "custom_service":
                    module = get_module("custom_service", self.headless)
                    module.execute(self.model_config)
                else:
                    module = get_module("web", self.headless)
                    module.execute(self.model_config)
            elif "websites" in self.model_config:
                websites = self.model_config["websites"]
                if self.model_config.get("randomize", False):
                    random.shuffle(websites)

                for website in websites:
                    if isinstance(website, dict):
                        site_type = website.get("type", "").lower()
                        if site_type == "youtube":
                            module = get_module("youtube", self.headless)
                            module.execute(self.model_config)
                        elif site_type == "download":
                            module = get_module("download", self.headless)
                            module.execute(self.model_config)
                        elif site_type == "soundcloud":
                            module = get_module("soundcloud", self.headless)
                            module.execute(self.model_config)
                        elif site_type == "google":
                            module = get_module("web", self.headless)
                            self.model_config["website"] = "https://www.google.com"
                            module.execute(self.model_config)
                        elif site_type == "firefox_search":
                            module = get_module("firefox_search", self.headless)
                            module.execute(self.model_config)
                        elif site_type == "custom_service":
                            module = get_module("custom_service", self.headless)
                            module.execute(self.model_config)
                        else:
                            module = get_module("web", self.headless)
                            self.model_config["website"] = website.get("url")
                            module.execute(self.model_config)
                    else:
                        module = get_module("web", self.headless)
                        self.model_config["website"] = website
                        module.execute(self.model_config)

                    rest_time = random.randint(5, 10)
                    print(f">>> Taking a break for {rest_time} minutes before next website")
                    time.sleep(rest_time * 60)
            elif "link" in self.model_config:
                module = get_module("web", self.headless)
                self.model_config["website"] = self.model_config["link"]
                module.execute(self.model_config)
        except Exception as e:
            print(f">>> Error in HTTP model execution: {e}")

    def verify(self) -> bool:
        if not (("website" in self.model_config) or 
                ("websites" in self.model_config) or 
                ("link" in self.model_config)):
            print(">>> Error in HTTP/S model: No website to visit specified in the config!")
            return False
        return True

    def _is_within_work_hours(self):
        if "work_hours" not in self.model_config:
            return True

        now = datetime.now().time()
        start_time_str = self.model_config["work_hours"].get("start", "09:00")
        end_time_str = self.model_config["work_hours"].get("end", "17:00")

        try:
            start_time = datetime.strptime(start_time_str, "%H:%M").time()
            end_time = datetime.strptime(end_time_str, "%H:%M").time()

            if start_time <= now <= end_time:
                return True
            return False
        except Exception as e:
            print(f">>> Error parsing work hours: {e}")
            return True