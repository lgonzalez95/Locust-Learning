from locust import HttpUser, constant, task


class MyReqRes(HttpUser):
    host = "https://reqres.in"
    wait_time = constant(1)

    @task
    def get_users(self):
        response = self.client.get("/api/users?page=2")
        print(response.status_code)
        assert response.status_code == 200

    @task
    def create_user(self):
        response = self.client.post("/api/users", data="""{"name":"morpheus","job":"leader"}""")
        print(response.status_code)
        assert response.status_code == 201
