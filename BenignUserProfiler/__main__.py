#!/usr/bin/env python3

import argparse
from multiprocessing import cpu_count
from .benign_user_profiler import BenignUserProfiler

def args_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog='BenignUserProfiler')
    parser.add_argument('-c', '--config-file', action='store', help='Json config file address.')
    parser.add_argument('-l', '--headless', action='store_false', help='Browser mode. default=True.')
    parser.add_argument('-t', '--threads', action='store', help='Number of threads. default=CPU count')
    return parser


def main():
    parsed_arguments = args_parser().parse_args()
    config_file_address = "./BenignUserProfiler/config.json" if parsed_arguments.config_file is None else parsed_arguments.config_file
    headless = parsed_arguments.headless
    number_of_threads = cpu_count() if parsed_arguments.threads is None else int(parsed_arguments.threads)
    benign_user_profiler = BenignUserProfiler(config_file_address, headless, number_of_threads)
    benign_user_profiler.run()


if __name__ == "__main__":
    main()
