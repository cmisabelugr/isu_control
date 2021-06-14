from django.shortcuts import render, get_object_or_404

from .models import *

# Create your views here.

def index(request):
    comensales = Comensal.objects.all()
    context = {
        'comensales' : comensales
    }
    return render(request, 'comensales/index.html', context)

def detail(request, comensal_id):
    comen = get_object_or_404(Comensal, pk=comensal_id)
    return render(request, 'comensales/detail.html', {'comensal' : comen})
