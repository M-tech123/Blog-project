from django.shortcuts import render, HttpResponse
from django.http import Http404
from .models import Post

# Create your views here.
def posts(request):
    posts = Post.objects.all()
    return render(request, 'blog/posts.html', {'posts': posts})


def post_detail(request, id):
    try:
        post = Post.objects.get(id=id, status=Post.Status.PUBLISHED)
    except Post.DoesNotExist:
        raise Http404("Post does not exist")
    return render(request, 'blog/post_detail.html', {'post': post})