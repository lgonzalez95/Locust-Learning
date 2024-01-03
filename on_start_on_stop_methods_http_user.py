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
from locust import HttpUser, task, constant, SequentialTaskSet


class MyTest(SequentialTaskSet):

    def on_start(self):
        self.client.get("/", name=self.on_start.__name__)
        print("Start")

    @task
    def browse_product(self):
        self.client.get("/product/OLJCESPC7Z", name=self.browse_product.__name__)
        print("Browse Product")

    @task
    def cart_page(self):
        self.client.get("/cart", name=self.browse_product.__name__)
        print("Cart Page")

    def on_stop(self):
        self.client.get("/", name=self.on_stop.__name__)
        print("Stop")


class LoadTest(HttpUser):
    host = "https://onlineboutique.dev"
    tasks = [MyTest]
    wait_time = constant(1)

# locust -f on_start_on_stop_methods_http_user.py -r 1 -u 1 -t 10s --headless --only-summary
