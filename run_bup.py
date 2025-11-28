#!/usr/bin/env python3


import os
import sys
from BenignUserProfiler.benign_user_profiler import BenignUserProfiler

def main():
    config_path = os.path.join(os.path.dirname(__file__), "BenignUserProfiler", "config.json")
    print(f"Config path: {os.path.abspath(config_path)}")
    profiler = BenignUserProfiler(
        config_file=config_path,
        parallel=False,
        work_hours=None,
        randomize=True
    )
    profiler.run()

if __name__ == "__main__":
    main()