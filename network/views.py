from django.contrib.auth import authenticate, login, logout
from django.core.paginator import Paginator
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
import json

from .models import User, Post, Follows, Likes






def like_remove(request, post_id):
    post = Post.objects.get(pk=post_id)
    user = User.objects.get(pk=request.user.id)
    like = Likes.objects.filter(user_like=user, post_like=post)
    like.delete()
    return JsonResponse({"message": "like removed successfully"})



def like_add(request, post_id):
    post = Post.objects.get(pk=post_id)
    user = User.objects.get(pk=request.user.id)
    like_new = Likes(user_like=user, post_like=post)
    like_new.save()
    return JsonResponse({"message": "like add successfully"})






def edit_post(request, post_id):
    if request.method == "POST":
        data = json.loads(request.body)
        post_edit = Post.objects.get(pk=post_id)
        post_edit.content = data["content"]
        post_edit.save()
        return JsonResponse({"message": "edit successfully", "data": data["content"]})

def index(request):
    all_posts = Post.objects.all().order_by("id").reverse()

    # render on pagination
    paginator = Paginator(all_posts, 5)
    number_of_page = request.GET.get("page")
    all_posts_per_page = paginator.get_page(number_of_page)

    all_likes = Likes.objects.all()

    who_you_liked = []
    try:
        for like in all_likes:
            if like.user.id == request.user.id:
                who_you_liked.append(like.post.id)

    except:
        who_you_liked = []







    return render(request, "network/index.html", {
        "all_posts": all_posts,
        "all_posts_per_page": all_posts_per_page,
        "who_you_liked": who_you_liked,


    })

def new_post(request):
    if request.method == "POST":
        content = request.POST["content"]
        user = User.objects.get(pk=request.user.id)
        post = Post(content=content, user=user)
        post.save()
        return HttpResponseRedirect(reverse("index"))


def profile(request, user_id):
    user = User.objects.get(pk=user_id)
    all_posts = Post.objects.filter(user=user).order_by("id").reverse()

    who_following = Follows.objects.filter(user=user)
    who_follower = Follows.objects.filter(follower_user=user)

    try:
        check_follow = who_follower.filter(user=User.objects.get(pk=request.user.id))
        if len(check_follow) != 0:
            is_following = True
        else:
            is_following = False
    except:
        is_following = False


    # render on pagination
    paginator = Paginator(all_posts, 5)
    number_of_page = request.GET.get("page")
    all_posts_per_page = paginator.get_page(number_of_page)

    return render(request, "network/profile.html", {
        "all_posts": all_posts,
        "all_posts_per_page": all_posts_per_page,
        "username": user.username,
        "who_following": who_following,
        "who_follower": who_follower,
        "is_following": is_following,
        "profile_user": user

    })

def following(request):
    current_user = User.objects.get(pk=request.user.id)
    following_people = Follows.objects.filter(user=current_user)
    all_posts = Post.objects.all().order_by("id").reverse()
    following_posts = []

    for post in all_posts:
        for person in following_people:
            if person.follower_user == post.user:
                following_posts.append(post)

    # render on pagination
    paginator = Paginator(following_posts, 5)
    number_of_page = request.GET.get("page")
    all_posts_per_page = paginator.get_page(number_of_page)

    return render(request, "network/following.html", {
        "all_posts_per_page": all_posts_per_page,

    })



def follow_user(request):
    user_follow = request.POST["user_follow"]
    current_user = User.objects.get(pk=request.user.id)
    user_follow_data = User.objects.get(username=user_follow)
    follow = Follows(user=current_user, follower_user=user_follow_data)
    follow.save()
    user_id = user_follow_data.id
    return HttpResponseRedirect(reverse(profile, kwargs={'user_id': user_id}))

def unfollow_user(request):
    user_follow = request.POST["user_follow"]
    current_user = User.objects.get(pk=request.user.id)
    user_follow_data = User.objects.get(username=user_follow)
    follow = Follows.objects.get(user=current_user, follower_user=user_follow_data)
    follow.delete()
    user_id = user_follow_data.id
    return HttpResponseRedirect(reverse(profile, kwargs={'user_id': user_id}))

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