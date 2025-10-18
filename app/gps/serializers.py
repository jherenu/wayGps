from rest_framework import serializers
from .models import  Equipo


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