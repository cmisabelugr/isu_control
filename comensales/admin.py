from django.contrib import admin
from .models import Comensal, Comida, ComidaActual

# Register your models here.

admin.site.register(Comensal)
admin.site.register(Comida)
admin.site.register(ComidaActual)
