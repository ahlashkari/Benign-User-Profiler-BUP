#!/usr/bin/env python3

import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from .traffic_model import TrafficModel


class HTTPModel(TrafficModel):
    def __init__(self, driver: object):
        self.firefox_driver = None
        if isinstance(driver, webdriver.firefox.webdriver.WebDriver):
            self.firefox_driver = driver

    def __str__(self):
        return "HTTP/S"

    def generate(self) -> None:
        if self.model_config["browser"].lower() == "firefox":
            self.__generate_with_firefox()
        else:
            print(f">>> Error occured in HTTP/S model: Not a supported browser "
                  f"'{self.model_config['browser']}'")

    def verify(self) -> bool:
        for key in ["browser", "link"]:
            if key not in self.model_config:
                print(f">>> Error in HTTP/S model: No '{key}' specified in the config!")
                return False
        return True

    def __generate_with_firefox(self):
        try:
            self.firefox_driver.execute_script("window.open('');")
            windows = self.firefox_driver.window_handles
            self.firefox_driver.switch_to.window(windows[-1])
            self.firefox_driver.get(self.model_config["link"])
        except Exception as e:
            print(f">>> Error in HTTP/S model.")
            print(e)
            return

        if "clicks" in self.model_config:
            for click in self.model_config["clicks"]:
                try:
                    if click["type"] == "link":
                        element = self.firefox_driver.find_element(
                                by=By.LINK_TEXT, value=click["value"])
                        element.click()

                    elif click["type"] == "text_form":
                        element = self.firefox_driver.find_element(By.NAME, click["name"])
                        element.send_keys(click["value"])

                    elif click["type"] == "submit_by_path":
                        element = self.firefox_driver.find_element(By.XPATH, click["value"])
                        element.submit()

                    elif click["type"] == "scroll_down":
                        self.firefox_driver.execute_script("return document.body.scrollHeight")
                        self.firefox_driver.execute_script(
                                "window.scrollTo(0, document.body.scrollHeight);")

                    elif click["type"] == "next_tab":
                        self.firefox_driver.find_element_by_tag_name('body').send_keys(
                                Keys.CONTROL + Keys.TAB)
                        windows = self.firefox_driver.window_handles
                        self.firefox_driver.switch_to.window(windows[-1])

                    else:
                        print(f">>> Error occured in HTTP/S model: "
                              f"Not supported type '{click['type']}'")

                    if "wait_after" in click:
                        time.sleep(click["wait_after"])
                except Exception as e:
                    print(">>> Exception occurred in HTTP/S model:")
                    print(e)
                    continue