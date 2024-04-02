#!/usr/bin/env python3

from abc import ABC, abstractmethod
from datetime import datetime, timedelta

class TrafficModel(ABC):
    start_time: datetime = datetime.now()
    frequency: int = 1
    time_interval: int = 0
    model_config: dict = {}

    @abstractmethod
    def generate(self) -> None:
        pass

    @abstractmethod
    def verify(self) -> None:
        pass

    @abstractmethod
    def __str__(self) -> None:
        pass

    def get_start_time(self):
        return self.start_time
    
    def set_start_time(self, frequency: int):
        self.start_time = self.start_time + timedelta(seconds=frequency * self.time_interval)