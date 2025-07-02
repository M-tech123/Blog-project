from django.shortcuts import render, HttpResponse
from django.http import Http404
from .models import Post


# Create your views here.
def posts(request):
    posts = Post.objects.all()
    return render(request, 'blog/posts.html', {'posts': posts})


def post_detail(request, year, month, day, post):
    try:
        post = Post.objects.get(
            status=Post.Status.PUBLISHED,
            slug=post,
            publish__year=year,
            publish__month=month,
            publish__day=day
        )
    except Post.DoesNotExist:
        raise Http404("Post does not exist")
    return render(request, 'blog/post_detail.html', {'post': post})