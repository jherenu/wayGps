from django.contrib.gis.db import models
from django.contrib.postgres.fields import CITextField


class Movil(models.Model):
    # Identificación
    id = models.BigAutoField(primary_key=True)
    codigo = models.CharField(max_length=32, unique=True, null=True, blank=True)
    alias = CITextField(null=True, blank=True)
    patente = CITextField(unique=True, null=True, blank=True)
    vin = models.CharField(max_length=17, null=True, blank=True)

    # Datos del vehículo
    marca = models.TextField(null=True, blank=True)
    modelo = models.TextField(null=True, blank=True)
    anio = models.SmallIntegerField(null=True, blank=True)
    color = models.TextField(null=True, blank=True)
    tipo_vehiculo = models.CharField(max_length=20, null=True, blank=True)

    # Equipo GPS
    gps_id = CITextField(unique=True)

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

    # Telemetría
    ignicion = models.BooleanField(null=True, blank=True)
    bateria_pct = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    odometro_km = models.DecimalField(max_digits=12, decimal_places=3, null=True, blank=True)
    km_calculado = models.DecimalField(max_digits=12, decimal_places=3, null=True, blank=True)
    km_ultimo_calculo_at = models.DateTimeField(null=True, blank=True)

    # Geocodificación
    dir_formateada = models.TextField(null=True, blank=True)
    dir_calle = models.TextField(null=True, blank=True)
    dir_numero = models.TextField(null=True, blank=True)
    dir_piso = models.TextField(null=True, blank=True)
    dir_depto = models.TextField(null=True, blank=True)
    dir_barrio = models.TextField(null=True, blank=True)
    dir_localidad = models.TextField(null=True, blank=True)
    dir_municipio = models.TextField(null=True, blank=True)
    dir_provincia = models.TextField(null=True, blank=True)
    dir_cp = models.TextField(null=True, blank=True)
    dir_pais = models.TextField(default='Argentina', null=True, blank=True)
    geo_fuente = models.CharField(max_length=30, null=True, blank=True)
    geo_confianza = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    geo_actualizado_at = models.DateTimeField(null=True, blank=True)
    geo_geohash = models.CharField(max_length=15, null=True, blank=True)

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

    def _str_(self):
        return f"{self.alias or self.patente or self.gps_id}"

# Create your models here.
