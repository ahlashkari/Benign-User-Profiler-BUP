#!/usr/bin/env python3

try:
    from setuptools import setup
except ImportError as error:
    raise SystemExit(error)

version = "1.0.0"
author = "AmirHossein Ahmadnejad Roudsari, Moein Shafi"
author_email = "amirhahm@yorku.ca"
entry_points = {
        "console_scripts": ["benign-user-profiler = BenignUserProfiler.__main__:main"]
        }

setup(
        name="BenignUserProfiler",
        version=version,
        author=author,
        author_email=author_email,
        packages=[
            "BenignUserProfiler",
            "BenignUserProfiler.traffic_models",
        ],
        package_dir={
            "BenignUserProfiler": "BenignUserProfiler",
            "BenignUserProfiler.traffic_models": "BenignUserProfiler/traffic_models",
        },
        entry_points=entry_points,
)
