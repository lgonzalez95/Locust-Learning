from locust import TaskSet, constant, task, HttpUser
import random

"""
If you are performance testing a website that is structured in a hierarchical way, with sections and sub-sections, 
it may be useful to structure your load test the same way. For this purpose, Locust provides the TaskSet class.
"""


class MyHttpCat(TaskSet):
    @task
    def get_status(self):
        self.client.get("/200")
        print("Get status of 200")

    @task
    def get_random_status(self):
        status_codes = [100, 101, 102, 200, 201, 202, 203, 204, 205, 206, 207]
        self.client.get("/" + str(random.choice(status_codes)))
        print("Get random status code")


class MyLoadTest(HttpUser):
    host = "https://http.cat"
    wait_time = constant(1)
    tasks = [MyHttpCat]
