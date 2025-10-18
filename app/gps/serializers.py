from rest_framework import serializers
from .models import Movil, Equipo


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
            'dir_formateada', 'dir_calle', 'dir_numero', 'dir_piso', 'dir_depto',
            'dir_barrio', 'dir_localidad', 'dir_municipio', 'dir_provincia',
            'dir_cp', 'dir_pais', 'geo_fuente', 'geo_confianza',
            'geo_actualizado_at', 'geo_geohash',
            'gps_id',  # DEPRECATED - mantener read_only por compatibilidad
        )
    
    def get_equipo_gps_info(self, obj):
        """Retorna información del equipo GPS asignado usando la FK"""
        if obj.equipo_gps:  # ← CAMBIO: Usa la FK en lugar de gps_id
            return {
                'id': obj.equipo_gps.id,
                'imei': obj.equipo_gps.imei,
                'marca': obj.equipo_gps.marca,
                'modelo': obj.equipo_gps.modelo,
                'estado': obj.equipo_gps.estado
            }
        return None
    
    def validate_patente(self, value):
        """Validar que la patente no esté duplicada (excepto al editar)"""
        if value:
            # Obtener el ID del móvil que se está editando (si existe)
            movil_id = self.instance.id if self.instance else None
            
            # Verificar si ya existe otra patente igual
            qs = Movil.objects.filter(patente=value)
            if movil_id:
                qs = qs.exclude(id=movil_id)
            
            if qs.exists():
                raise serializers.ValidationError('Ya existe un móvil con esta patente')
        
        return value
    
    def validate_gps_id(self, value):
        """Validar que el GPS ID no esté duplicado (excepto al editar)"""
        if value:
            movil_id = self.instance.id if self.instance else None
            qs = Movil.objects.filter(gps_id=value)
            if movil_id:
                qs = qs.exclude(id=movil_id)
            
            if qs.exists():
                raise serializers.ValidationError('Ya existe un móvil con este GPS ID')
        
        return value
    
    def validate_codigo(self, value):
        """Validar que el código no esté duplicado (excepto al editar)"""
        if value:
            movil_id = self.instance.id if self.instance else None
            qs = Movil.objects.filter(codigo=value)
            if movil_id:
                qs = qs.exclude(id=movil_id)
            
            if qs.exists():
                raise serializers.ValidationError('Ya existe un móvil con este código')
        
        return value


class EquipoSerializer(serializers.ModelSerializer):
    movil_info = serializers.SerializerMethodField(read_only=True)
    
    class Meta:
        model = Equipo
        fields = [
            'id', 'imei', 'numero_serie', 'marca', 'modelo', 
            'estado', 'empresa', 'fecha_instalacion',
            'created_at', 'updated_at', 'movil_info'
        ]
        read_only_fields = ('id', 'created_at', 'updated_at', 'empresa', 'movil_info')
    
    def get_movil_info(self, obj):
        """Retorna información del móvil asignado (si existe)"""
        try:
            # Buscar móvil que tenga este IMEI en gps_id
            movil = Movil.objects.filter(gps_id=obj.imei).first()
            if movil:
                return {
                    'id': movil.id,
                    'patente': movil.patente,
                    'alias': movil.alias,
                }
            return None
        except Exception:
            return None
    
    def create(self, validated_data):
        """Crear equipo estableciendo created_at y updated_at manualmente"""
        from django.utils import timezone
        validated_data['created_at'] = timezone.now()
        validated_data['updated_at'] = timezone.now()
        return super().create(validated_data)
    
    def update(self, instance, validated_data):
        """Actualizar equipo estableciendo updated_at manualmente"""
        from django.utils import timezone
        validated_data['updated_at'] = timezone.now()
        return super().update(instance, validated_data)
    
    def validate_imei(self, value):
        """Validar que el IMEI no esté duplicado"""
        if value:
            equipo_id = self.instance.id if self.instance else None
            qs = Equipo.objects.filter(imei=value)
            if equipo_id:
                qs = qs.exclude(id=equipo_id)
            
            if qs.exists():
                raise serializers.ValidationError('Ya existe un equipo con este IMEI')
        
        return value
    
    def validate_numero_serie(self, value):
        """Validar que el número de serie no esté duplicado si se proporciona"""
        if value:
            equipo_id = self.instance.id if self.instance else None
            qs = Equipo.objects.filter(numero_serie=value)
            if equipo_id:
                qs = qs.exclude(id=equipo_id)
            
            if qs.exists():
                raise serializers.ValidationError('Ya existe un equipo con este número de serie')
        
        return value