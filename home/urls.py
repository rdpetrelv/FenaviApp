from django.urls import path
from . import views 

urlpatterns = [
    path('crearusuario/', views.crearusuario, name = 'crearusuario'),
    path('desconexion/', views.desconexion, name = 'desconexion'),
]