from django.urls import path

from . import views

app_name = 'research'
urlpatterns = [
    path('research/', views.ResearchView.as_view(), name='research'),
]
