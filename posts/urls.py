from django.urls import path
from .views import post_comment_create, like_unlike_post, PostDeleteView, PostUpdateView


app_name = 'posts'


urlpatterns = [
    path('', post_comment_create, name="main-post"),
    path('liked', like_unlike_post, name="like-post"),
    path('<pk>/delete/', PostDeleteView.as_view(), name="post-delete"),
    path('<pk>/update/', PostUpdateView.as_view(), name="post-update"),
]
