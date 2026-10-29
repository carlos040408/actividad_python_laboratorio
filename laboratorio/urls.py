from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista_equipos, name='lista_equipos'),
    path('registrar/', views.registrar_equipo, name='registrar_equipo'),
]