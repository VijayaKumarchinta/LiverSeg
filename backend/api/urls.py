from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.http import JsonResponse
from django.db import connection
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from api.views import protected_media


# ── Health check ──────────────────────────────────────────────────────────────
def health_check(request):
    try:
        connection.ensure_connection()
        db_ok = True
    except Exception:
        db_ok = False
    http_status = 200 if db_ok else 503
    return JsonResponse(
        {'status': 'ok' if db_ok else 'degraded', 'db': db_ok},
        status=http_status
    )


urlpatterns = [
    path('health/', health_check, name='health_check'),
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # Media files are served through authenticated view — no static() fallback
    path('media/<path:path>', protected_media, name='protected_media'),
]

# Serve static assets in development only
if settings.DEBUG:
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns
    urlpatterns += staticfiles_urlpatterns()