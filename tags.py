"""
@tag('get', 'invalid')
--tags
--exclude-tags
"""

from locust import task, constant, SequentialTaskSet, FastHttpUser, tag
from json import JSONDecodeError


class MyScript(SequentialTaskSet):
    @task
    @tag('Invalid')
    def login_missing_pass(self):
        expected_response = 'Missing email or username'
        with self.client.post('/api/login', catch_response=True, name='Missing data') as response:
            result = True if expected_response in response.text else False
            response.success() if result else response.failure('Got invalid response')

    @task
    @tag('Valid')
    def login_valid(self):
        payload = {"email": "eve.holt@reqres.in", "password": "cityslicka"}
        with self.client.post('/api/login', json=payload, catch_response=True, name='Valid login') as response:
            try:
                if not response.json()["token"]:
                    response.failure("Did not get a value in the token field")
            except JSONDecodeError:
                response.failure("Response could not be decoded as JSON")
            except KeyError:
                response.failure("Response did not contain expected key 'greeting'")


class LoadTest(FastHttpUser):
    host = "https://reqres.in"
    tasks = [MyScript]
    wait_time = constant(1)
