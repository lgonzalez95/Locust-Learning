from locust import SequentialTaskSet, constant, task, HttpUser
import random


class MySequentialTaskSet(SequentialTaskSet):
    @task
    def get_status(self):
        self.client.get("/200")
        print("Get the status of 200")

    @task
    def get_random_status(self):
        status_codes = [100, 101, 102, 200, 201, 202, 203, 204, 205, 206, 207]
        self.client.get("/" + str(random.choice(status_codes)))
        print("Get the random status code")


class MyLoadTest(HttpUser):
    host = "https://http.cat"
    wait_time = constant(1)
    tasks = [MySequentialTaskSet]
