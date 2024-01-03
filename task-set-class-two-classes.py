from locust import TaskSet, constant, task, HttpUser
import random


class MyHttpCat(TaskSet):
    @task
    def get_status(self):
        self.client.get("/200")
        print("Get status of 200")
        self.interrupt(reschedule=False)


@task
class MyAnotherHttpCat(TaskSet):
    @task
    def get_500_code(self):
        self.client.get("/500")
        print("Get status of 500")
        self.interrupt(reschedule=False)


class MyLoadTest(HttpUser):
    host = "https://http.cat"
    wait_time = constant(1)
    tasks = [MyHttpCat, MyAnotherHttpCat]
