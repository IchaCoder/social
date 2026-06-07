from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth import get_user_model, authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import FollowersCount, LikePost, Profile, Post

User = get_user_model()

# Create your views here.
@login_required(login_url='signin')
def index(request):
    profile_object = User.objects.get(username=request.user.username)
    profile_data = Profile.objects.get(user=profile_object)

    posts = Post.objects.all()
    context = {
        'user_profile': profile_data,
        'posts': posts
    }
    return render(request, 'index.html', context)

def like_post(request):
    username = request.user.username
    post_id = request.GET.get('post_id')
    post = Post.objects.get(id=post_id)
    like_filter = LikePost.objects.filter(post_id=post_id, username=username).first()

    if like_filter == None:
        new_like = LikePost.objects.create(post_id=post_id, username=username)
        new_like.save()
        post.no_of_likes += 1
        post.save()
        return redirect('/')
    else:
        like_filter.delete()
        post.no_of_likes -= 1
        post.save()
        return redirect('/')

@login_required(login_url='signin')
def upload(request):

    if request.method == 'POST':
        user = request.user.username
        image = request.FILES.get('image_upload')
        caption = request.POST.get('caption')

        new_post = Post.objects.create(user=user, image=image, caption=caption)
        new_post.save()

        return redirect('/')
    else:
        return redirect('/')

@login_required(login_url='signin')
def settings(request):
    profile = Profile.objects.get(user=request.user)
    context = {
        'user_profile': profile
    }

    if request.method == 'POST':
        if request.FILES.get('image') == None:
            image = profile.profileimg
            bio = request.POST.get('bio')
            location = request.POST.get('location')

            profile.profileimg = image
            profile.bio = bio
            profile.location = location
            profile.save()
        if request.FILES.get('image') != None:
            image = request.FILES.get('image')
            bio = request.POST.get('bio')
            location = request.POST.get('location')

            profile.profileimg = image
            profile.bio = bio
            profile.location = location
            profile.save()
    return render(request, 'setting.html', context)

@login_required(login_url='signin')
def profile(request, pk):
    user_object = User.objects.get(username=pk)
    user_profile = Profile.objects.get(user=user_object)
    user_posts = Post.objects.filter(user=pk)
    user_post_length = len(user_posts)
    
    follower = request.user.username
    user = pk

    if FollowersCount.objects.filter(follower=follower, user=user).first():
        button_text = 'Unfollow'
    else:
        button_text = 'Follow'

    user_followers = len(FollowersCount.objects.filter(user=pk))
    user_following = len(FollowersCount.objects.filter(follower=pk))

    context = {
        'user_object': user_object,
        'user_profile': user_profile,
        'user_posts': user_posts,
        'user_post_length': user_post_length,
        'button_text': button_text,
        'user_followers': user_followers,
        'user_following': user_following
    }
    return render(request, 'profile.html', context)
def signup(request):
    
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password == confirm_password:
           if User.objects.filter(username=username).exists():
                messages.info(request, 'Username already taken')
                return redirect('signup')
           elif User.objects.filter(email=email).exists():
                messages.info(request, 'Email already taken')
                return redirect('signup')
           else:
                user = User.objects.create_user(username=username, email=email, password=password)
                user.save()

                # log the user in and redirect to settings page
                user_login = authenticate(request, username=username, password=password)
                login(request, user_login)

                # Create a profile for the new user
                user_model = User.objects.get(username=username)
                profile = Profile(user=user_model, id_user=user_model.id)
                profile.save()
                return redirect('signup')
        else:
            messages.info(request, 'Passwords do not match')
            return redirect('signup')

    else:
        return render(request, 'signup.html')
    
def signin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            messages.info(request, 'Invalid credentials')
            return redirect('signin')
    else:
        return render(request, 'signin.html')
    
def follow(request):
    if request.method == 'POST':
        follower = request.POST.get('follower')
        user = request.POST.get('user')

        if FollowersCount.objects.filter(follower=follower, user=user).first():
            delete_follower = FollowersCount.objects.get(follower=follower, user=user)
            delete_follower.delete()
            return redirect('/profile/' + user)
        else:
            new_follower = FollowersCount.objects.create(follower=follower, user=user)
            new_follower.save()
            return redirect('/profile/' + user)
    else:
        return redirect('/')

@login_required(login_url='signin')
def logout_view(request):
    logout(request)
    return redirect('signin')

