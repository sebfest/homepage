from django.urls import path

from blog import views

app_name = 'blog'
urlpatterns = [
    path('', views.PostListView.as_view(), name='post_list'),
    path('post/<slug:slug>/', views.PostDetailView.as_view(), name='post_detail'),
    path('tag/<slug:slug>/', views.PostTagListView.as_view(), name='post_tag_list'),
    path('archive/', views.PostArchiveView.as_view(), name='post_archive'),
]
