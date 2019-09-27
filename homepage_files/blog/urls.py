from django.urls import path

from blog import views, feed

app_name = 'blog'
urlpatterns = [
    path('', views.PostListView.as_view(), name='post_list'),
    path('tag/<slug:slug>/', views.PostTagListView.as_view(), name='post_tag_list'),
    path('post/<slug:slug>/', views.PostDetailView.as_view(), name='post_detail'),
    path('feed/', feed.PostFeed(), name='post_feed'),
]
