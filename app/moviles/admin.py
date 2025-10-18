from django.contrib import admin
from django.contrib.gis.admin import GISModelAdmin
from .models import Movil


@admin.register(Movil)
class MovilAdmin(GISModelAdmin):
    list_display = [
        'patente', 'alias', 'equipo_gps', 
        'marca', 'modelo', 'activo', 'created_at'
    ]
    list_filter = ['activo', 'tipo_vehiculo', 'created_at']
    search_fields = ['patente', 'alias', 'gps_id', 'codigo', 'vin']
    ordering = ['-created_at']
    
    fieldsets = (
        ('Identificación', {
            'fields': ('codigo', 'alias', 'patente', 'vin')
        }),
        ('Vehículo', {
            'fields': ('marca', 'modelo', 'anio', 'color', 'tipo_vehiculo')
        }),
        ('Equipo GPS', {
            'fields': ('equipo_gps', 'gps_id')
        }),
        ('Estado', {
            'fields': ('activo',)
        }),
    )
    
    readonly_fields = ['gps_id']