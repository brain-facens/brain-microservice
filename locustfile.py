from locust import HttpUser, task 

class LoginTest(HttpUser):
    @task 
    def adminLogin(self):
        self.client.post("/auth/admin/login", json={"username": "admin", "password": "admin"})