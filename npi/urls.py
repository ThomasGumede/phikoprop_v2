from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.shortcuts import render
from django.urls import path, include

def npi_home(request):
    return render(request, "home/home.html")


urlpatterns = [
    path("", include("npi_home.urls", namespace="npi_home")),
    path('admin/', admin.site.urls),
    path("", include("accounts.urls", namespace="accounts")),
    path("", include("properties.urls", namespace="properties")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
