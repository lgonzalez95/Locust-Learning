from json import JSONDecodeError
from locust import task, constant, FastHttpUser, SequentialTaskSet, LoadTestShape
from faker import Faker


class UserActions(SequentialTaskSet):

    def __init__(self, parent):
        super().__init__(parent)
        self.auth_token = None
        self.fake = Faker()

    def on_start(self):
        url = "http://localhost:3001/authorize"
        payload = {"username": "eve.holt@reqres.in", "password": "cityslicka"}
        headers = {"headers": {"Content-Type": "application/json"}}
        with self.client.post(url, catch_response=True, json=payload, headers=headers, name="Get Token") as response:
            self.auth_token = response.json()["token"]

    @task
    def create_joke(self):
        url = '/create-joke-slow'
        expected_mgs = "Joke created successfully"
        headers = {"headers": {"Authorization": "Bearer " + self.auth_token}}
        payload = {"joke": self.fake.sentence()}
        with self.client.post(url, catch_response=True, json=payload, headers=headers, name="Create Joke") as response:
            try:
                if expected_mgs in response.text:
                    response.success()
                else:
                    response.failure('The Joke creation has failed')
                try:
                    assert response.json()["message"] == expected_mgs, 'The expected message should be: ' + expected_mgs
                except JSONDecodeError as e:
                    response.failure("Response could not be decoded as JSON:" + str(e))
                except KeyError as k:
                    response.failure("Response did not contain expected key: " + str(k))
            except TypeError as e:
                print('Type error ' + str(e) + ' for response: ' + str(response.text))


class User(FastHttpUser):
    host = "http://localhost:3001"
    wait_time = constant(1)
    tasks = [UserActions]


class CustomLoad(LoadTestShape):
    """
    Keyword arguments:
        stages -- A list of dicts, each representing a stage with the following keys:
            duration -- When this many seconds pass the test is advanced to the next stage
            users -- Total user count
            spawn_rate -- Number of users to start/stop per second
            stop -- A boolean that can stop that test at a specific stage
        stop_at_end -- Can be set to stop once all stages have run.
    """
    stages = [
        {"duration": 10, "users": 10, "spawn_rate": 2},
        {"duration": 60, "users": 100, "spawn_rate": 10},  # normal request load
        {"duration": 120, "users": 200, "spawn_rate": 20},  # request load around the breaking point
        {"duration": 180, "users": 200, "spawn_rate": 20},  # request load around the breaking point
        {"duration": 240, "users": 400, "spawn_rate": 30},  # request load beyond the breaking point
        {"duration": 300, "users": 0, "spawn_rate": 30},  # scale down to 0 requests for recovery stage
        {"duration": 360, "users": 10, "spawn_rate": 2}  # scale up to 10 users to verify the service was restored
    ]

    def tick(self):
        run_time = self.get_run_time()
        for stage in self.stages:
            if run_time < stage["duration"]:
                return stage["users"], stage["spawn_rate"]

        return None
