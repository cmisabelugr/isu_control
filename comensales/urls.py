from django.urls import path

from . import views


app_name= 'comensales'

urlpatterns = [
    path('', views.index, name='index'),
    path('total/', views.total, name='total'),
    path('<int:comensal_id>/', views.detail, name='detail'),
    path('newcode/', views.addComida, name='nuevaComida'),
    path('status/', views.status, name='status'),
    path('solofranpuedeentraraqui/', views.resumen_fran, name='resumen_fran'),
    path('json_dump/', views.json_escaneos, name='json_dump'),
]
