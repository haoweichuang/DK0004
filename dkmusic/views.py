from django.shortcuts import render, get_object_or_404, redirect
from .models import Post, Comment
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .form import UserRegistraionForm, AddPostForm, CommentForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Count


def index(request, genre=None):
    if genre:
        posts_list = Post.objects.filter(genre=genre, available=True)
    else:
        posts_list = Post.objects.filter(available=True)
    paginator = Paginator(posts_list, 5)
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    return render(request, 'index.html', {'posts':posts})


def register(request):
    if request.method == 'POST':
        user_form = UserRegistraionForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            return render(request, 'register_done.html', {"new_user": new_user})
    else:
        user_form = UserRegistraionForm()
    return render(request, 'register.html', {'user_form': user_form})


@login_required
def studio(request):
    user = User.objects.get(username=request.user.username)
    try:
        posts_list = Post.objects.filter(available=True, user=user)
    except:
        posts_list = []
    paginator = Paginator(posts_list, 5)
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    return render(request, 'my_studio.html', {'posts': posts, 'user':user})


@login_required
def addPost(request):
    if request.method == 'POST':
        add_post_form = AddPostForm(request.POST, request.FILES)
        if add_post_form.is_valid():
            obj = add_post_form.save(commit=False)
            obj.user = request.user
            obj.save()
            return render(request, 'add_post_done.html')
    else:
        add_post_form = AddPostForm()
    return render(request, 'add_post_form.html', {'add_post_form':add_post_form})


def detail(request, post_slug):
    post = get_object_or_404(Post, slug=post_slug)
    comments = Comment.objects.filter(available=True, post=post)
    return render(request, 'detail.html', {'post': post, 'comments': comments})


def about(request):
    return render(request, 'about.html')


@login_required
def comment(request, post_slug):
    post = get_object_or_404(Post, slug=post_slug)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.post = post   # 将这个评论关联到对应的歌曲
            obj.user = request.user  # 将这个评论关联到相对应的评论者
            obj.save()
            return redirect('dkmusic:detail', post_slug=post.slug)
    else:
        form = CommentForm()
    return render(request, 'comment.html', {'form': form, 'post': post} )


@login_required
def deletePost(request, post_slug):
    post = get_object_or_404(Post, slug=post_slug)
    if request.user == post.user:
        post.delete()
        return redirect("dkmusic:studio")
    else:
        raise PermissionError
        return redirect('/')


@login_required
def editDetail(request, post_slug):
    post = get_object_or_404(Post, slug=post_slug)
    comments = Comment.objects.filter(available=True, post=post)
    return render(request, 'detail_editable.html', {'post': post, 'comments': comments})


def popular(request):
    posts = Post.objects.filter(available=True).annotate(total_comments=Count('comments')).order_by('-total_comments')[:5]
    return render(request, 'popular.html', {'posts': posts})











