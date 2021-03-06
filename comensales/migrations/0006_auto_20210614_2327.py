# Generated by Django 3.2.4 on 2021-06-14 21:27

import comensales.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('comensales', '0005_alter_comida_fecha'),
    ]

    operations = [
        migrations.CreateModel(
            name='ComidaActual',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('com', models.CharField(choices=[('Desayuno', 'Desayuno'), ('Brunch', 'Brunch'), ('Almuerzo', 'Almuerzo'), ('Merienda', 'Merienda'), ('Cena', 'Cena')], default=comensales.models.enumComidas['DE'], max_length=8)),
            ],
        ),
        migrations.AlterField(
            model_name='comensal',
            name='nombre',
            field=models.CharField(blank=True, max_length=200),
        ),
    ]
