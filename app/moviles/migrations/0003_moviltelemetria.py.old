import django.db.models.deletion
from django.db import migrations, models


def migrar_datos_telemetria(apps, schema_editor):
    """
    Migra los datos de telemetría desde la tabla moviles a moviles_telemetria
    """
    Movil = apps.get_model('moviles', 'Movil')
    MovilTelemetria = apps.get_model('moviles', 'MovilTelemetria')
    
    # Copiar datos de todos los móviles
    for movil in Movil.objects.all():
        MovilTelemetria.objects.create(
            movil=movil,
            ignicion=movil.ignicion,
            bateria_pct=movil.bateria_pct,
            odometro_km=movil.odometro_km,
            km_calculado=movil.km_calculado,
            km_ultimo_calculo_at=movil.km_ultimo_calculo_at
        )


def revertir_migracion(apps, schema_editor):
    """
    Revierte la migración eliminando todos los registros de telemetría
    """
    MovilTelemetria = apps.get_model('moviles', 'MovilTelemetria')
    MovilTelemetria.objects.all().delete()


class Migration(migrations.Migration):

    dependencies = [
        ('moviles', '0002_movilgeocode_remove_movil_dir_barrio_and_more'),
    ]

    operations = [
        # 1. Crear la tabla moviles_telemetria
        migrations.CreateModel(
            name='MovilTelemetria',
            fields=[
                ('movil', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='telemetria', serialize=False, to='moviles.movil')),
                ('ignicion', models.BooleanField(blank=True, help_text='Estado de la ignición del vehículo', null=True)),
                ('bateria_pct', models.DecimalField(blank=True, decimal_places=2, help_text='Porcentaje de batería del vehículo', max_digits=5, null=True)),
                ('odometro_km', models.DecimalField(blank=True, decimal_places=3, help_text='Odómetro reportado por el GPS', max_digits=12, null=True)),
                ('km_calculado', models.DecimalField(blank=True, decimal_places=3, help_text='Kilómetros calculados por el sistema', max_digits=12, null=True)),
                ('km_ultimo_calculo_at', models.DateTimeField(blank=True, help_text='Última vez que se calculó el kilometraje', null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Telemetría de Móvil',
                'verbose_name_plural': 'Telemetrías de Móviles',
                'db_table': 'moviles_telemetria',
            },
        ),
        
        # 2. Migrar los datos existentes
        migrations.RunPython(
            migrar_datos_telemetria,
            revertir_migracion
        ),
    ]