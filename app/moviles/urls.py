from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MovilViewSet, moviles_frontend

# Router para API
router = DefaultRouter()
router.register(r'moviles', MovilViewSet, basename='movil')

urlpatterns = [
    # API endpoints
    path('api/', include(router.urls)),
    
    # Frontend
    path('moviles/', moviles_frontend, name='moviles_frontend'),
]