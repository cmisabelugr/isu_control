from django.urls import path

from . import views


app_name= 'comensales'

urlpatterns = [
    path('', views.index, name='index'),
    path('total/', views.total, name='total'),
    path('<int:comensal_id>/', views.detail, name='detail'),
    path('<str:qr>/', views.addComida, name='nuevaComida'),
]
