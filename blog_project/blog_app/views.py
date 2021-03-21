from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib import auth, messages
from .models import *
from django.utils import timezone

# Create your views here.


def register(request):
    if request.user.is_authenticated or request.user.is_staff:
        auth.logout(request)
        return redirect('login')
    if request.method == 'POST':
        name = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        obj = User.objects.filter(email=email)
        count = 0
        for i in obj:
            count += 1
        if count == 0:
            print('ys')
            User.objects.create_user(username=email, password=password, email=email, first_name=name)
            messages.error(request, 'Successfully Registered, login now!', extra_tags='user')
            return redirect('login')
        else:
            messages.error(request, 'Email Already Registered, Please try to login!', extra_tags='user')
    return render(request, 'register.html')


def login(request):
    if request.user.is_authenticated or request.user.is_staff:
        auth.logout(request)
        return redirect('login')
    if request.method == 'POST':
        email = request.POST['username']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        if password != '':
            if password == confirm_password:
                user = auth.authenticate(request, username=email, password=password)
                if user is not None:
                    auth.login(request, user)
                    return redirect('home')
                else:
                    messages.error(request, 'Invalid credentials!', extra_tags='user')
                    return redirect('login')
            else:
                messages.error(request, 'password should match!', extra_tags='user')
                return redirect('login')
        else:
            messages.error(request, 'Password cannot be empty!', extra_tags='user')
            return redirect('login')
    return render(request, 'login.html')


def blog_home(request):
    if not request.user.is_authenticated or request.user.is_staff:
        return redirect('login')
    blogs = Blog.objects.all().order_by('uploaded_on')
    blogs = blogs[::-1]
    count = 0
    for i in blogs:
        count += 1
    category = Category.objects.all()
    return render(request, 'home.html', {'blogs': blogs, 'categories': category, 'count': count})


def add_blog(request):
    if not request.user.is_authenticated or request.user.is_staff:
        return redirect('login')
    if request.method == "POST":
        user = request.user
        print(user)
        title = request.POST['title']
        content = request.POST['content']
        category = request.POST.get('category')
        Blog.objects.create(title=title, text=content, uploaded_by=user, category=Category.objects.get(category=category))
    return redirect('home')


def edit_blog(request, pk):
    if not request.user.is_authenticated or request.user.is_staff:
        return redirect('login')
    if request.method == "POST":
        blog = Blog.objects.get(id=pk)
        user = request.user.first_name
        title = request.POST['title']
        content = request.POST['content']
        category = request.POST.get('category')
        blog.title = title
        blog.text = content
        blog.edited_by = user
        blog.edited_on = timezone.now()
        blog.category = Category.objects.get(category=category)
        blog.save()
    return redirect('home')


def blog_detail(request, pk):
    if not request.user.is_authenticated or request.user.is_staff:
        return redirect('login')
    blog = Blog.objects.get(id=pk)
    if request.method == "POST":
        blog = Blog.objects.get(id=pk)
        user = request.user.first_name
        title = request.POST['title']
        content = request.POST['content']
        blog.title = title
        blog.text = content
        blog.edited_by = user
        blog.edited_on = timezone.now()
        blog.save()
    return render(request, 'blog_detail.html', {'blog': blog})


def logout(request):
    auth.logout(request)
    return redirect('login')

# navigation page view:


def navigation(request):
    return render(request, 'navigation.html')


# admin views:


def admin_panel(request):
    if not request.user.is_staff:
        return redirect('admin_login')
    users = User.objects.filter(is_staff=False)
    print(users)
    return render(request, 'admin_panel.html', {'users': users})


def category(request):
    if not request.user.is_staff:
        return redirect('admin_login')
    categories = Category.objects.all()
    count = 0
    for i in categories:
        count += 1
    print(categories)
    return render(request, 'categories.html', {'categories': categories, 'count': count})


def blog(request):
    if not request.user.is_staff:
        return redirect('admin_login')
    blogs = Blog.objects.all()
    count = 0
    for i in blogs:
        count += 1
    return render(request, 'blogs.html', {'blogs': blogs, 'count': count})


def admin_blog(request, pk):
    if not request.user.is_staff:
        return redirect('admin_login')
    blog = Blog.objects.get(id=pk)
    print(blog)
    return render(request, 'admin_blog.html', {'blog': blog})


def delete_blog(request, pk):
    if not request.user.is_staff:
        return redirect('admin_login')
    blog = Blog.objects.get(id=pk)
    blog.delete()
    return redirect('blog')


def delete_category(request, pk):
    if not request.user.is_staff:
        return redirect('admin_login')
    category = Category.objects.get(id=pk)
    category.delete()
    return redirect('category')


def user_specific_blog(request, pk):
    if not request.user.is_staff:
        return redirect('admin_login')
    user = User.objects.get(id=pk)
    blogs = Blog.objects.filter(uploaded_by=user)
    count = 0
    for i in blogs:
        count += 1
    return render(request, 'user_specific_blog.html', {'blogs': blogs, 'user': user, 'count': count})


def add_category(request):
    if not request.user.is_staff:
        return redirect('admin_login')
    if request.method == "POST":
        category = request.POST['category']
        Category.objects.create(category=category)
    return redirect('category')


def admin_login(request):
    if not request.user.is_staff or request.user.is_staff:
        auth.logout(request)
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        if password != '':
            if password == confirm_password:
                user = auth.authenticate(request, username=username, password=password)
                if user is not None and user.is_staff:
                    auth.login(request, user)
                    messages.success(request, 'Successfully logged in!', extra_tags='admin')
                    return redirect('admin_panel')
                else:
                    messages.error(request, 'Invalid credentials!', extra_tags='admin')
                    return redirect('admin_login')
            else:
                messages.error(request, 'password should match!', extra_tags='admin')
                return redirect('admin_login')
        else:
            messages.error(request, 'Password cannot be empty!', extra_tags='admin')
            return redirect('admin_login')
    return render(request, 'admin_login.html')
