from django.urls import path
from .views import post_comment_create, like_unlike_post

app_name = 'posts'

urlpatterns = [
    path('', post_comment_create, name="main-post"),
    path('liked', like_unlike_post, name="like-post")
]