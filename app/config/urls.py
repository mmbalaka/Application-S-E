"""Configuration des URLs du projet."""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("i18n/", include("django.conf.urls.i18n")),  # bascule de langue (set_language)
    path("", include("suivi.urls")),
]

# Fichiers téléversés (sources de vérification) — servis par Django en développement
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
