
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create_post", views.create_post, name="create_post"),
    path("profile/<int:user_id>", views.get_profile, name="profile"),
    path("follow/<int:user_id>", views.follow, name="follow"),
    path("unfollow/<int:user_id>", views.unfollow, name="unfollow"),
    path("following", views.get_following_page, name="following"),

    # API routes
    path("posts/<int:post_id>", views.get_a_post, name="get_a_post"),
    path("likes", views.add_like, name="add_like"),
    path("likes/<int:post_id>", views.get_total_likes, name="get_total_likes")
]
