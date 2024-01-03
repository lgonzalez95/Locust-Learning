"""
User class represents a user which is to be spawned and attack the system
some methods available are:
abstract=True
on_start()
on_stop()
tasks
wait()
wait_time()
weight = 10
"""

from locust import User, task, constant


class MyFirstDemo(User):
    weight = 2
    wait_time = constant(1)

    @task
    def launch(self):
        print("Launching the URL")

    @task
    def search(self):
        print("Searching")


class MySecondDemo(User):
    weight = 2
    wait_time = constant(1)

    @task
    def launch2(self):
        print("Second")

    @task
    def search2(self):
        print("Searching second")
