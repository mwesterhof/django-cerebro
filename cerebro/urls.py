from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from django.conf.urls.static import static

from brain import urls as brain_urls


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(brain_urls)),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
