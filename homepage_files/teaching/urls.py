from django.urls import path

from . import views

app_name = 'teaching'
urlpatterns = [
    path('teaching/', views.TeachingView.as_view(), name='teaching'),
]
