from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from gps.views import moviles_frontend, equipos_frontend
from authentication.views import login_frontend

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include('authentication.urls')),  # API de autenticación
    path('api/', include('gps.urls')),  # API de GPS
    path('login/', login_frontend, name='login'),  # Página de login
    path('moviles/', moviles_frontend, name='moviles_frontend'),
    path('equipos/', equipos_frontend, name='equipos_frontend'),
    path('', login_frontend, name='home'),  # Redirige raíz a login
]

# Servir archivos estáticos y media en desarrollo
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)