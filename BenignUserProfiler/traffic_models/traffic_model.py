#!/usr/bin/env python3

from abc import ABC, abstractmethod
from datetime import datetime, timedelta
import random

class TrafficModel(ABC):
    def __init__(self):
        self.start_time = datetime.now()
        self.frequency = 1
        self.time_interval = 0
        self.model_config = {}

    @abstractmethod
    def generate(self) -> None:
        pass

    @abstractmethod
    def verify(self) -> bool:
        pass

    @abstractmethod
    def __str__(self) -> str:
        pass

    def get_start_time(self):
        return self.start_time
    
    def set_start_time(self, frequency: int):
        if isinstance(self.time_interval, list) and len(self.time_interval) == 2:
            interval = random.randint(self.time_interval[0], self.time_interval[1])
        else:
            interval = self.time_interval
        self.start_time = self.start_time + timedelta(seconds=frequency * interval)