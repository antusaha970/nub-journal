from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from .models import Blog
from .forms import RegisterForm, BlogForm


# ---------- Public ----------

def home(request):
    posts = Blog.objects.filter(status='published').order_by('-published_at')
    return render(request, 'blog/home.html', {'posts': posts})


def post_detail(request, slug):
    post = get_object_or_404(Blog, slug=slug, status='published')
    return render(request, 'blog/post_detail.html', {'post': post})


# ---------- Auth ----------

def register_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    form = RegisterForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = form.save()
        login(request, user)
        messages.success(request, f'Welcome, {user.username}!')
        return redirect('home')
    return render(request, 'blog/register.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        user = authenticate(
            request,
            username=request.POST.get('username'),
            password=request.POST.get('password'),
        )
        if user:
            login(request, user)
            return redirect('home')
        messages.error(request, 'Invalid username or password.')
    return render(request, 'blog/login.html')


def logout_view(request):
    logout(request)
    return redirect('home')


# ---------- Author (login required) ----------

@login_required
def my_posts(request):
    posts = Blog.objects.filter(user=request.user)
    return render(request, 'blog/my_posts.html', {'posts': posts})


@login_required
def post_create(request):
    form = BlogForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        post = form.save(commit=False)
        post.user = request.user
        post.save()
        messages.success(request, 'Post created successfully.')
        return redirect('my_posts')
    return render(request, 'blog/post_form.html', {'form': form, 'action': 'Create'})


@login_required
def post_edit(request, pk):
    post = get_object_or_404(Blog, pk=pk, user=request.user)
    form = BlogForm(request.POST or None, instance=post)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Post updated.')
        return redirect('my_posts')
    return render(request, 'blog/post_form.html', {'form': form, 'action': 'Edit', 'post': post})


@login_required
def post_delete(request, pk):
    post = get_object_or_404(Blog, pk=pk, user=request.user)
    if request.method == 'POST':
        post.delete()
        messages.success(request, 'Post deleted.')
        return redirect('my_posts')
    return render(request, 'blog/post_confirm_delete.html', {'post': post})


@login_required
def post_toggle_publish(request, pk):
    post = get_object_or_404(Blog, pk=pk, user=request.user)
    if request.method == 'POST':
        if post.status == 'draft':
            post.status = 'published'
            post.published_at = timezone.now()
        else:
            post.status = 'draft'
            post.published_at = None
        post.save()
    return redirect('my_posts')
