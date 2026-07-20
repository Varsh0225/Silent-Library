from locust import HttpUser, TaskSet, task, between

class UserTasks(TaskSet):
    @task(1) 
    def index_page(self):
        self.client.get("/")

    @task(3)
    def signup(self):
        self.client.get("/signup")

class WebsiteUser(HttpUser):
    wait_time = between(5, 15)
    task = [UserTasks]
    host = "http://127.0.0.1:8000"

# from locust import HttpUser, task, between

# class WebsiteUser(HttpUser):
#     wait_time = between(1, 2)

#     @task
#     def home(self):
#         self.client.get("/")

#     @task
#     def search_books(self):
#         self.client.get("/search/")