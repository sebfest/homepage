from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path(
      '',
      include('landing.urls')
    ),
    path(
      'blog/',
      include('blog.urls')
    ),
    path(
      'research/',
      include('research.urls')
    ),
    path(
      'admin/',
      admin.site.urls
    ),
    path(
      'markdownx/',
      include('markdownx.urls')
    ),
] 

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns.append(path('__debug__/', include('debug_toolbar.urls')))
