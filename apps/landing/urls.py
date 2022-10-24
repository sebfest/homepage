from django.urls import path

from landing import views

app_name = 'landing'
urlpatterns = [
    path(
        '',
        views.WelcomeView.as_view(),
        name='welcome'
    ),
    path(
        'disclaimer/',
        views.DisclaimerView.as_view(),
        name='disclaimer'
    ),

]
