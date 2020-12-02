from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import static, staticfiles_urlpatterns
from .views import home_view


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_view, name="home-view")
]

urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# urlpatterns +=  static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
# urlpatterns +=  static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

