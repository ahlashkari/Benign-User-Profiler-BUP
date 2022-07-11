#!/usr/bin/env python3

from pymongo import MongoClient
from .traffic_model import TrafficModel


class DBModel(TrafficModel):
    def __init__(self, model_config: dict):
        # TODO: verify the model config
        self._model_config = model_config
        self._url = self._model_config["url"]
        self._database_name = self._model_config["database"]
        self._queries = self._model_config["queries"]


class MongoDBModel(DBModel):
    def generate(self):
        collection_name = self._model_config["collection"]
        client = MongoClient(self._url)
        db = client[self._database_name]
        collection = db[collection_name]
        for query in self._queries:
            collection.find(query)

