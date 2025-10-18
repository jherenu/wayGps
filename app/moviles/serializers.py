from rest_framework import serializers
from .models import Movil
from gps.models import Equipo


class MovilSerializer(serializers.ModelSerializer):
    equipo_gps_info = serializers.SerializerMethodField(read_only=True)
    
    class Meta:
        model = Movil
        fields = '__all__'
        read_only_fields = (
            'id', 'created_at', 'updated_at', 'geom',
            'ultimo_lat', 'ultimo_lon', 'ultimo_rumbo', 'ultima_velocidad_kmh',
            'ultima_altitud_m', 'ult_satelites', 'ultimo_hdop',
            'fecha_gps', 'fecha_recepcion', 'raw_data', 'raw_json',
            'ignicion', 'bateria_pct', 'odometro_km', 'km_calculado',
            'km_ultimo_calculo_at',
            'dir_formateada', 'dir_calle', 'dir_numero', 'dir_piso', 'dir_depto',
            'dir_barrio', 'dir_localidad', 'dir_municipio', 'dir_provincia',
            'dir_cp', 'dir_pais', 'geo_fuente', 'geo_confianza',
            'geo_actualizado_at', 'geo_geohash',
            'icono_tipo', 'icono_color_hex', 'icono_url',
            'icono_rotacion_modo', 'icono_rotacion_grados', 'icono_escala'
        )
    
    def get_equipo_gps_info(self, obj):
        """Información del equipo GPS asignado"""
        if obj.equipo_gps:
            return {
                'id': obj.equipo_gps.id,
                'imei': obj.equipo_gps.imei,
                'marca': obj.equipo_gps.marca,
                'modelo': obj.equipo_gps.modelo,
                'estado': obj.equipo_gps.estado
            }
        return None
    
    def validate_patente(self, value):
        """Valida que la patente sea única"""
        if value:
            qs = Movil.objects.filter(patente=value)
            if self.instance:
                qs = qs.exclude(pk=self.instance.pk)
            if qs.exists():
                raise serializers.ValidationError("Ya existe un móvil con esta patente")
        return value
    
    def validate_gps_id(self, value):
        """Valida que el GPS ID sea único"""
        if value:
            qs = Movil.objects.filter(gps_id=value)
            if self.instance:
                qs = qs.exclude(pk=self.instance.pk)
            if qs.exists():
                raise serializers.ValidationError("Ya existe un móvil con este GPS ID")
        return value
    
    def validate_codigo(self, value):
        """Valida que el código sea único"""
        if value:
            qs = Movil.objects.filter(codigo=value)
            if self.instance:
                qs = qs.exclude(pk=self.instance.pk)
            if qs.exists():
                raise serializers.ValidationError("Ya existe un móvil con este código")
        return value