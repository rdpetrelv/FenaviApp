# Generated by Django 4.0 on 2023-06-05 19:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('visuales', '0015_alter_alimento_ciclo_alter_cicloproduccion_ciclo_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='metasIP',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('meta_IP_excelente', models.IntegerField()),
                ('meta_IP_bueno', models.IntegerField()),
                ('meta_IP_regular', models.IntegerField()),
            ],
            options={
                'verbose_name_plural': 'Metas IP',
            },
        ),
    ]