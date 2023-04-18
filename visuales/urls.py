from django.urls import path
from . import views

urlpatterns = [
    path("chart/ip_evolucion_ultimos_ciclos/", views.ip_evolucion_ultimos_ciclos, name="ip_evolucion_ultimos_ciclos"),
    path("chart/ip_comparativa_integrantes/", views.ip_comparativa_integrantes, name="ip_comparativa_integrantes"),
    #path("grafico2", views.graficoprueba2, name = 'grafico prueba')
]