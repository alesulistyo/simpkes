from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.staticfiles.storage import staticfiles_storage
from django.urls import include, path
from django.views.generic.base import RedirectView

from . import views

urlpatterns = [
    path('', views.index),
    path('admin/', admin.site.urls),
    path('monitor/', include('monitoring.urls')),
    path('riwayat/', include('history.urls')),
    path('favicon.ico', RedirectView.as_view(url=staticfiles_storage.url('img/favicon.ico'))),
] + static(
    settings.STATIC_URL, document_root=settings.STATIC_ROOT)
