#!/usr/bin/env python3

import time
import random
from .base_browser import BaseBrowserModule

class FirefoxSearchModule(BaseBrowserModule):
    def __init__(self, headless=False):
        super().__init__(headless)

    def execute(self, config):
        search_terms = config.get("firefox_search_terms", ["latest news", "weather today"])
        search_term = random.choice(search_terms)

        start_url = "about:blank"

        print(f">>> Starting Firefox for header bar search: {start_url}")
        if not self.browser_command(start_url):
            print(">>> Failed to launch browser")
            return False

        time.sleep(random.uniform(3, 5))

        search_bar_positions = [
            (500, 40),
            (600, 40),
            (400, 40)
        ]

        print(f">>> Will search for: {search_term} using Firefox search bar")

        for pos in search_bar_positions:
            print(f">>> Clicking Firefox search bar at position {pos}")
            try:
                import pyautogui
                screen_width, screen_height = pyautogui.size()
                scaled_x = int(pos[0] * screen_width / 1000)
                scaled_y = int(pos[1] * screen_height / 800)
                pyautogui.click(scaled_x, scaled_y)
            except ImportError:
                self.click(pos[0], pos[1])
            time.sleep(1.0)

        print(f">>> Typing search term in Firefox bar: {search_term}")
        try:
            import pyautogui
            pyautogui.hotkey('ctrl', 'a')
            time.sleep(0.5)
            pyautogui.press('delete')
            time.sleep(0.5)

            pyautogui.write(search_term)
            time.sleep(0.5)
            pyautogui.press('enter')
        except ImportError:
            self.press_key("ctrl+a")
            time.sleep(0.5)
            self.press_key("Delete")
            time.sleep(0.5)

            self.keyboard_input(search_term)

        print(">>> Waiting for search results to load")
        time.sleep(random.uniform(3, 6))

        scroll_count = random.randint(2, 5)
        for i in range(scroll_count):
            print(f">>> Scrolling through search results ({i+1}/{scroll_count})")
            self.scroll_down(1)
            time.sleep(random.uniform(2, 4))

        if config.get("click_results", True):
            results_to_visit = random.randint(
                config.get("min_results_to_visit", 1),
                config.get("max_results_to_visit", 3)
            )

            print(f">>> Will visit {results_to_visit} search results")

            for i in range(results_to_visit):
                y_pos = 250 + (i * 100)
                x_pos = 400 + random.randint(-50, 50)

                print(f">>> Clicking on search result {i+1} at position ({x_pos}, {y_pos})")
                self.click(x_pos, y_pos)

                load_time = random.uniform(4, 8)
                print(f">>> Waiting {load_time:.1f} seconds for page to load")
                time.sleep(load_time)

                result_browse_time = random.uniform(10, 30)
                print(f">>> Browsing result for {result_browse_time:.0f} seconds")

                result_scrolls = random.randint(1, 4)
                for j in range(result_scrolls):
                    self.scroll_down(1)
                    time.sleep(random.uniform(2, 5))

                print(">>> Going back to search results")
                self.press_key("alt+Left")
                time.sleep(random.uniform(2, 4))

        print(">>> Closing browser")
        self.close_browser()
        return True