from django.urls import path

from contact import views

app_name = 'contact'
urlpatterns = [
    path('contact/', views.ContactView.as_view(), name='contact'),
    path('thanks/', views.ThanksView.as_view(), name='thanks'),
]
