from django.urls import path, include
from users.views import *
from django.urls import path
from users import views as user_views
app_name = 'users'

urlpatterns = [
    path('register', user_views.register, name='register'),
    path('login', user_views.login, name='login'),
    path('admin_main', user_views.admin_main, name='admin_main'),
    path('main_page', user_views.main_page, name='main_page'),
    path('logout', user_views.logout_view, name='logout'),
    path('profile/', user_views.profile_view, name='profile'),
    path('my_posts/', user_views.my_posts_view, name='my_posts'),
    path('', include('posts.urls', namespace='users')),
]