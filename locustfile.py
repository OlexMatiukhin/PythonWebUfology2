from locust import HttpUser, SequentialTaskSet, task, between


class RegularUserFlow(SequentialTaskSet):

    def on_start(self):
        self.login()

    def login(self):
        response = self.client.post("users/login", data={
            "username": "pahenko",
            "password": "Patreon41"
        })
        print("Login RegularUser:", response.status_code)

    @task
    def view_main_page(self):
        self.client.get("users/main_page")

    @task
    def view_post_detail(self):
        self.client.get("users/post_detail/1/")

    @task
    def like_post(self):
        self.client.post(
            "users/post_detail/1/like/",
            data={},
            name="[POST] Toggle Post Like"
        )

    @task
    def comment_post(self):
        self.client.post("users/post_detail/1/", data={
            "content": "Nice post from RegularUser!"
        })
        self.interrupt()


class BloggerUserFlow(SequentialTaskSet):

    def on_start(self):
        self.client.get("users/logout")
        self.login()
        self.post_id = None

    def login(self):
        response = self.client.post("users/login", data={
            "username": "parasiuk_oleg",
            "password": "Imbapas1#"
        })
        print("Login BloggerUser:", response.status_code)

    @task
    def create_post(self):
        response = self.client.post("users/create_post", data={
            "title": "Test Post from Blogger",
            "content": "Some content here"
        })

        if response.status_code in (200, 201):
            try:
                self.post_id = response.json().get("id")
            except:
                print("WARNING: create_post returned HTML instead of JSON.")

    @task
    def view_post_detail(self):
        if self.post_id:
            self.client.get(f"users/blogger_posts_detail/{self.post_id}/")

    @task
    def like_post(self):
        if self.post_id:
            self.client.post(
                f"users/post_detail/{self.post_id}/like/",
                data={},
                name="[POST] Toggle Post Like"
            )

    @task
    def comment_post(self):
        if self.post_id:
            self.client.post(
                f"users/post_detail/{self.post_id}/",
                data={"content": "Nice post from Blogger!"}
            )

    @task
    def my_posts(self):
        self.client.get("users/my_posts/")

    @task
    def delete_post(self):
        if self.post_id:
            self.client.post(f"/delete/{self.post_id}/")
            self.post_id = None
        self.interrupt()



class RegularUser(HttpUser):
    tasks = [RegularUserFlow]
    wait_time = between(1, 2)


class BloggerUser(HttpUser):
    tasks = [BloggerUserFlow]
    wait_time = between(1, 2)
