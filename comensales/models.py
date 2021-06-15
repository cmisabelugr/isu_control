from django.db import models

from enum import Enum

from django.utils import timezone, dateformat

# Create your models here.

class enumComidas(Enum):
    DE = "Desayuno"
    BR = "Brunch"
    AL = "Almuerzo"
    ME = "Merienda"
    CE = "Cena"

class Comensal(models.Model):
    codigo = models.CharField(max_length=200, default="0")
    nombre = models.CharField(max_length=200, blank=True)
    def __str__(self):
        if self.nombre:
            return self.nombre
        else:
            return self.codigo


class Comida(models.Model):
    de_comensal = models.ForeignKey(Comensal, on_delete=models.CASCADE)
    com = models.CharField(
        max_length=8,
        choices=[(tag.value, tag.value) for tag in enumComidas],
        default = enumComidas.DE
    )
    fecha = models.DateTimeField(default=timezone.now)
    def __str__(self):
        return "{} comió {} a las {}".format(self.de_comensal, self.com, dateformat.format(timezone.localtime(self.fecha), 'H:i, D d/m/y'))


class ComidaActual(models.Model):
    com = models.CharField(
        max_length=8,
        choices=[(tag.value, tag.value) for tag in enumComidas],
        default = enumComidas.DE
    )
    def __str__(self):
        return "Comida actual: {}".format(com)
