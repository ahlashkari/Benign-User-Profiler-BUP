#!/usr/bin/env python3

import datetime
import time
from multiprocessing import Process, Manager, Pool
from .scheduler import Scheduler


class TrafficGenerator(object):
    def __init__(self, scheduler: Scheduler, number_of_threads: int) -> None:
        self.__scheduler = scheduler
        self.__number_of_threads = number_of_threads

    def start(self) -> None:
        processes = []
        if self.__number_of_threads == 1:
            self.start_sequential()
            return
        with Manager() as manager:
            self.__tasks_ids = manager.list()
            self.__tasks_ids.extend(self.__scheduler.get_tasks_ids())
            self.__get_task_lock = manager.Lock()
            for i in range(self.__number_of_threads):
                processes.append(Process(target=self.__worker, args=(i,)))

            for i in range(self.__number_of_threads):
                processes[i].start()

            for i in range(self.__number_of_threads):
                processes[i].join()

    def __worker(self, thread_number: int) -> None:
        while(True):
            task = None
            with self.__get_task_lock:
                if len(self.__tasks_ids) == 0:
                    return
                task_id = self.__tasks_ids.pop()
                task = self.__scheduler.get_task_by_id(task_id)
                print(f">> thread number: {thread_number}, task: {str(task)}")
            current_time = datetime.datetime.now()
            if current_time < task.get_start_time():
                waiting_time = task.get_start_time() - current_time
                print(f">> thread number: {thread_number}, waiting for {waiting_time}")
                time.sleep(waiting_time.total_seconds())
            task.generate()

    def start_sequential(self):
        self.__tasks_ids = []
        self.__tasks_ids.extend(self.__scheduler.get_tasks_ids())

        while(True):
            task = None
            if len(self.__tasks_ids) == 0:
                return
            task_id = self.__tasks_ids.pop()
            task = self.__scheduler.get_task_by_id(task_id)
            print(f">> thread number: 0, task: {str(task)}")

            current_time = datetime.datetime.now()
            if current_time < task.get_start_time():
                waiting_time = task.get_start_time() - current_time
                print(f">> thread number: 0, waiting for {waiting_time}")
                time.sleep(waiting_time.total_seconds())
            task.generate()
