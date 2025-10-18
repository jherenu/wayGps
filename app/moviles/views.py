from rest_framework import viewsets
from django.shortcuts import render

from .models import Movil
from .serializers import MovilSerializer


class MovilViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gestión de móviles (vehículos de la flota)
    """
    queryset = Movil.objects.select_related('equipo_gps').all()
    serializer_class = MovilSerializer


def moviles_frontend(request):
    """Renderiza templates/moviles/index.html"""
    return render(request, 'moviles/index.html')