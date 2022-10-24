from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

import config.settings.base as settings
import os

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
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if os.environ['DEBUG'] == '1':
    urlpatterns.append(path('__debug__/', include('debug_toolbar.urls')))
