from django.shortcuts import render, HttpResponse, get_object_or_404
from django.http import Http404
from .models import Post
from django.core.paginator import Paginator
from django.core.paginator import EmptyPage, PageNotAnInteger
from django.views.generic import ListView
from .forms import EmailPostForm
from django.core.mail import send_mail

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
    template_name = 'blog/post/posts.html'
    context_object_name = 'posts'
    paginate_by = 2

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
    return render(request, 'blog/post/post_detail.html', {'post': post})


def post_share(request, post_id):
    post = get_object_or_404(Post,id=post_id,status=Post.Status.PUBLISHED)
    sent = False
    if request.method == 'POST':
        form = EmailPostForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = f"{cd['name']} recommends you read {post.title}"
            message = f"Read {post.title} at {post_url}\n\n" \
                        f"{cd['name']}'s comments: {cd['comments']}"
            send_mail(subject, message, 'ms505351@gmail.com', [cd['to']])
            sent = True
    else:
        form = EmailPostForm()
    return render(request, 'blog/post/share.html', {'form': form, 'post': post, 'sent': sent})