# muti request test api

from locust import HttpUser, task

class AdminTest(HttpUser):
    @task
    def adminLogin(self):
        self.client.post("/auth/admin/login", json={"username": "admin", "password": "admin"})

class ClientTest(HttpUser):
    @task
    def clientLogin(self):
        self.client.post("/auth/client/login", json={"username": "eduardo", "password": "@op93001"})

class DemoTest(HttpUser):
    @task
    def demoLogin(self):
        self.client.post("/auth/demo/login", json={"username": "eduardo", "password": "@op93001"})