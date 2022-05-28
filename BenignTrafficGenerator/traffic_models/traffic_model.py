#!/usr/bin/env python3

from abc import ABC, abstractmethod

class TrafficModel(ABC):
    @abstractmethod
    def generate(self, flow: object) -> None:
        pass
