from django.contrib.gis.db import models
#from django.contrib.postgres.fields import CITextField

class Equipo(models.Model):
    """
    Modelo de Equipos GPS
    Representa los dispositivos GPS que se instalan en los vehículos
    """
    # Identificación
    id = models.BigAutoField(primary_key=True)
    imei = models.CharField(max_length=15, unique=True, verbose_name='IMEI')
    numero_serie = models.CharField(max_length=50, null=True, blank=True, verbose_name='Número de Serie')
    
    # Información del equipo
    marca = models.CharField(max_length=50, null=True, blank=True)
    modelo = models.CharField(max_length=50, null=True, blank=True)
    
    # Estado
    estado = models.CharField(max_length=20, null=True, blank=True)
    
    # Relación con empresa (para futuro)
    empresa = models.ForeignKey(
        'Empresa',
        on_delete=models.DO_NOTHING,
        null=True,
        blank=True
        # La columna en la BD se llama 'empresa_id' (convención de Django)
    )
    
    # Fechas
    fecha_instalacion = models.DateTimeField(null=True, blank=True)
    
    # Auditoría (no usar auto_now porque managed=False)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    
    class Meta:
        managed = False  # No permitir que Django modifique la tabla
        db_table = 'equipos_gps'
        verbose_name = 'Equipo GPS'
        verbose_name_plural = 'Equipos GPS'
    
    def __str__(self):
        return f"{self.imei} - {self.marca or 'Sin marca'} {self.modelo or ''}"


class Empresa(models.Model):
    """Modelo temporal para la relación (se creará completo en el futuro)"""
    id = models.BigAutoField(primary_key=True)
    nombre = models.CharField(max_length=200)
    
    class Meta:
        managed = False
        db_table = 'empresas'


# Create your models here.
