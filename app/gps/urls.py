from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MovilViewSet

router = DefaultRouter()
router.register(r'moviles', MovilViewSet)

urlpatterns = [
    path('', include(router.urls)),
]