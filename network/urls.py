
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("new-post", views.new_post, name="new-post"),
    path("profile/<str:username>", views.profile, name="profile"),
    path("follow-unfollow/<str:username>", views.follow_unfollow, name="follow-unfollow"),
    path("following", views.following, name="following"),
    # routes using javascript
    path("edit-post/<int:postId>", views.edit_post, name="edit-post"),
    path("like-post/<int:postId>", views.like_post, name="like-post")
]
