from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
import json
from django.shortcuts import render
from django.urls import reverse
from django.core.paginator import Paginator
from django.views.decorators.csrf import csrf_exempt

from .models import *


def index(request):
  #get all posts
  posts = Post.objects.all().order_by('-date')
  paginator = Paginator(posts, 10) # Show 10 posts per page.
  page_number = request.GET.get('page')
  page_obj = paginator.get_page(page_number)

  return render(request, "network/index.html", {
    'page_obj': page_obj
  })


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

@login_required(login_url='login')
def new_post(request):
  if request.method == "POST":
    creator = request.user
    text = request.POST['new-post-text']
    
    #create and save new post using post model/object
    newPost = Post(creator=creator, text=text)
    newPost.save()

    return HttpResponseRedirect(reverse("index"))

def profile(request, username):
  #get user
  user = request.user
  #get user info of profile
  profile = User.objects.get(username=username)
  #get follower count
  followerCount = profile.followers.all().count()
  #get following count
  followingCount = profile.following.all().count()
  #get profile username
  profileUsername = profile.username
  
  #get all user posts to populate profile
  profilePosts = Post.objects.filter(creator=profile).order_by('-date')
  paginator = Paginator(profilePosts, 10) # Show 10 posts per page.
  page_number = request.GET.get('page')
  page_obj = paginator.get_page(page_number)

  if request.user.is_authenticated:
    #follow/unfollow button text
    if user.following.filter(username=username):
      followMessage = "Unfollow"
    else:
      followMessage = "Follow"

    return render(request, "network/profile.html", {
      "profileUsername": profileUsername,
      'page_obj': page_obj,
      "followerCount": followerCount,
      "followingCount": followingCount,
      "followMessage": followMessage
    })
  else:
    return render(request, "network/profile.html", {
      "profileUsername": profileUsername,
      'page_obj': page_obj,
      "followerCount": followerCount,
      "followingCount": followingCount,
    })

def follow_unfollow(request, username):
  if request.method == "POST":
    #get user and profile to be followed/unfollowed
    user = request.user
    profile = User.objects.get(username=username)

    if user.following.filter(username=username):
      user.following.remove(profile)
    else:
      user.following.add(profile)

  return HttpResponseRedirect(reverse("profile", args=(username,)))

@login_required(login_url='login')
def following(request):
  user = request.user
  #get all profiles user is following
  following = user.following.all()
  
  #get all posts from profiles the user is following
  posts = Post.objects.filter(creator__in=following).order_by('-date')
  paginator = Paginator(posts, 10) # Show 10 posts per page.
  page_number = request.GET.get('page')
  page_obj = paginator.get_page(page_number)


  return render(request, "network/following.html", {
    'page_obj': page_obj
  })

@csrf_exempt
@login_required(login_url='login')
def edit_post(request, postId):
  # print(f"FROM DJANGO PARAMETER:{postId}")
  user = request.user
  post = Post.objects.get(pk=postId)

  # make sure post creator is the same as user trying to edit post
  if user.username == post.creator.username:
    data = json.loads(request.body)
    updatedPostText = data.get('postText')
    post.text = updatedPostText
    post.save()
    # data.get('postId')
    return JsonResponse({"response": "Post updated and saved."})
  else:
    return JsonResponse({"response": "You are not the post creator. You can't edit this post."})


