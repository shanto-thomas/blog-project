"""
URL configuration for blog_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

from blog.views import signup, user_login, \
    add_post, delete_post, home, login_view, signup_view, update_profile_view, user_profile_view, \
    post_view, logout_view, get_post, update_post

urlpatterns = [
    path('admin/', admin.site.urls),
    path('home', home, name='home'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('signup/', signup_view, name='signup'),
    path('post-blogs/', post_view, name='post-blogs'),
    # path('add-post/', add_post_view, name='add_post'),
    path('profile/', user_profile_view, name='user_profile'),
    path('update-profile/', update_profile_view, name='update_profile'),

    path('api/user_login/', user_login, name='user_login'),
    path('api/signup_user/', signup, name='signup_user'),
    path('api/view-posts/<int:post_id>/', get_post, name='view_posts'),
    path('api/update-posts/<int:post_id>/', update_post, name='update_post'),
    path('api/adding-posts/', add_post, name='adding-posts'),
    path('api/delete-post/<int:post_id>/', delete_post, name='delete_post'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
