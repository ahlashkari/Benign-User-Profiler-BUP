#!/usr/bin/env python3

from datetime import datetime
import argparse
import sys
import os
import platform
import tempfile
from .config_loader import ConfigLoader
from .traffic_models.model_factory import ModelFactory
from .scheduler import Scheduler
from .traffic_generator import TrafficGenerator


class BenignUserProfiler(object):
    def __init__(self, config_file, parallel=False, work_hours=None, randomize=False, headless=False, simulate=False):
        self.config_file = config_file
        self.parallel = parallel
        self.randomize = randomize
        self.headless = headless
        self.simulate = simulate
        self.temp_dir = tempfile.mkdtemp()
        
        if work_hours:
            start_time = "09:00"
            end_time = "17:00"
            
            if isinstance(work_hours, str):
                try:
                    work_hours_parts = work_hours.split("-")
                    if len(work_hours_parts) == 2:
                        start_time = work_hours_parts[0].strip()
                        end_time = work_hours_parts[1].strip()
                except:
                    pass
                    
            self.work_hours = {
                "start": start_time,
                "end": end_time
            }
        else:
            self.work_hours = None

    def run(self) -> None:
        try:
            config = ConfigLoader().load(self.config_file)
            if not config:
                return
                
            if self.work_hours:
                for model_config in config.values():
                    model_config["work_hours"] = self.work_hours
                    
            if self.randomize:
                for model_config in config.values():
                    model_config["randomize"] = True
            
            if self.simulate:
                for model_config in config.values():
                    model_config["simulate"] = True
                    
            model_factory = ModelFactory(headless=self.headless)
            scheduler = Scheduler()
            generator = TrafficGenerator()

            for name, model_config in config.items():
                model = model_factory.create_model(model_config)
                if model:
                    scheduler.add_model(model)

            if self.parallel:
                generator.generate_parallel(scheduler)
            else:
                generator.generate_sequential(scheduler)
        except Exception as e:
            print(f">>> Error in BenignUserProfiler. {e}")


def main():
    print(f"""
    *****************************************************************************
    *                                                                           *
    *                      Benign User Profiler (BUP)                           *
    *                                                                           *
    *         A tool for generating realistic user traffic patterns             *
    *                                                                           *
    *****************************************************************************
    
    Running on: {platform.system()} {platform.release()}
    Python version: {platform.python_version()}
    Current time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
    """)

    parser = argparse.ArgumentParser()
    parser.add_argument("--config", "-c", help="Config file path", default=os.path.join(os.path.dirname(__file__), "config.json"))
    parser.add_argument("--parallel", "-p", help="Run tasks in parallel", action="store_true")
    parser.add_argument("--work-hours", "-w", help="Set work hours (e.g. '09:00-17:00') or use default 9am-5pm if no value provided", nargs="?", const=True)
    parser.add_argument("--randomize", "-r", help="Randomize task execution", action="store_true")
    parser.add_argument("--headless", "-d", help="Run browsers in headless mode", action="store_true")
    parser.add_argument("--skip-actions", "-s", help="Skip performing actual actions", action="store_true")
    args = parser.parse_args()

    profiler = BenignUserProfiler(
        config_file=args.config, 
        parallel=args.parallel, 
        work_hours=args.work_hours, 
        randomize=args.randomize,
        headless=args.headless,
        simulate=args.skip_actions
    )
    profiler.run()

    if len(sys.argv) == 1:
        print("No arguments provided. Use -h or --help to see available options.")


if __name__ == "__main__":
    main()