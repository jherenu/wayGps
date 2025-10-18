from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Movil, Equipo
from .serializers import MovilSerializer, EquipoSerializer


class MovilViewSet(viewsets.ModelViewSet):
    queryset = Movil.objects.select_related('equipo_gps').all()  # ← OPTIMIZACIÓN
    serializer_class = MovilSerializer


class EquipoViewSet(viewsets.ModelViewSet):
    queryset = Equipo.objects.all()
    serializer_class = EquipoSerializer
    
    @action(detail=False, methods=['get'])
    def sin_asignar(self, request):
        """Obtener equipos inactivos (sin asignar a ningún móvil)"""
        # Buscar equipos con estado 'inactivo' y que no estén referenciados en moviles.gps_id
        equipos_inactivos = Equipo.objects.filter(estado='inactivo')
        
        # Filtrar los que NO están asignados (no aparecen en moviles.gps_id)
        equipos_sin_asignar = []
        for equipo in equipos_inactivos:
            # Verificar si este IMEI está en uso en algún móvil
            if not Movil.objects.filter(gps_id=equipo.imei).exists():
                equipos_sin_asignar.append(equipo)
        
        serializer = self.get_serializer(equipos_sin_asignar, many=True)
        return Response(serializer.data)


# Vista para servir el frontend de móviles
def moviles_frontend(request):
    return render(request, 'moviles/index.html')


# Vista para servir el frontend de equipos
def equipos_frontend(request):
    return render(request, 'equipos/index.html')