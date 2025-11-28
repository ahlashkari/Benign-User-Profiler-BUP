#!/usr/bin/env python3

import time
import random
from .base_browser import BaseBrowserModule

class YoutubeModule(BaseBrowserModule):
    def execute(self, config):
        youtube_url = "https://www.youtube.com"

        if not self.browser_command(youtube_url):
            print(">>> Failed to launch browser for YouTube")
            return False

        print(f">>> Browsing YouTube: {youtube_url}")

        time.sleep(random.uniform(5, 10))

        if "youtube_searches" in config:
            search_term = random.choice(config["youtube_searches"])
            print(f">>> Searching for: {search_term}")

            search_method = random.choice(["direct_url", "interactive"])

            if search_method == "direct_url":
                search_url = f"https://www.youtube.com/results?search_query={search_term.replace(' ', '+')}"
                print(f">>> Using direct URL search: {search_url}")
                self.browser_command(search_url)
            else:
                print(">>> Using interactive search method")

                search_box_positions = [
                    (500, 120),
                    (600, 120),
                    (400, 120)
                ]

                time.sleep(random.uniform(2, 4))

                print(">>> Clicking on YouTube's search box (avoiding browser search bar)")
                for pos in search_box_positions:
                    print(f">>> Clicking YouTube search box at position {pos}")
                    try:
                        import pyautogui
                        screen_width, screen_height = pyautogui.size()
                        scaled_x = int(pos[0] * screen_width / 1000)
                        scaled_y = int(pos[1] * screen_height / 800)
                        pyautogui.click(scaled_x, scaled_y)
                    except ImportError:
                        self.click(pos[0], pos[1])
                    time.sleep(1.0)

                print(f">>> Typing search term: {search_term}")
                for char in search_term:
                    try:
                        import pyautogui
                        pyautogui.write(char, interval=0.1)
                    except ImportError:
                        self.keyboard_input(char)
                    time.sleep(0.05)

                time.sleep(0.5)
                print(">>> Pressing Enter to search")
                try:
                    import pyautogui
                    pyautogui.press('enter')
                except ImportError:
                    self.press_key("Return")

                time.sleep(5)

            time.sleep(random.uniform(5, 10))

            print(">>> Selecting a video from search results")

            try:
                import pyautogui
                screen_width, screen_height = pyautogui.size()

                video_positions = [
                    (screen_width // 2, int(screen_height * 0.3)),
                    (screen_width // 2, int(screen_height * 0.4)),
                    (screen_width // 2, int(screen_height * 0.5)),
                    (screen_width // 2, int(screen_height * 0.6)),
                    (screen_width // 2, int(screen_height * 0.7))
                ]

                video_weights = [0.4, 0.3, 0.15, 0.1, 0.05]
                selected_index = random.choices(range(len(video_positions)), weights=video_weights, k=1)[0]
                selected_pos = video_positions[selected_index]

                print(f">>> Clicking on video at position {selected_pos} (result #{selected_index+1})")
                pyautogui.click(selected_pos[0], selected_pos[1])

            except ImportError:
                video_positions = [
                    (500, 300),
                    (500, 400),
                    (500, 500),
                    (500, 600),
                    (500, 700)
                ]

                video_weights = [0.4, 0.3, 0.15, 0.1, 0.05]
                selected_index = random.choices(range(len(video_positions)), weights=video_weights, k=1)[0]
                selected_pos = video_positions[selected_index]

                print(f">>> Clicking on video at position {selected_pos} (result #{selected_index+1})")
                self.click(selected_pos[0], selected_pos[1])

            for i in range(2):
                time.sleep(0.5)
                try:
                    import pyautogui
                    offset_x = random.randint(-20, 20)
                    offset_y = random.randint(-10, 10)
                    pyautogui.click(selected_pos[0] + offset_x, selected_pos[1] + offset_y)
                except ImportError:
                    self.click(selected_pos[0], selected_pos[1])

            time.sleep(random.uniform(5, 10))

            watch_time = random.randint(
                config.get("youtube_min_watch", 1800),
                config.get("youtube_max_watch", 1800)
            )

            print(f">>> Watching video for {watch_time} seconds")

            print(">>> Trying all methods to ensure video playback")

            if "youtube_video" in config:
                direct_url = config["youtube_video"]
                print(f">>> Using direct YouTube URL: {direct_url}")
                self.browser_command(direct_url)
                time.sleep(5)

            def try_play_methods():
                click_positions = [
                    (500, 350),
                    (400, 300),
                    (600, 350),
                    (500, 400),
                    (350, 350)
                ]

                for pos in click_positions:
                    print(f">>> Clicking at position {pos}")
                    try:
                        import pyautogui
                        screen_width, screen_height = pyautogui.size()
                        x_scale = screen_width / 1000
                        y_scale = screen_height / 700
                        scaled_x = int(pos[0] * x_scale)
                        scaled_y = int(pos[1] * y_scale)
                        print(f">>> Using PyAutoGUI to click at {scaled_x}, {scaled_y}")
                        pyautogui.click(scaled_x, scaled_y)
                    except ImportError:
                        self.click(pos[0], pos[1])
                    time.sleep(0.5)

                play_keys = ["space", "k", "p", "Return"]
                for key in play_keys:
                    print(f">>> Pressing '{key}' key to play video")
                    self.press_key(key)
                    time.sleep(0.5)

                print(">>> Pressing 'f' key to toggle fullscreen")
                self.press_key("f")
                time.sleep(1)
                self.press_key("f")
                time.sleep(1)

                big_play_positions = [
                    (screen_width // 2, screen_height // 2),
                    (screen_width // 2, screen_height // 2 - 50)
                ]
                for pos in big_play_positions:
                    try:
                        import pyautogui
                        print(f">>> Clicking large play button at {pos}")
                        pyautogui.click(pos[0], pos[1])
                    except ImportError:
                        pass
                    time.sleep(0.5)

            try_play_methods()
            time.sleep(3)

            intervals = min(10, max(2, watch_time // 30))
            interval_time = watch_time / intervals

            last_play_check = time.time()
            play_check_interval = 300

            for i in range(intervals):
                current_sleep = min(interval_time, play_check_interval)
                time.sleep(current_sleep)

                current_time = time.time()
                if current_time - last_play_check >= play_check_interval:
                    print(">>> Periodic playback check - ensuring video is still playing")
                    try_play_methods()
                    last_play_check = current_time

                interaction = random.choice([
                    "Still watching...",
                    "Watching video...",
                    "Video playing..."
                ])
                print(f">>> {interaction}")

                elapsed = (i + 1) * interval_time
                percent_complete = min(100, (elapsed / watch_time) * 100)
                print(f">>> Video progress: approximately {percent_complete:.1f}% complete")

                if random.random() < 0.7:
                    interaction_type = random.choice([
                        "play_pause",
                        "like",
                        "volume",
                        "skip",
                        "fullscreen",
                        "quality",
                        "mute"
                    ])

                    if interaction_type == "play_pause":
                        key = random.choice(["space", "k"])
                        self.press_key(key)
                        print(f">>> Pressed {key} key to pause video")
                        time.sleep(1.5)
                        self.press_key(key)
                        print(f">>> Pressed {key} key to resume video")

                    elif interaction_type == "like":
                        self.press_key("l")
                        print(">>> Pressed L key to like/unlike video")

                    elif interaction_type == "volume":
                        for _ in range(random.randint(1, 3)):
                            self.press_key("Up")
                            time.sleep(0.2)
                        time.sleep(0.5)
                        for _ in range(random.randint(1, 2)):
                            self.press_key("Down")
                            time.sleep(0.2)
                        print(">>> Adjusted volume with arrow keys")

                    elif interaction_type == "skip":
                        direction = random.choice(["forward", "backward"])
                        if direction == "forward":
                            for _ in range(random.randint(1, 5)):
                                self.press_key("Right")
                                time.sleep(0.2)
                            print(">>> Skipped forward in video")
                        else:
                            for _ in range(random.randint(1, 3)):
                                self.press_key("Left")
                                time.sleep(0.2)
                            print(">>> Skipped backward in video")

                    elif interaction_type == "fullscreen":
                        self.press_key("f")
                        print(">>> Toggled fullscreen mode")
                        time.sleep(3)
                        self.press_key("f")
                        print(">>> Exited fullscreen mode")

                    elif interaction_type == "quality":
                        self.press_key(".")
                        time.sleep(1)
                        for _ in range(random.randint(1, 4)):
                            self.press_key("Down")
                            time.sleep(0.3)
                        self.press_key("Escape")
                        print(">>> Adjusted video quality settings")

                    elif interaction_type == "mute":
                        self.press_key("m")
                        print(">>> Muted video")
                        time.sleep(2)
                        self.press_key("m")
                        print(">>> Unmuted video")

                if i % 3 == 0 and random.random() < 0.5:
                    self.scroll_down(random.randint(1, 3))
                    print(">>> Scrolled down to view comments")
                    time.sleep(2)
                    for _ in range(random.randint(1, 3)):
                        self.press_key("Home")
                        time.sleep(0.5)
                    print(">>> Scrolled back to video")

        self.close_browser()
        return True