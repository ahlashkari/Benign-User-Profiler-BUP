#!/usr/bin/env python3

import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from .traffic_model import TrafficModel


class HTTPModel(TrafficModel):
    def __init__(self, model_config: dict, driver: object):
        # TODO: verify the model config: e.g. type, link, browser are mandatory
        self.__model_config = model_config
        self.firefox_driver = None
        if isinstance(driver, webdriver.firefox.webdriver.WebDriver):
            self.firefox_driver = driver

    def generate(self) -> None:
        # TODO: check using enum instead
        # TODO: add frequency, start_time, and time_interval
        # TODO: add headless option
        # TODO: add other browsers
        # TODO: use try catch
        # TODO: add installation script (containig installation for browsers drivers)
        if self.__model_config["browser"] == "firefox":
            self.__generate_with_firefox()
        else:
            print(f">>>> Error occured: Not a supported browser '{self.__model_config['browser']}'")

    def __generate_with_firefox(self):
        self.firefox_driver.execute_script("window.open('');")
        windows = self.firefox_driver.window_handles
        self.firefox_driver.switch_to.window(windows[-1])
        self.firefox_driver.get(self.__model_config["link"])
        if "clicks" in self.__model_config:
            for click in self.__model_config["clicks"]:
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
                    print(f">>>> Error occured: Not supported type '{click['type']}'")

                if "wait_after" in click:
                    # TODO: replace it with 'WebDriverWait'
                    time.sleep(click["wait_after"])
#        self.firefox_driver.quit()
