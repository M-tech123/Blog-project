from django.shortcuts import render, HttpResponse, get_object_or_404, redirect
from django.http import Http404
from .models import Post
from django.core.paginator import Paginator
from django.core.paginator import EmptyPage, PageNotAnInteger
from django.views.generic import ListView
from .forms import EmailPostForm, CommentForm
from django.core.mail import send_mail
from django.views.decorators.http import require_POST

# Create your views here.
# def posts(request):
#     post_list = Post.objects.all()
#     paginator = Paginator(post_list, 2)
#     page_number = request.GET.get('page', 1)

#     try:
#         posts = paginator.get_page(page_number)
#     except PageNotAnInteger:
#         posts = paginator.get_page(1)
#     except EmptyPage:
#         posts = paginator.get_page(paginator.num_pages)
#     return render(request, 'blog/post/posts.html', {'posts': posts})


class PostListView(ListView):
    model = Post
    template_name = "blog/post/posts.html"
    context_object_name = "posts"
    paginate_by = 2


def post_detail(request, year, month, day, post):
    try:
        post = Post.objects.get(
            status=Post.Status.PUBLISHED,
            slug=post,
            publish__year=year,
            publish__month=month,
            publish__day=day,
        )
        comments = post.comments.filter(active=True)

        if request.method == "POST":
            form = CommentForm(request.POST)
            if form.is_valid():
                comment = form.save(commit=False)
                comment.post = post
                comment.save()
                return redirect(post.get_absolute_url())
        else:
            form = CommentForm()

    except Post.DoesNotExist:
        raise Http404("Post does not exist")
    return render(
        request,
        "blog/post/post_detail.html",
        {"post": post, "comments": comments, "form": form},
    )


def post_share(request, year, month, day, post):
    post = get_object_or_404(
        Post,
        slug=post,
        status=Post.Status.PUBLISHED,
        publish__year=year,
        publish__month=month,
        publish__day=day,
    )
    sent = False
    if request.method == "POST":
        form = EmailPostForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = f"{cd['name']} recommends you read {post.title}"
            message = (
                f"Read {post.title} at {post_url}\n\n"
                f"{cd['name']}'s comments: {cd['comments']}"
            )
            send_mail(subject, message, "ms505351@gmail.com", [cd["to"]])
            sent = True
    else:
        form = EmailPostForm()
    return render(
        request, "blog/post/share.html", {"form": form, "post": post, "sent": sent}
    )


@require_POST
def post_comment(request, year, month, day, post):
    post = get_object_or_404(
        Post,
        slug=post,
        status=Post.Status.PUBLISHED,
        publish__year=year,
        publish__month=month,
        publish__day=day,
    )
    comment = None
    form = CommentForm(request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.post = post
        comment.save()
    return render(
        request,
        "blog/post/comment.html",
        {"form": form, "post": post, "comment": comment},
    )
