from django.contrib import admin
from .models import Movil, Equipo


@admin.register(Movil)
class MovilAdmin(admin.ModelAdmin):
    list_display = ['patente', 'alias', 'gps_id', 'marca', 'modelo', 'activo', 'created_at']
    list_filter = ['activo', 'tipo_vehiculo', 'created_at']
    search_fields = ['patente', 'alias', 'gps_id', 'codigo', 'vin']
    ordering = ['-created_at']


@admin.register(Equipo)
class EquipoAdmin(admin.ModelAdmin):
    list_display = ['imei', 'marca', 'modelo', 'estado', 'fecha_instalacion', 'created_at']
    list_filter = ['estado', 'marca', 'created_at']
    search_fields = ['imei', 'numero_serie', 'marca', 'modelo']
    ordering = ['-created_at']


# Register your models here.
