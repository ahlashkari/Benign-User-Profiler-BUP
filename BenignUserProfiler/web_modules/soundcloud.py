#!/usr/bin/env python3

import time
import random
import subprocess
import os
from .base_browser import BaseBrowserModule

class SoundcloudModule(BaseBrowserModule):
    def execute(self, config):
        soundcloud_url = "https://soundcloud.com"

        if not self.browser_command(soundcloud_url):
            print(">>> Failed to launch browser for SoundCloud")
            return False

        print(f">>> Browsing SoundCloud: {soundcloud_url}")
        time.sleep(random.uniform(5, 10))

        if "soundcloud_searches" in config:
            search_term = random.choice(config["soundcloud_searches"])
            print(f">>> Searching for music: {search_term}")

            search_method = random.choice(["direct_url", "interactive"])

            if search_method == "direct_url":
                search_url = f"https://soundcloud.com/search?q={search_term.replace(' ', '%20')}"
                print(f">>> Using direct URL search: {search_url}")
                self.browser_command(search_url)
            else:
                print(">>> Using interactive search method")
                self.browser_command(soundcloud_url)
                time.sleep(random.uniform(3, 5))

                time.sleep(random.uniform(3, 5))

                try:
                    import pyautogui
                    screen_width, screen_height = pyautogui.size()

                    search_positions = [
                        (screen_width // 2, 150),
                        (screen_width * 0.7, 150),
                        (screen_width * 0.8, 150),
                        (screen_width * 0.3, 150),
                        (screen_width * 0.5, 200)
                    ]

                    print(">>> Clicking on SoundCloud's search box (avoiding browser search bar)")

                    for pos in search_positions:
                        print(f">>> Clicking SoundCloud search box at {pos}")
                        pyautogui.click(pos[0], pos[1])
                        time.sleep(1.0)

                        pyautogui.write(search_term)
                        time.sleep(0.5)
                        pyautogui.press('enter')
                        time.sleep(1.0)
                except ImportError:
                    search_positions = [(500, 150), (600, 150), (400, 150), (500, 200)]

                    print(">>> Clicking on SoundCloud's search box (avoiding browser search bar)")
                    for pos in search_positions:
                        print(f">>> Clicking SoundCloud search box at {pos}")
                        self.click(pos[0], pos[1])
                        time.sleep(1.0)

                        for char in search_term:
                            self.press_key(char)
                            time.sleep(0.05)
                        self.press_key("Return")
                        time.sleep(1.0)

            time.sleep(random.uniform(5, 10))

            print(">>> Selecting a track from search results")

            selection_areas = [
                {"area": {"x_min": 400, "x_max": 800, "y_min": 250, "y_max": 350}, "weight": 0.5},
                {"area": {"x_min": 400, "x_max": 800, "y_min": 350, "y_max": 450}, "weight": 0.3},
                {"area": {"x_min": 400, "x_max": 800, "y_min": 450, "y_max": 550}, "weight": 0.1},
                {"area": {"x_min": 400, "x_max": 800, "y_min": 550, "y_max": 650}, "weight": 0.1}
            ]

            weights = [area["weight"] for area in selection_areas]
            chosen_area = random.choices(selection_areas, weights=weights, k=1)[0]["area"]

            try:
                import pyautogui
                screen_width, screen_height = pyautogui.size()

                x_min = int(chosen_area["x_min"] * screen_width / 1920)
                x_max = int(chosen_area["x_max"] * screen_width / 1920)
                y_min = chosen_area["y_min"]
                y_max = chosen_area["y_max"]

                x = random.randint(x_min, x_max)
                y = random.randint(y_min, y_max)

                print(f">>> Clicking on track at position ({x}, {y})")

                for offset in [(0, 0), (10, 0), (-10, 0), (0, 10), (0, -10)]:
                    click_x = max(0, min(screen_width, x + offset[0]))
                    click_y = max(0, min(screen_height, y + offset[1]))
                    pyautogui.click(click_x, click_y)
                    time.sleep(0.3)
            except ImportError:
                self.click(random.randint(400, 800), random.randint(300, 600))
                time.sleep(0.5)
                self.click(random.randint(400, 800), random.randint(300, 600))

            time.sleep(5)

            print(">>> Using multiple methods to start music playback")

            try:
                import pyautogui
                screen_width, screen_height = pyautogui.size()

                center_x, center_y = screen_width // 2, screen_height // 2
                print(f">>> Clicking center of screen ({center_x}, {center_y})")
                pyautogui.click(center_x, center_y)
                time.sleep(1)

                play_positions = [
                    (center_x, center_y - 100),
                    (center_x - 200, center_y),
                    (center_x, center_y - 50),
                    (center_x - 100, center_y),
                    (center_x - 250, center_y),
                    (center_x - 250, center_y - 50),
                    (center_x - 250, center_y + 50)
                ]

                for pos in play_positions:
                    print(f">>> Clicking potential play button at {pos}")
                    for offset in [(0, 0), (5, 0), (-5, 0), (0, 5), (0, -5)]:
                        click_x = max(0, min(screen_width, pos[0] + offset[0]))
                        click_y = max(0, min(screen_height, pos[1] + offset[1]))
                        pyautogui.click(click_x, click_y)
                        time.sleep(0.2)

            except ImportError:
                for pos in [(800, 400), (500, 300), (300, 400), (700, 300)]:
                    print(f">>> Clicking position {pos}")
                    self.click(pos[0], pos[1])
                    time.sleep(1)

            for _ in range(3):
                print(">>> Pressing space key to play/pause")
                self.press_key("space")
                time.sleep(0.5)

            print(">>> Trying media player shortcuts")
            for key in ["j", "k", "l"]:
                self.press_key(key)
                time.sleep(0.5)

            try:
                import pyautogui
                screen_width, screen_height = pyautogui.size()

                waveform_y = screen_height // 2

                for x_ratio in [0.25, 0.5, 0.75]:
                    x = int(screen_width * x_ratio)
                    print(f">>> Clicking on waveform at ({x}, {waveform_y})")
                    pyautogui.click(x, waveform_y)
                    time.sleep(0.5)
            except ImportError:
                pass

            print(">>> Track should be playing now")
            time.sleep(5)

            listen_time = random.randint(
                config.get("soundcloud_min_listen", 1800),
                config.get("soundcloud_max_listen", 1800)
            )

            print(f">>> Listening to music for {listen_time} seconds")

            def ensure_playback():
                print(">>> Ensuring music is playing...")

                try:
                    import pyautogui
                    screen_width, screen_height = pyautogui.size()

                    play_positions = [
                        (screen_width // 2, screen_height // 2 - 100),
                        (screen_width // 3, screen_height // 2),
                        (screen_width // 2, screen_height // 2),
                        (screen_width // 2 - 200, screen_height // 2),
                        (50, screen_height // 2),
                        (screen_width // 2 - 250, screen_height // 2)
                    ]

                    for pos in play_positions:
                        print(f">>> Clicking potential play button at {pos}")
                        for offset in [(0, 0), (5, 5), (-5, -5), (5, -5), (-5, 5)]:
                            click_x = max(0, min(screen_width, pos[0] + offset[0]))
                            click_y = max(0, min(screen_height, pos[1] + offset[1]))
                            pyautogui.click(click_x, click_y)
                            time.sleep(0.2)
                except ImportError:
                    for pos in [(400, 300), (300, 350), (500, 300)]:
                        self.click(pos[0], pos[1])
                        time.sleep(0.5)

                print(">>> Pressing space to play/pause")
                self.press_key("space")
                time.sleep(0.5)

                self.press_key("l")
                time.sleep(0.5)

                try:
                    platform = self.get_platform()

                    if platform == "linux":
                        try:
                            subprocess.run(["xdotool", "key", "space"], timeout=1)
                            print(">>> Used xdotool to press space")
                        except (subprocess.SubprocessError, FileNotFoundError):
                            pass
                    elif platform == "windows":
                        pass
                except Exception as e:
                    print(f">>> Error trying platform-specific playback: {e}")

            intervals = min(15, max(3, listen_time // 120))
            interval_time = listen_time / intervals
            last_playback_check = time.time()
            playback_check_interval = 180

            ensure_playback()

            for i in range(intervals):
                current_sleep = min(interval_time, playback_check_interval)
                time.sleep(current_sleep)

                current_time = time.time()
                if current_time - last_playback_check >= playback_check_interval:
                    ensure_playback()
                    last_playback_check = current_time

                interaction = random.choice([
                    "Still listening...",
                    "Enjoying the music...",
                    "Music playing...",
                    "Track continues...",
                    "Audio streaming..."
                ])
                print(f">>> {interaction}")

                elapsed = (i + 1) * interval_time
                percent_complete = min(100, (elapsed / listen_time) * 100)
                print(f">>> Track progress: approximately {percent_complete:.1f}% complete")

                if random.random() < 0.7:
                    interaction_type = random.choice([
                        "skip_forward",
                        "skip_backward",
                        "play_pause",
                        "volume_up",
                        "volume_down",
                        "mute"
                    ])

                    if interaction_type == "skip_forward":
                        for _ in range(random.randint(1, 3)):
                            self.press_key("Right")
                            time.sleep(0.2)
                        print(">>> Skipped forward in track")

                    elif interaction_type == "skip_backward":
                        for _ in range(random.randint(1, 3)):
                            self.press_key("Left")
                            time.sleep(0.2)
                        print(">>> Skipped backward in track")

                    elif interaction_type == "play_pause":
                        self.press_key("space")
                        print(">>> Paused track")
                        time.sleep(random.uniform(1.0, 2.0))
                        self.press_key("space")
                        print(">>> Resumed track")

                    elif interaction_type == "volume_up":
                        for _ in range(random.randint(1, 3)):
                            self.press_key("Up")
                            time.sleep(0.2)
                        print(">>> Increased volume")

                    elif interaction_type == "volume_down":
                        for _ in range(random.randint(1, 3)):
                            self.press_key("Down")
                            time.sleep(0.2)
                        print(">>> Decreased volume")

                    elif interaction_type == "mute":
                        self.press_key("m")
                        print(">>> Muted track")
                        time.sleep(random.uniform(1.0, 2.0))
                        self.press_key("m")
                        print(">>> Unmuted track")

                if i % 3 == 0 and random.random() < 0.5:
                    scroll_amount = random.randint(1, 3)
                    self.scroll_down(scroll_amount)
                    print(f">>> Scrolled down {scroll_amount} times to see more tracks")
                    time.sleep(random.uniform(1.0, 3.0))

                    if random.random() < 0.3:
                        try:
                            import pyautogui
                            screen_width = pyautogui.size()[0]
                            x_pos = random.randint(screen_width // 4, screen_width // 4 * 3)
                            y_pos = random.randint(400, 600)
                            print(f">>> Clicking on another track at ({x_pos}, {y_pos})")

                            for offset in [(0, 0), (10, 0), (-10, 0), (0, 10), (0, -10)]:
                                click_x = max(0, min(screen_width, x_pos + offset[0]))
                                click_y = max(0, min(screen_height, y_pos + offset[1]))
                                pyautogui.click(click_x, click_y)
                                time.sleep(0.2)

                            time.sleep(2)
                            ensure_playback()
                        except ImportError:
                            self.click(random.randint(300, 700), random.randint(400, 600))
                            time.sleep(2)

        self.close_browser()
        return True

    def get_platform(self):

        import platform
        system = platform.system().lower()
        if system == "linux":
            return "linux"
        elif system == "windows":
            return "windows"
        elif system == "darwin":
            return "macos"
        else:
            return "unknown"