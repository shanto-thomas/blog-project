from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .models import Post, Profile
from .serializers import PostSerializer, UserSerializer
from django.shortcuts import render, redirect, get_object_or_404


# Home page view
@login_required
def home(request):
    try:
        post_list = Post.objects.all()
        data=dict(post_data=post_list, users_id=request.user)
        return render(request, 'home.html', {'post_list': data})

    except Exception as e:
        return Response({'error': 'Something went wrong. Please try again later!'},
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR)


def login_view(request):
    try:
        return render(request, 'login.html')
    except Exception as e:
        return Response({'error': 'Something went wrong. Please try again later!'},
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR)


def signup_view(request):
    try:
        return render(request, 'signup.html')
    except Exception as e:
        return Response({'error': 'Something went wrong. Please try again later!'},
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@login_required
def post_view(request):
    try:
        return render(request, 'post.html')
    except Exception as e:
        return Response({'error': 'Something went wrong. Please try again later!'},
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@login_required
def logout_view(request):
    try:
        logout(request)
        return redirect('login')
    except Exception as e:
        return Response({'error': 'Something went wrong. Please try again later!'},
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# Signup view
@api_view(['POST'])
def signup(request):
    try:
        data = request.data
        user = User.objects.create_user(username=data['name'], password=data['password'], email=data['email'])
        Profile.objects.create(user=user)
        return redirect('login')
    except Exception as e:
        return Response({'error': 'Something went wrong. Please try again later!'},
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# Login view

@csrf_exempt
@api_view(['POST'])
def user_login(request):
    try:
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(username=username, password=password)
        if user:
            login(request, user)  # Django login
            return Response(UserSerializer(user).data)  # Return user data
        else:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({'error': 'Something went wrong. Please try again later!'},
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@login_required
@api_view(['GET'])
def user_profile_view(request):
    try:
        profile = Profile.objects.get(user=request.user)
        data = dict(username=profile.user.username, email=profile.user.email,
                    profile_picture=profile.profile_picture.url if profile.profile_picture else None)
        return render(request, 'profile.html', {'profile_data': data})
    except Exception as e:
        return Response({'error': 'Something went wrong. Please try again later!'},
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@login_required
def update_profile_view(request):
    try:
        profile = Profile.objects.get(user=request.user)

        if request.method == 'POST':
            username = request.POST.get('name')
            email = request.POST.get('email')
            profile_picture = request.FILES.get('file')

            # Update the user instance
            request.user.username = username
            request.user.email = email
            request.user.save()

            # Update the profile instance
            if profile_picture:
                profile.profile_picture = profile_picture
            profile.save()

            return redirect('home')

        return render(request, 'profile.html', {'profile_data': profile})
    except Exception as e:
        return Response({'error': 'Something went wrong. Please try again later!'},
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@login_required
@api_view(['GET'])
def get_post(request, post_id):
    try:
        post = Post.objects.get(id=post_id)
        data = dict(post=post, users_id=request.user)
        if post:
            return render(request, 'view_post.html', {'view_post': data})
        else:
            return redirect('home')
    except Exception as e:
        return Response({'error': 'Something went wrong. Please try again later!'},
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR)



@login_required
@api_view(['POST'])
def add_post(request):
    try:
        serializer = PostSerializer(data=request.data,
                                    context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({'error': 'Something went wrong. Please try again later!'},
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR)



@login_required
@api_view(['POST'])
def update_post(request, post_id):
    try:
        post = Post.objects.get(id=post_id)
        if post.author != request.user:
            return Response({'error': 'You are not the author'}, status=status.HTTP_403_FORBIDDEN)
        serializer = PostSerializer(post, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({'error': 'Something went wrong. Please try again later!'},
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@login_required
@api_view(['DELETE'])
def delete_post(request, post_id):
    try:
        post = get_object_or_404(Post, id=post_id)

        if post.author != request.user:
            return Response({'error': 'You are not the author'}, status=status.HTTP_403_FORBIDDEN)

        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    except Exception as e:
        return Response({'error': 'Something went wrong. Please try again later!'},
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR)
