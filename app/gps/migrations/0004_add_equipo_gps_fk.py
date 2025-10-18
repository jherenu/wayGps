# Generated manually to document database changes

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('gps', '0003_fix_gps_id_null'),
    ]

    operations = [
        # Documentar que se agregó la columna equipo_gps_id manualmente
        migrations.AddField(
            model_name='movil',
            name='equipo_gps',
            field=models.ForeignKey(
                blank=True,
                db_column='equipo_gps_id',
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name='moviles',
                to='gps.equipo',
                verbose_name='Equipo GPS'
            ),
        ),
    ]