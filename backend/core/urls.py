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


# ─────────────────────────────────────────────────────────────
# HEALTH CHECK
# ─────────────────────────────────────────────────────────────
def health_check(request):
    try:
        connection.ensure_connection()
        db_ok = True
    except Exception:
        db_ok = False

    return JsonResponse(
        {
            'status': 'ok' if db_ok else 'degraded',
            'database': db_ok,
        },
        status=200 if db_ok else 503
    )


# ─────────────────────────────────────────────────────────────
# URL PATTERNS
# ─────────────────────────────────────────────────────────────
urlpatterns = [
    # Health endpoint
    path('health/', health_check, name='health_check'),

    # Django admin
    path('admin/', admin.site.urls),

    # API routes
    path('api/', include('api.urls')),

    # JWT authentication
    path(
        'api/token/',
        TokenObtainPairView.as_view(),
        name='token_obtain_pair'
    ),

    path(
        'api/token/refresh/',
        TokenRefreshView.as_view(),
        name='token_refresh'
    ),

    # Protected media serving
    path(
        'media/<path:path>',
        protected_media,
        name='protected_media'
    ),
]


# ─────────────────────────────────────────────────────────────
# STATIC FILES IN DEVELOPMENT
# ─────────────────────────────────────────────────────────────
if settings.DEBUG:
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns
    urlpatterns += staticfiles_urlpatterns()