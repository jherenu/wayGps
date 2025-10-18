from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Equipo
from .serializers import EquipoSerializer


class EquipoViewSet(viewsets.ModelViewSet):
    queryset = Equipo.objects.all()
    serializer_class = EquipoSerializer
    
    @action(detail=False, methods=['get'])
    def sin_asignar(self, request):
        """Obtener equipos inactivos (sin asignar a ningún móvil)"""
        # Buscar equipos con estado 'inactivo' y que no estén referenciados en moviles.gps_id
        equipos_inactivos = Equipo.objects.filter(estado='inactivo')
        
     
        serializer = self.get_serializer(equipos_sin_asignar, many=True)
        return Response(serializer.data)

# Vista para servir el frontend de equipos
def equipos_frontend(request):
    return render(request, 'equipos/index.html')