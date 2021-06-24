from django.shortcuts import render, get_object_or_404

from django.http import HttpResponse, JsonResponse, response

from django.contrib.auth.decorators import login_required

from django.utils import timezone


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
        'Cena': 4,
        'Pack': 5
    }
    dias = {}
    x = [0]*(len(claves.keys())+1)
    for comida in comidas:
        fecha_nueva = dateformat.format(timezone.localtime(comida.fecha), 'd/m/y')
        if fecha_ant != fecha_nueva:
            x = [0]*(len(claves.keys())+1)
            fecha_ant = fecha_nueva
        
        x[claves[comida.com]] += 1
        x[len(claves.keys())] += 1
        dias[str(fecha_ant)] = x
        fecha_ant = fecha_nueva
        
    dias[str(fecha_ant)] = x
            
    return render(request, 'comensales/total.html', {'dias' : dias})
            

def addComida(request):
    if 'pass' not in request.GET or request.GET['pass']!="hola":
        respuesta = {
            'status':403,
            'message': "FORBIDDEN"
            }
        return JsonResponse(respuesta)

    if 'qr' not in request.GET:
        respuesta = {
            'status':403,
            'message': "FORBIDDEN"
            }
        return JsonResponse(respuesta)

    qr = request.GET['qr']

    CodigosFran = {
        'FranDes': enumComidas.DE,
        'FranBru': enumComidas.BR,
        'FranAlm': enumComidas.AL,
        'FranMer': enumComidas.ME,
        'FranCen': enumComidas.CE,
        'FranPac': enumComidas.PA,
        }
    
    if qr in CodigosFran.keys():
        ComAct = ComidaActual.objects.first()
        
        if ComAct is None:
            ComAct = ComidaActual()

        ComAct.com = CodigosFran[qr].value
        ComAct.save()
        respuesta = {
            'status':200,
            'message': "{} guardada con exito".format(ComAct.com)
            }
        return JsonResponse(respuesta)
    else:
        try:
            comen = Comensal.objects.get(codigo=qr)
        except Comensal.DoesNotExist:
            comen = Comensal(codigo=qr)
            comen.save()
        
        comida_activa = ComidaActual.objects.first().com
        #Add comprobación de que no ha comido ya
        comidas_servidas_hoy = Comida.objects.filter(de_comensal=comen, com=comida_activa, fecha__gte=timezone.now().replace(hour=0, minute=0, second=0), fecha__lte=timezone.now().replace(hour=23, minute=59, second=59))
        if (comidas_servidas_hoy.count() !=0):
            respuesta = {
            'status':409,
            'message': "{} ya ha comido hoy.".format(comen),
            'display_name' : "{}".format(comen),
            }
            return JsonResponse(respuesta)



        nuevaCom = Comida(de_comensal=comen, com = comida_activa)
        nuevaCom.save()
        respuesta = {
            'status':200,
            'message': "{} añadid@ con éxito al comensal {}".format(comida_activa, comen),
            'display_name' : "{}".format(comen),
            'comidas_turno' : Comida.objects.filter(com=comida_activa, fecha__gte=timezone.now().replace(hour=0, minute=0, second=0), fecha__lte=timezone.now().replace(hour=23, minute=59, second=59)).count()
            }
    return JsonResponse(respuesta)

def status(request):
    comida_activa = ComidaActual.objects.first().com
    respuesta = {
        'status': 200,
        'message': "Funcionando correctamente",
        'comidas_turno' : Comida.objects.filter(com=comida_activa, fecha__gte=timezone.now().replace(hour=0, minute=0, second=0), fecha__lte=timezone.now().replace(hour=23, minute=59, second=59)).count(),
        'comida_activa' : comida_activa
    }
    return JsonResponse(respuesta)