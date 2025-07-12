from django.urls import path, include
from . import views

app_name = "blog"

urlpatterns = [
    path("", views.PostListView.as_view(), name="post"),
    path(
        "<int:year>/<int:month>/<int:day>/<slug:post>",
        views.post_detail,
        name="post_detail",
    ),
    path(
        "<int:year>/<int:month>/<int:day>/<slug:post>/share/",
        views.post_share,
        name="post_share",
    ),
    path(
        "<int:year>/<int:month>/<int:day>/<slug:post>/comment/",
        views.post_comment,
        name="post_comment",
    ),
]
