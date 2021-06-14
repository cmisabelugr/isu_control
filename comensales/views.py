from django.shortcuts import render, get_object_or_404

from django.http import HttpResponse

from django.contrib.auth.decorators import login_required

from .models import *

# Create your views here.

@login_required(login_url='/admin/')
def index(request):
    comensales = Comensal.objects.all()
    context = {
        'comensales' : comensales
    }
    return render(request, 'comensales/index.html', context)


@login_required(login_url='/admin/')
def detail(request, comensal_id):
    comen = get_object_or_404(Comensal, pk=comensal_id)
    return render(request, 'comensales/detail.html', {'comensal' : comen})



def addComida(request, qr):
    CodigosFran = {
        'FranDes': enumComidas.DE,
        'FranBru': enumComidas.BR,
        'FranAlm': enumComidas.AL,
        'FranMer': enumComidas.ME,
        'FranCen': enumComidas.CE
        }
    
    if qr in CodigosFran.keys():
        ComAct = ComidaActual.objects.first()
        ComAct.com = CodigosFran[qr].value
        ComAct.save()
    else:
        try:
            comen = Comensal.objects.get(codigo=qr)
        except Comensal.DoesNotExist:
            comen = Comensal(codigo=qr)
            comen.save()
        
        nuevaCom = Comida(de_comensal=comen, com = ComidaActual.objects.first().com)
        nuevaCom.save()
        
    return HttpResponse("Comida añadida con éxito", status=200)
