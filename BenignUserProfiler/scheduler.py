#!/usr/bin/env python3

import copy
import random
from datetime import datetime, timedelta

class Scheduler(object):
    def __init__(self):
        self.__tasks = []
        self.__tasks_ids = []
        self.__models = []

    def add_model(self, model):
        self.__models.append(model)
        self.__schedule_model(model)

    def __schedule_model(self, model):
        task_id = len(self.__tasks)
        
        for frequency_index in range(model.frequency):
            task = copy.copy(model)
            task.set_start_time(frequency=frequency_index)
            self.__tasks.append((task_id, task))
            self.__tasks_ids.append((task_id, task.get_start_time()))
            task_id += 1

        self.__tasks_ids.sort(key=lambda task: task[1], reverse=True)

    def get_tasks_ids(self):
        tasks = [task[0] for task in self.__tasks_ids]
        
        should_randomize = any(getattr(model, 'model_config', {}).get('randomize', False) for model in self.__models)
        
        if should_randomize:
            print(">>> Randomizing task execution order")
            random.shuffle(tasks)
            
        return tasks

    def get_task_by_id(self, task_id: int):
        for task in self.__tasks:
            if task[0] == task_id:
                return task[1]
        return None
        
    def get_tasks_count(self):
        return len(self.__tasks)