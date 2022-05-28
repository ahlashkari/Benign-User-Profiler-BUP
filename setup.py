#!/usr/bin/env python3

try:
    from setuptools import setup
except ImportError as error:
    raise SystemExit(error)

version = "0.1.0"
author = "Moein Shafi"
author_email = "mosafer.moein@gmail.com"
entry_points = {
        "console_scripts": ["benign-traffic-generator = BenignTrafficGenerator.__main__:main"]
        }

setup(
        name="BenignTrafficGenerator",
        version=version,
        author=author,
        author_email=author_email,
        packages=[
            "BenignTrafficGenerator",
            "BenignTrafficGenerator.traffic_models",
        ],
        package_dir={
            "BenignTrafficGenerator": "BenignTrafficGenerator",
            "BenignTrafficGenerator.traffic_models": "BenignTrafficGenerator/traffic_models",
        },
        entry_points=entry_points,
)
