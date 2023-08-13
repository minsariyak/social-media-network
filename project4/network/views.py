import json
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator

from .models import *

@login_required(login_url="login")
def index(request):
    all_posts = Post.objects.all().order_by("-dateCreated")
    paginator = Paginator(all_posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, "network/index.html", {
        "page_obj": page_obj
    })

@login_required(login_url="login")
def get_following_page(request):
    following = Following.objects.filter(user=request.user)
    users_following = []

    for follow in following:
        users_following.append(follow.following)

    posts = Post.objects.filter(user__in=users_following).order_by("-dateCreated")

    if following:
        lonely = False
    else:
        lonely = True

    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, "network/following.html", {
        "lonely": lonely,
        "page_obj": page_obj
    })

@login_required(login_url="login")
def get_profile(request, user_id):
    user = User.objects.get(pk=user_id)
    posts = Post.objects.filter(user=user).order_by("-dateCreated")
    followers = Follower.objects.filter(user=user)
    following = Following.objects.filter(user=user)
    total_followers = len(followers)
    total_following = len(following)

    owner = True
    follows = False

    if request.user != user:
        owner = False

    for follower in followers:
        if request.user == follower.follower:
            follows = True
            break

    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, "network/profile.html", {
        "followers": followers,
        "following": following,
        "total_followers": total_followers,
        "total_following": total_following,
        "user": user,
        "owner": owner,
        "follows": follows,
        "page_obj": page_obj
    })

@login_required(login_url="login")
def follow(request, user_id):
    logged_in_user = request.user
    following_user = User.objects.get(pk=user_id)

    new_following = Following(user=logged_in_user, following=following_user)
    new_following.save()
    new_follower = Follower(user=following_user, follower=logged_in_user)
    new_follower.save()

    return HttpResponseRedirect(reverse('profile', args=(user_id,)))

@login_required(login_url="login")
def unfollow(request, user_id):
    logged_in_user = request.user
    following_user = User.objects.get(pk=user_id)

    update_following = Following.objects.get(user=logged_in_user, following=following_user)
    update_following.delete()

    update_follower = Follower.objects.get(user=following_user, follower=logged_in_user)
    update_follower.delete()

    return HttpResponseRedirect(reverse('profile', args=(user_id,)))

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")

@login_required(login_url="login")
def create_post(request):
    if request.method == 'POST':
        content = request.POST.get('content')
        new_post = Post(user=request.user, content=content)
        new_post.save()

        return HttpResponseRedirect(reverse("index"))


# *********************************************************************************************************************
# API Route Functions
# *********************************************************************************************************************

@login_required(login_url="login")
@csrf_exempt
def get_a_post(request, post_id):
    if request.method == 'GET':
        post = Post.objects.get(pk=post_id)

        return JsonResponse(post.serialize(), safe=False)

    elif request.method == 'PUT':
        data = json.loads(request.body)
        post_id = data.get('post_id')
        new_content = data.get('new_content')

        post = Post.objects.get(pk=post_id)
        post.content = new_content
        post.save()

        return JsonResponse({"message": "Post edited successfully"}, status=201)

@login_required(login_url="login")
@csrf_exempt
def get_total_likes(request, post_id):
    post = Post.objects.get(pk=post_id)
    likes = Like.objects.filter(post=post)

    liked = False
    for like in likes:
        if request.user == like.user:
            liked = True
            break

    return JsonResponse({"total_likes": len(likes), "liked": liked}, safe=False)

@login_required(login_url="login")
@csrf_exempt
def add_like(request):
    if request.method == "POST":
        data = json.loads(request.body)
        post_id = data.get('post_id')
        post = Post.objects.get(pk=post_id)
        new_like = Like(user=request.user, post=post)
        new_like.save()

        return JsonResponse({"message": "Post liked successfully"}, status=201)

    elif request.method == 'PUT':
        data = json.loads(request.body)
        post_id = data.get('post_id')
        post = Post.objects.get(pk=post_id)
        like = Like.objects.get(user=request.user, post=post)
        like.delete()

        return JsonResponse({"message": "Post unliked successfully"}, status=201)