from django.shortcuts import render
from .serializers import PostSeriazizer
from .models import Post, Comment
from .templates.blog.forms import PostForm, CommentForm, PostSendForm
from django.utils import timezone
from django.shortcuts import render, get_object_or_404
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from autoslug import AutoSlugField
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.mail import send_mail
from rest_framework.response import Response
from rest_framework.views import APIView


def paginate(posts, request, num):
    paginator = Paginator(posts, num)
    page = request.GET.get("page")
    try:
        posts = paginator.page(page)
        return posts
    except PageNotAnInteger:
        posts = paginator.page(1)
        return posts
    except EmptyPage:
        return posts
        posts = paginator.page(paginator.num_pages)
    

class PostView(APIView):
    def get(self, request):
        posts = Post.objects.all()
        serializer = PostSeriazizer(posts, many=True)
        return Response({'posts': serializer.data})
    
    def post(self, request):
        post_article = request.data.get('post_article')
        serializer = PostSeriazizer(data=post_article)
        if serializer.is_valid(raise_exception=True):
            post_saved = serializer.save()
        return Response({"success": "Post '{}' created successfully".format(post_saved.title)})
    
    def put(self, request, id):
        saved_post = get_object_or_404(Post.objects.all(), id=id)
        data = request.data.get('post_article')
        serializer = PostSeriazizer(instance=saved_post, data=data, partial=True)
        if serializer.is_valid(raise_exception=True):
            post_saved = serializer.save()
        return Response({"success": "Post '{}' updated successfully".format(post_saved.title)})


def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by("-published_date")
    posts = paginate(posts, request, 3)
    return render(request, "blog/post_list.html", {"posts": posts})


def post_list_theme(request, theme):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by("published_date")
    posts = posts.filter(theme=theme)
    return render(request, "blog/post_list.html", {"posts": posts})


def post_detail(request, id):
    post = get_object_or_404(Post, id=id)
    return render(request, "blog/post_detail.html", {"post": post})


@login_required
def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect("post_detail", id=post.id)
    else:
        form = PostForm()
    return render(request, "blog/post_edit.html", {"form": form})


@login_required
def post_edit(request, id):
    post = get_object_or_404(Post, id=id)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect("post_detail", id=post.id)
    else:
        form = PostForm(instance=post)
    return render(request, "blog/post_edit.html", {"form": form})


@login_required
def post_draft_list(request):
    posts = Post.objects.filter(published_date__isnull=True).order_by("created_date")
    return render(request, "blog/post_draft_list.html", {"posts": posts})


@login_required
def post_publish(request, id):
    post = get_object_or_404(Post, id=id)
    post.publish()
    return redirect("post_detail", id=id)


@login_required
def post_remove(request, id):
    post = get_object_or_404(Post, id=id)
    post.delete()
    return redirect("post_list")


def add_comment_to_post(request, id):
    post = get_object_or_404(Post, id=id)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            return redirect("post_detail", id=post.id)
    else:
        form = CommentForm()
    return render(request, "blog/add_comment_to_post.html", {"form": form})


@login_required
def comment_approve(request, id):
    comment = get_object_or_404(Comment, id=id)
    comment.approve()
    return redirect("post_detail", id=comment.post.id)


@login_required
def comment_remove(request, id):
    comment = get_object_or_404(Comment, id=id)
    comment.delete()
    return redirect("post_detail", id=comment.post.id)


def post_share(request, id):
    # retrieving article by id
    post = get_object_or_404(Post, id=id)
    sent = False
    if request.method == "POST":
        # now form is saved
        form = PostSendForm(request.POST)
        # validate each row (depends on used forms.method while creating row)
        if form.is_valid():
            cd = form.cleaned_data 
            post_url = request.build_absolute_uri(post.id)
            subject = '{} ({}) recommends you reading "{}"'.format(
                cd["name"], cd["email"], post.title
            )
            message = 'Read "{}" at {}\n\n{}\'s comments:{}'.format(
                post.title, post_url, cd["name"], cd["comments"]
            )
            send_mail(subject, message, "biggreen.rm@gmail.com", [cd["to"]])
            sent = True
            return redirect("post_detail", id=post.id)
    else:
        form = PostSendForm()
        return render(
            request, "blog/share.html", {"post": post, "form": form, "sent": sent}
        )
