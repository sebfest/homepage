from django.contrib import admin
from django.contrib.flatpages import views as flat_views
from django.urls import path, include
from django.conf.urls.static import static


from homepage import settings

urlpatterns = [
    path('', include('blog.urls')),
    path('', include('research.urls')),
    path('', include('teaching.urls')),
    path('', include('contact.urls')),
    path('pages/', include('django.contrib.flatpages.urls')),
    path('markdownx/', include('markdownx.urls')),
    path('admin/', admin.site.urls),
    path('about/', flat_views.flatpage, {'url': '/about/'}, name='about'),
    path('disclaimer/', flat_views.flatpage, {'url': '/disclaimer/'}, name='disclaimer'),
    ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns




