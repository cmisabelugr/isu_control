# Generated by Django 3.2.4 on 2021-06-14 13:38

import comensales.models
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Comensal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=200)),
                ('comida', models.CharField(choices=[(comensales.models.enumComidas['DE'], 'Desayuno'), (comensales.models.enumComidas['BR'], 'Brunch'), (comensales.models.enumComidas['AL'], 'Almuerzo'), (comensales.models.enumComidas['ME'], 'Merienda'), (comensales.models.enumComidas['CE'], 'Cena')], max_length=8)),
            ],
        ),
    ]