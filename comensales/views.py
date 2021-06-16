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

@login_required(login_url='/admin/')
def total(request):
    comidas = Comida.objects.all().order_by('fecha')
    fecha_ant = dateformat.format(timezone.localtime(Comida.objects.first().fecha), 'd/m/y')
    claves = {
        'Desayuno': 0,
        'Brunch': 1,
        'Almuerzo': 2,
        'Merienda': 3,
        'Cena': 4
    }
    dias = {}
    x = [0, 0, 0, 0, 0, 0]
    for comida in comidas:
        fecha_nueva = dateformat.format(timezone.localtime(comida.fecha), 'd/m/y')
        if fecha_ant != fecha_nueva:
            x = [0, 0, 0, 0, 0, 0]
            fecha_ant = fecha_nueva
        
        x[claves[comida.com]] += 1
        x[5] += 1
        dias[str(fecha_ant)] = x
        fecha_ant = fecha_nueva
        
    dias[str(fecha_ant)] = x
            
    return render(request, 'comensales/total.html', {'dias' : dias})
            

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
        
        if ComAct is None:
            ComAct = ComidaActual()

        ComAct.com = CodigosFran[qr].value
        ComAct.save()
        return HttpResponse("{} guardad@ con éxito".format(ComAct.com), status=200)
    else:
        try:
            comen = Comensal.objects.get(codigo=qr)
        except Comensal.DoesNotExist:
            comen = Comensal(codigo=qr)
            comen.save()
        
        nuevaCom = Comida(de_comensal=comen, com = ComidaActual.objects.first().com)
        nuevaCom.save()
        
    return HttpResponse("{} añadid@ con éxito al comensal {}".format(ComidaActual.objects.first().com, comen), status=200)
