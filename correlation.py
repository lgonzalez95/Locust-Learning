"""
extracting the dynamic value from response
pass the extracted value in the subsequent requests
Use: Regular expressions, or parsers
"""

from locust import HttpUser, SequentialTaskSet, task, constant, log
import re
import random


class PetStore(SequentialTaskSet):
    def __init__(self, parent):
        super().__init__(parent)
        self.jsession = ""
        self.random_product = ""

    # @task
    # def home_page(self):
    #     with self.client.get('', catch_response=True, name='Home Page') as response:
    #         if 'Welcome to JPetStore 6' in response.text and response.elapsed.total_seconds() < 2.0:
    #             response.success()
    #         else:
    #             response.failure('Home page took too long to load and/or the text check has failed.')
    #         print("Home")

    @task
    def enter_store(self):
        products = ['Fish', 'Cats', 'Dogs', 'Reptiles', 'Birds']
        with self.client.get('/actions/Catalog.action', catch_response=True, name='Actions') as response:
            for product in products:
                if product in response.text:
                    response.success()
                else:
                    response.failure()

            try:
                jsession = re.search(r'jsessionid=(.+?)\?', response.text)  # Extracting the jsession id
                self.jsession = jsession.group(1)
            except:
                self.jsession = ''

            print(self.jsession)


# @task
# def signin_page(self):
#     self.client.cookies.clear()
#     url = "/actions/Account.action;jsessionid=" + self.jsession + "?signonForm="
#     with self.client.get(url, catch_response=True, name="T20_SignInPage") as response:
#         if "Please enter your username and password." in response.text:
#             response.success()
#         else:
#             response.failure("Sign in page check failed")
#
# @task
# def login(self):
#     self.client.cookies.clear()
#     url = "/actions/Account.action"
#     data = {
#         "username": "j2ee",
#         "password": "j2ee",
#         "signon": "Login"
#     }
#     with self.client.post(url, name="T30_SignIn", data=data, catch_response=True) as response:
#         # print(response.text)
#         if "Welcome ABC!" in response.text:
#             response.success()
#             try:
#                 random_product = re.findall(r"Catalog.action\?viewCategory=&categoryId=(.+?)\"",
#                                             response.text)  # Extracting all the products
#                 self.random_product = random.choice(random_product)  # Storing the random product
#             except AttributeError:
#                 self.random_product = ""
#         else:
#             response.failure("Sign in Failed")
#
# @task
# def random_product_page(self):
#     url = "/actions/Catalog.action?viewCategory=&categoryId=" + self.random_product
#     name = "T40_" + self.random_product + "_Page"
#     with self.client.get(url, name=name, catch_response=True) as response:
#         if self.random_product in response.text:
#             response.success()
#         else:
#             response.failure("Product page not loaded")
#
# @task
# def sign_out(self):
#     with self.client.get("/actions/Account.action?signoff=", name="T50_SignOff", catch_response=True) as response:
#         if response.status_code == 200:
#             response.success()
#         else:
#             response.failure("Log off failed")
#     self.client.cookies.clear()


class LoadTest(HttpUser):
    host = "https://petstore.octoperf.com"
    wait_time = constant(1)
    tasks = [PetStore]
