from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, PatientViewSet, ActivityLogViewSet, PacsConfigViewSet, AuditLogViewSet

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'patients', PatientViewSet)
router.register(r'activities', ActivityLogViewSet)
router.register(r'pacs', PacsConfigViewSet)
router.register(r'audit', AuditLogViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
