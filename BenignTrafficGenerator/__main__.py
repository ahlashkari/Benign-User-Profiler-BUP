#!/usr/bin/env python3

import argparse
from .benign_traffic_generator import BenignTrafficGenerator

def args_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog='BenignTrafficGenerator')
    parser.add_argument('-c', '--config-file', action='store', help='Json config file address.')
    return parser


def main():
    parsed_arguments = args_parser().parse_args()
    config_file_address = "./BenignTrafficGenerator/config.json" if parsed_arguments.config_file is None else parsed_arguments.config_file
    benign_traffic_generator = BenignTrafficGenerator(config_file_address)
    benign_traffic_generator.run()


if __name__ == "__main__":
    main()
