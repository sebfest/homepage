from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.flatpages import views
from django.urls import path, include

from homepage import settings

urlpatterns = [
    path('', include('blog.urls')),
    path('', include('research.urls')),
    path('admin/', admin.site.urls),
    path('about/', views.flatpage, {'url': '/about/'}, name='about'),
    path('disclaimer/', views.flatpage, {'url': '/disclaimer/'}, name='disclaimer'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
