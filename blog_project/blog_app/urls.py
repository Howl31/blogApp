"""blog_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('home', views.blog_home, name='home'),
    path('add_blog/', views.add_blog, name='add_blog'),
    path('edit_blog/<int:pk>/', views.edit_blog, name='edit_blog'),
    path('blog_detail/<int:pk>/', views.blog_detail, name='blog_detail'),
    path('', views.navigation, name='navigation'),
    # Admin Panel Url
    path('admin_panel/', views.admin_panel, name='admin_panel'),
    path('category/', views.category, name='category'),
    path('blog/', views.blog, name='blog'),
    path('admin_blog/<int:pk>/', views.admin_blog, name='admin_blog'),
    path('delete_blog/<int:pk>/', views.delete_blog, name='delete_blog'),
    path('delete_category/<int:pk>/', views.delete_category, name='delete_category'),
    path('user_specific_blog/<int:pk>/', views.user_specific_blog, name='user_specific_blog'),
    path('add_category/', views.add_category, name='add_category'),
    path('admin_login/', views.admin_login, name='admin_login'),
]
