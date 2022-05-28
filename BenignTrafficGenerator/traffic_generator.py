#!/usr/bin/env python3

class TrafficGenerator(object):
    def start(self, traffic_models: list) -> None:
        for traffic_model in traffic_models:
            traffic_model.generate()
