from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("new_post", views.new_post, name="new_post"),
    path("profile/<int:user_id>", views.profile, name="profile"),
    path("unfollow_user", views.unfollow_user, name="unfollow_user"),
    path("follow_user", views.follow_user, name="follow_user"),
    path("following", views.following, name="following"),
    path("edit/<int:post_id>", views.edit_post, name="edit_post"),
    path("like_add/<int:post_id>", views.like_add, name="like_add"),
    path("like_remove/<int:post_id>", views.like_remove, name="like_remove"),
]
