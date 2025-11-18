from locust import HttpUser, task, between

from locust import HttpUser, task, between
from django.views.decorators.csrf import csrf_exempt


class RegularUser(HttpUser):
    wait_time = between(1, 5)

    def on_start(self):
        self.login()

    def login(self):
        # Авторизация юзера
        response = self.client.post("/users/login", data={
            "username": "pahenko",
            "password": "Patreon41"
        }, allow_redirects=True)
        print("Login RegularUser:", response.status_code)

    @task(3)
    def view_main_page(self):
        self.client.get("/users/main_page")

    @task(2)
    def view_post_detail(self):
        self.client.get("/users/post_detail/1/")

    @task(1)
    def like_post(self):
        self.client.post(
            "/users/post_detail/1/like/",
            data={},
            name="[POST] Toggle Post Like"
        )

    @task(1)
    def comment_post(self):
        self.client.post("/users/post_detail/1/", data={
            "content": "Nice post from RegularUser!"
        })


class BloggerUser(HttpUser):
    wait_time = between(1, 5)

    def on_start(self):
        self.login()

    def login(self):
        response = self.client.post("/users/login", data={
            "username": "parasiuk_oleg",
            "password": "Imbapas1#"
        }, allow_redirects=True)
        print("Login BloggerUser:", response.status_code)

    @task(3)
    def view_blogger_posts_detail(self):
        self.client.get("/users/ blogger_posts_detail/1/")  # исправлен пробел

    @task(2)
    def create_post(self):
        self.client.post("/users/create_post", data={
            "title": "Test Post from Blogger",
            "content": "Some content here"
        })

    @task(1)
    def my_posts(self):
        self.client.get("/users/my_posts/")

    @task(1)
    def like_post(self):
        self.client.post(
            "/users/post_detail/1/like/",
            data={},
            name="[POST] Toggle Post Like"
        )

    @task(1)
    def comment_post(self):
        self.client.post("/users/post_detail/1/", data={
            "content": "Nice post from Blogger!"
        })

    @task(1)
    def delete_post(self):
        self.client.post("/delete/1/")
