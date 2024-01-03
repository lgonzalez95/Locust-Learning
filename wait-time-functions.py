"""
Unit is in seconds

functions:

between (min, max): Will try to simulate a random time between the min and max
constant(wait_time): Waits the given time
constant_pacing(wait_time): Sets a global wait time and will be used by the tasks,
ignoring other wait times given within the tasks

"""
import time

from locust import User, task, constant, between, constant_pacing


class MyUser(User):
    # wait_time = constant(1)
    # wait_time = between(2, 4)
    wait_time = constant_pacing(2)

    # If the constant pacing is less than the time it takes to complete a task then it is
    # ignored, otherwise if it is more than the task's time then a delay will be added: constant pacing time - task time

    @task
    def launch(self):
        time.sleep(5)
        print("Injecting delay")
