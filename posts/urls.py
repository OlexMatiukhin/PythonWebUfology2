from django.urls import path
from users.views import *
from django.urls import path
from users import views as user_views
app_name = 'posts'
from posts.views import *
urlpatterns = [
    path('create_post', create_post, name='create_post'),
    path('post_detail/<int:pk>/', post_detail_view, name='post_detail'),
    path(' blogger_posts_detail/<int:pk>/', blogger_posts_detail_view, name='blogger_posts_detail'),
    path('delete/<int:post_id>/', delete_post_view, name='delete_post'),

    path('post_detail/<int:pk>/like/',toggle_post_like_view, name='toggle_post_like'),
    path('post_detail/<int:pk>/dislike/', toggle_post_dislike_view, name='toggle_post_dislike'),

    path('comment/<int:comment_id>/like/', toggle_comment_like_view, name='toggle_comment_like'),
    path('comment/<int:comment_id>/dislike/', toggle_comment_dislike_view, name='toggle_comment_dislike'),

]