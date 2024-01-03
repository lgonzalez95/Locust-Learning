from locust import HttpUser, task, constant


class HelloWorld(HttpUser):
    wait_time = constant(1)
    host = 'https://www.google.com'

    @task
    def test(self):
        self.client.get('/')

# docker run -p 8089:8089 -v $PWD:/mnt/locust -d locustio/locust -f /mnt/locust/sample.py
# docker run -p 8089:8089 -v $PWD:/mnt/locust -d locustio/locust -f /mnt/locust/sample.py --html report.html --headless -r 1 -u 1 -t 10s
