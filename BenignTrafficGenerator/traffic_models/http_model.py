#!/usr/bin/env python3

from .traffic_model import TrafficModel


class HTTPModel(TrafficModel):
    def generate(self) -> None:
        print(">>>> It is HTTP traffic!")
        pass
