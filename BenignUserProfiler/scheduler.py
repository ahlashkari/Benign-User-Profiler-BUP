#!/usr/bin/python3

import copy

class Scheduler(object):
    def __init__(self, traffic_models: list):
        self.__tasks = []
        self.__tasks_ids = []
        self.__prioritize_tasks(traffic_models)

    def __prioritize_tasks(self, traffic_models: list):
        task_id = 0
        for traffic_model in traffic_models:
            for frequency in range(traffic_model.frequency):
                task = copy.copy(traffic_model)
                task.set_start_time(frequency=frequency)
                self.__tasks.append((task_id, task))
                self.__tasks_ids.append((task_id, task.get_start_time()))
                task_id += 1

        self.__tasks_ids.sort(key=lambda task: task[1], reverse=True)

    def get_tasks_ids(self):
        tasks = [task[0] for task in self.__tasks_ids]
        return tasks

    def get_task_by_id(self, task_id: int):
        for task in self.__tasks:
            if task[0] == task_id:
                return task[1]
        return None
