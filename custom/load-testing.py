import random
from json import JSONDecodeError

from locust import task, constant, FastHttpUser, SequentialTaskSet, LoadTestShape


class UserActions(SequentialTaskSet):
    @task
    def get_filtered_joke_by_id(self):
        random_joke_id = random.randint(1, 70)
        url = '/v1/en/' + str(random_joke_id)
        with self.client.get(url, catch_response=True, name="Get Joke By Id") as response:
            if "id" in response.text:
                response.success()
            else:
                response.failure('Did not get any joke for the given id ' + str(random_joke_id))
            try:
                assert response.json()["id"] == random_joke_id, 'The received joke id should be ' + str(random_joke_id)
            except JSONDecodeError as e:
                response.failure("Response could not be decoded as JSON:" + str(e))
            except KeyError as k:
                response.failure("Response did not contain expected key: " + str(k))

    @task
    def get_slow_response(self):
        url = '/get-slow'
        expected_mgs = "This is just a test"
        with self.client.get(url, catch_response=True, name="Get Slow Message") as response:
            if "message" in response.text:
                response.success()
            else:
                response.failure('Did not get the expected response')
            try:
                assert response.json()["message"] == expected_mgs, 'The expected message should be: ' + expected_mgs
            except JSONDecodeError as e:
                response.failure("Response could not be decoded as JSON:" + str(e))
            except KeyError as k:
                response.failure("Response did not contain expected key: " + str(k))


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
        {"duration": 60, "users": 100, "spawn_rate": 10},  # spike the request to 100 at 1m
        {"duration": 120, "users": 200, "spawn_rate": 25},  # spike the request to 200 for 1m
        {"duration": 180, "users": 200, "spawn_rate": 25},  # stay at 200 request for 1m
        {"duration": 240, "users": 50, "spawn_rate": 10},  # reduce at 50 requests for 1m
        {"duration": 300, "users": 10, "spawn_rate": 5}  # reduce at 50 requests for 1m
    ]

    def tick(self):
        run_time = self.get_run_time()
        for stage in self.stages:
            if run_time < stage["duration"]:
                return stage["users"], stage["spawn_rate"]

        return None
