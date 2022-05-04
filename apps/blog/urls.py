from django.urls import path

from blog import views

app_name = 'blog'
urlpatterns = [
    path(
        'posts/',
        views.PostListView.as_view(),
        name='post_list'
    ),
    path(
        'posts/<slug:slug>/',
        views.PostDetailView.as_view(),
        name='post_detail'
    ),
    path(
        'posts/tag/<slug:slug>/',
        views.PostTagListView.as_view(),
        name='post_tag_list'
    ),
    path(
        'posts/archive/',
        views.PostArchiveView.as_view(),
        name='post_archive'
    ),
]
