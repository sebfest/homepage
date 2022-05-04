from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.flatpages import views
from django.urls import path, include

import config.settings.base as settings

urlpatterns = [
    path('', views.flatpage, {'url': '/'}, name='welcome'),
    path('blog/', include('blog.urls')),
    path('research/', include('research.urls')),
    path('admin/', admin.site.urls),
    path('markdownx/', include('markdownx.urls')),
    path('disclaimer/', views.flatpage, {'url': '/disclaimer/'}, name='disclaimer'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
