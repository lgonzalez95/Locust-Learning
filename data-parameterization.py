"""
Test data in separate file: CSV, TXT, JSON, ETC
Test data in python file
Test data from third party libreary like Faker
"""

from locust import task, constant, SequentialTaskSet, FastHttpUser
from CsvRead import CsvRead


class MyScript(SequentialTaskSet):
    @task
    def place_order(self):
        test_data = CsvRead("Data/data.csv").read()

        data = {
            "custname": test_data['name'],
            "custtel": test_data['phone'],
            "custemail": test_data['email'],
            "size": test_data['size'],
            "topping": test_data['toppings'],
            "delivery": test_data['time'],
            "comments": test_data['instructions']
        }

        name = 'Order for ' + test_data['name']

        with self.client.post("/post", catch_response=True, name=name, data=data) as response:
            print( response.text)
            if response.status_code == 200 and test_data['name'] in response.text:
                response.success()
            else:
                response.failure("Failure in processing the order")


class LoadTest(FastHttpUser):
    host = "https://httpbin.org"
    tasks = [MyScript]
    wait_time = constant(1)
