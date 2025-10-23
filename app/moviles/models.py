from django.contrib.gis.db import models

# Create your models here.
class Movil(models.Model):
    # Identificación
    id = models.BigAutoField(primary_key=True)
    codigo = models.CharField(max_length=32, unique=True, null=True, blank=True)
    alias = models.CharField(max_length=100, null=True, blank=True)
    patente = models.CharField(max_length=20, unique=True, null=True, blank=True)
    vin = models.CharField(max_length=17, null=True, blank=True)

    # Datos del vehículo
    marca = models.TextField(null=True, blank=True)
    modelo = models.TextField(null=True, blank=True)
    anio = models.SmallIntegerField(null=True, blank=True)
    color = models.TextField(null=True, blank=True)
    tipo_vehiculo = models.CharField(max_length=20, null=True, blank=True)

    # Equipo GPS
    gps_id = models.CharField(max_length=50, unique=True, null=True, blank=True, db_column='gps_id',
                              help_text='DEPRECATED - Usar equipo_gps')
        # Columna NUEVA (ForeignKey)
    equipo_gps = models.ForeignKey(
        'gps.Equipo',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='moviles',
        db_column='equipo_gps_id',
        verbose_name='Equipo GPS'
    )                              

    # Última posición
    ultimo_lat = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    ultimo_lon = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    ultimo_rumbo = models.SmallIntegerField(null=True, blank=True)
    ultima_velocidad_kmh = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    ultima_altitud_m = models.DecimalField(max_digits=7, decimal_places=2, null=True, blank=True)
    ult_satelites = models.SmallIntegerField(null=True, blank=True)
    ultimo_hdop = models.DecimalField(max_digits=4, decimal_places=1, null=True, blank=True)
    fecha_gps = models.DateTimeField(null=True, blank=True)
    fecha_recepcion = models.DateTimeField(null=True, blank=True)

    # Payload crudo
    raw_data = models.TextField(null=True, blank=True)
    raw_json = models.JSONField(null=True, blank=True)

    # Geometría
    geom = models.PointField(srid=4326, null=True, blank=True)

    # Personalización de ícono
    icono_tipo = models.CharField(max_length=20, null=True, blank=True)
    icono_color_hex = models.CharField(max_length=7, null=True, blank=True)
    icono_url = models.TextField(null=True, blank=True)
    icono_rotacion_modo = models.CharField(max_length=10, null=True, blank=True)
    icono_rotacion_grados = models.SmallIntegerField(null=True, blank=True)
    icono_escala = models.DecimalField(max_digits=3, decimal_places=2, null=True, blank=True)

    # Estado
    activo = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'moviles'
        verbose_name = 'Móvil'
        verbose_name_plural = 'Móviles'

    def __str__(self):
        return f"{self.alias or self.patente or self.gps_id}"

class MovilGeocode(models.Model):
    """
    Datos de geocodificación del móvil.
    Relación 1:1 con Movil.
    """
    
    # Relación con Movil
    movil = models.OneToOneField(
        Movil,
        on_delete=models.CASCADE,
        primary_key=True,
        related_name='geocode',
        verbose_name='Móvil'
    )
    
    # Dirección formateada completa
    dir_formateada = models.TextField(null=True, blank=True, verbose_name='Dirección Formateada')
    # Componentes de dirección
    dir_calle = models.TextField(null=True, blank=True, verbose_name='Calle')
    dir_numero = models.TextField(null=True, blank=True, verbose_name='Número')
    dir_piso = models.TextField(null=True, blank=True, verbose_name='Piso')
    dir_depto = models.TextField(null=True, blank=True, verbose_name='Departamento')
    dir_barrio = models.TextField(null=True, blank=True, verbose_name='Barrio')
    dir_localidad = models.TextField(null=True, blank=True, verbose_name='Localidad')
    dir_municipio = models.TextField(null=True, blank=True, verbose_name='Municipio')
    dir_provincia = models.TextField(null=True, blank=True, verbose_name='Provincia')
    dir_cp = models.TextField(null=True, blank=True, verbose_name='Código Postal')
    dir_pais = models.TextField(default='Argentina', null=True, blank=True, verbose_name='País')
    
    # Metadatos de geocodificación
    geo_fuente = models.CharField(max_length=30, null=True, blank=True, verbose_name='Fuente Geocodificación')
    geo_confianza = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, verbose_name='Confianza (%)')
    geo_actualizado_at = models.DateTimeField(null=True, blank=True, verbose_name='Última Actualización')
    geo_geohash = models.CharField(max_length=15, null=True, blank=True, verbose_name='Geohash')
    
    # Auditoría
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Fecha Creación')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Fecha Actualización')
    
    class Meta:
        db_table = 'moviles_geocode'
        verbose_name = 'Geocodificación de Móvil'
        verbose_name_plural = 'Geocodificaciones de Móviles'
    
    def __str__(self):
        if self.dir_formateada:
            return f"Geocode: {self.dir_formateada[:50]}"
        return f"Geocode: Móvil #{self.movil_id}"

class MovilTelemetria(models.Model):
    """
    Datos de telemetría y sensores del vehículo.
    Relación OneToOne con Movil.
    """
    movil = models.OneToOneField(
        'Movil',
        on_delete=models.CASCADE,
        primary_key=True,
        related_name='telemetria'
    )
    
    # Sensores
    ignicion = models.BooleanField(
        null=True, 
        blank=True,
        help_text='Estado de la ignición del vehículo'
    )
    bateria_pct = models.DecimalField(
        max_digits=5, 
        decimal_places=2, 
        null=True, 
        blank=True,
        help_text='Porcentaje de batería del vehículo'
    )
    
    # Odómetro
    odometro_km = models.DecimalField(
        max_digits=12, 
        decimal_places=3, 
        null=True, 
        blank=True,
        help_text='Odómetro reportado por el GPS'
    )
    km_calculado = models.DecimalField(
        max_digits=12, 
        decimal_places=3, 
        null=True, 
        blank=True,
        help_text='Kilómetros calculados por el sistema'
    )
    km_ultimo_calculo_at = models.DateTimeField(
        null=True, 
        blank=True,
        help_text='Última vez que se calculó el kilometraje'
    )
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'moviles_telemetria'
        verbose_name = 'Telemetría de Móvil'
        verbose_name_plural = 'Telemetrías de Móviles'
    
    def __str__(self):
        return f"Telemetría {self.movil.patente}"