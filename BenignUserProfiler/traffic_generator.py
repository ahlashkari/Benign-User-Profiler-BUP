#!/usr/bin/env python3

import datetime
import time
import os
from multiprocessing import Process, Manager, Pool, cpu_count
from .scheduler import Scheduler


class TrafficGenerator(object):
    def __init__(self) -> None:
        pass

    def generate_parallel(self, scheduler: Scheduler, num_threads=None) -> None:
        if num_threads is None:
            num_threads = cpu_count()
            
        processes = []
        print(f">>> Starting parallel execution with {num_threads} threads")
        
        with Manager() as manager:
            task_ids = manager.list()
            task_ids.extend(scheduler.get_tasks_ids())
            get_task_lock = manager.Lock()
            
            for i in range(num_threads):
                processes.append(Process(
                    target=self._worker_process, 
                    args=(i, task_ids, get_task_lock, scheduler)
                ))

            for i in range(num_threads):
                processes[i].start()

            for i in range(num_threads):
                processes[i].join()

    def _worker_process(self, thread_number: int, task_ids, get_task_lock, scheduler) -> None:
        while True:
            task = None
            with get_task_lock:
                if len(task_ids) == 0:
                    return
                task_id = task_ids.pop()
                task = scheduler.get_task_by_id(task_id)
                print(f">>> Thread {thread_number}: Processing task: {str(task)}")
            current_time = datetime.datetime.now()
            if current_time < task.get_start_time():
                waiting_time = task.get_start_time() - current_time
                print(f">>> Thread {thread_number}: Waiting for {waiting_time}")
                time.sleep(waiting_time.total_seconds())
            try:
                task.generate()
            except Exception as e:
                print(f">>> Thread {thread_number}: Error executing task {str(task)}: {e}")

    def generate_sequential(self, scheduler: Scheduler) -> None:
        task_ids = scheduler.get_tasks_ids()
        print(f">>> Starting sequential execution with {len(task_ids)} tasks")
        
        for task_id in task_ids:
            task = scheduler.get_task_by_id(task_id)
            print(f">>> Processing task: {str(task)}")
            current_time = datetime.datetime.now()
            if current_time < task.get_start_time():
                waiting_time = task.get_start_time() - current_time
                print(f">>> Waiting for {waiting_time}")
                time.sleep(waiting_time.total_seconds())
            try:
                task.generate()
            except Exception as e:
                print(f">>> Error executing task {str(task)}: {e}")