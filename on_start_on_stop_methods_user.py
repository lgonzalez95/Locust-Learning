"""
Don't use @task decorator for these methods
They will be executed only once

on_start()
   ↓
@tasks
   ↓
on_stop()

Users:
on_start is called when a user starts
on_stop is called when a user starts


TaskSet:
on_start is called when the taskSet start executing
on_stop is called when the taskSet start executing
"""

from locust import User, task, constant


class MyTest(User):
    wait_time = constant(1)

    def on_start(self):
        print("Starting")

    @task
    def task_1(self):
        print("Task")

    def on_stop(self):
        print("Stopping")
