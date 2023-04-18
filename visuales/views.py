from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.shortcuts import redirect
from django.db import IntegrityError
from django.contrib.auth.forms import AuthenticationForm
from django.views.generic import TemplateView
from .models import Cicloproduccion, Ciclo_produccion_Form, Mortalidad, Alimento
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.http import JsonResponse


# Create your views here.
#def conversion(request):   
#    return render(request, 'conversion.html')

#def mortalidad(request):
#    return render(request, 'mortalidad.html')

#def indiceproductividad(request):
#    ciclos = Cicloproduccion.objects.all()
#    return render(request, 'indiceproductividad.html', {'ciclos': ciclos})

#Grafica indice de productividad

class Graficos(TemplateView):
    template_name = 'indiceproductividad.html'

    #@login_required
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["qs"] = Cicloproduccion.objects.filter(ciclo = 6, sexo = 'Macho')
        return context

#grafica mortalidad machos

class Graficos2(TemplateView):
    template_name = 'mortalidad.html'

    #@login_required
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["qs"] = Mortalidad.objects.filter( productor = 'Albeiro Hernández', semana = 7, sexo = 'Macho')
        return context

#Pendiente de realizar grafica

class Graficos3(TemplateView):
    template_name = 'conversion.html'
    
    #@login_required
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["qs"] = Alimento.objects.all()
        return context
    


# Tutorial de uso de chart.js en : https://testdriven.io/blog/django-charts/#prepare-and-serve-the-data

@login_required
def ip_evolucion_ultimos_ciclos(request):
    filter_by_user = Cicloproduccion.objects.filter(user = request.user, sexo = 'Macho')
    ciclo = []
    ip_ciclo = []
    for data in filter_by_user:
        ciclo.append(data.ciclo)
        ip_ciclo.append(round(data.indice_productividad,2))
    
    return JsonResponse({
        'title' : 'IP ultimos 6 ciclos',
        'data': {
            'labels' : ciclo,
            'dataset': [{
                'label':'Ips ciclos',
                'data': ip_ciclo
            }]
        }
    })

@login_required
def ip_comparativa_integrantes(request):
    ciclo_actual = int(Cicloproduccion.objects.order_by('-ciclo').first().ciclo)
    filter_by_ultimo_ciclo = Cicloproduccion.objects.filter(sexo = 'Macho', ciclo = ciclo_actual)
    productor = []
    ip_productor = []
    for data in filter_by_ultimo_ciclo:
        productor.append(data.productor)
        ip_productor.append(round(data.indice_productividad,2))

    return JsonResponse({
        'title' : 'IP comparativo ultimo ciclo',
        'data': {
            'labels' : productor,
            'dataset': [{
                'label':'Ips productores',
                'data': ip_productor
            }]
        }
    })

@login_required
def graficoprueba(request):
    return render(request, "grafico1.html", {})


#visual para grafica de conversion alimenticia
@login_required
def visual_Indice_productividad(request):
    filter_by_user = Cicloproduccion.objects.filter(user = request.user, sexo = 'Macho')
    ciclo = []
    ips_ciclo = []
    for data in filter_by_user:
        ciclo.append(data.ciclo)
        ips_ciclo.append(round(data.indice_productividad,2))

    ciclo_actual = int(Cicloproduccion.objects.order_by('-ciclo').first().ciclo)
    filter_by_ultimo_ciclo = Cicloproduccion.objects.filter(sexo = 'Macho', ciclo = ciclo_actual).order_by('-indice_productividad')
    productores = []
    ips_productor = []
    for data in filter_by_ultimo_ciclo:
        productores.append(data.productor)
        ips_productor.append(round(data.indice_productividad,2))

    return render(request, "indiceproductividad.html", {'ciclo1': ciclo, 'ips_ciclo': ips_ciclo, 'productores': productores, 'ips_productor': ips_productor})


#visual para grafica de conversion alimenticia
@login_required
def visual_Conversion_Alimentica(request):
    ciclo_actual = int(Cicloproduccion.objects.order_by('-ciclo').first().ciclo)
    machos_consumo_filtered = Alimento.objects.filter(user = request.user, 
                                                      ciclo = ciclo_actual,
                                                      sexo = 'Macho')
    hembras_consumo_filtered = Alimento.objects.filter(user = request.user, 
                                                      ciclo = ciclo_actual,
                                                      sexo = 'Hembra')
    machos_conversion_actual = round(machos_consumo_filtered.order_by('-semana').first().c_a_acum,2)
    hembras_conversion_actual = round(hembras_consumo_filtered.order_by('-semana').first().c_a_acum,2)
    machos_mortalidad_filtered = Mortalidad.objects.filter(user = request.user, 
                                                            ciclo = ciclo_actual,
                                                            sexo = 'Macho')
    hembras_mortalidad_filtered = Mortalidad.objects.filter(user = request.user,
                                                            ciclo = ciclo_actual, 
                                                            sexo = 'Hembra')
    semanas = []
    a = 0
    b = 0
    mixto_pesos_semanas = []
    mixto_conversion_semanas = []
    objetivos_mixto = 1.69
    objetivos_macho = 1.65
    objetivos_hembra = 1.72

    for row in machos_consumo_filtered:
        semanas.append(row.semana)
        #objetivos_macho.append(4275)
        for row2 in hembras_consumo_filtered:
            if row.semana == row2.semana:
                #objetivos_hembra.append(3728)
                #objetivos_mixto.append(4000)
                a = (((row.peso_ave*machos_mortalidad_filtered.filter(semana = row.semana).first().saldo_aves)+(row2.peso_ave*hembras_mortalidad_filtered.filter(semana = row2.semana).first().saldo_aves))/((machos_mortalidad_filtered.filter(semana = row.semana).first().saldo_aves)+(hembras_mortalidad_filtered.filter(semana = row2.semana).first().saldo_aves)))
                b = ((row.peso_ave*machos_mortalidad_filtered.filter(semana = row.semana).first().saldo_aves)+(row2.peso_ave*hembras_mortalidad_filtered.filter(semana = row2.semana).first().saldo_aves))
                mixto_pesos_semanas.append(round(a,0))
                mixto_conversion_semanas.append(round(((row.consumo_ave*machos_mortalidad_filtered.filter(semana = row.semana).first().saldo_aves)+(row2.consumo_ave*hembras_mortalidad_filtered.filter(semana = row2.semana).first().saldo_aves))/b,2))

    return render(request, 'conversion.html', {
        'machos_consumo_filtered' : machos_consumo_filtered,
        'hembras_consumo_filtered' : hembras_consumo_filtered,
        'machos_conversion_actual' : machos_conversion_actual,
        'hembras_conversion_actual' : hembras_conversion_actual,
        'semanas' : semanas,
        'mixto_conversion_semanas' : mixto_conversion_semanas,
        'objetivos_mixto' : objetivos_mixto,
        'objetivos_macho' : objetivos_macho,
        'objetivos_hembra' : objetivos_hembra,
        'mixto_conversion_actual' : mixto_conversion_semanas[-1],
        })

#visual para grafica de evolución de peso
@login_required
def visual_Evolucion_Peso(request):
    ciclo_actual = int(Cicloproduccion.objects.order_by('-ciclo').first().ciclo)
    machos_consumo_filtered = Alimento.objects.filter(user = request.user, 
                                                      ciclo = ciclo_actual,
                                                      sexo = 'Macho')
    hembras_consumo_filtered = Alimento.objects.filter(user = request.user, 
                                                      ciclo = ciclo_actual,
                                                      sexo = 'Hembra')
    machos_peso_actual = round(machos_consumo_filtered.order_by('-semana').first().peso_ave,0)
    hembras_peso_actual = round(hembras_consumo_filtered.order_by('-semana').first().peso_ave,0)
    machos_mortalidad_filtered = Mortalidad.objects.filter(user = request.user, 
                                                            ciclo = ciclo_actual,
                                                            sexo = 'Macho')
    hembras_mortalidad_filtered = Mortalidad.objects.filter(user = request.user,
                                                            ciclo = ciclo_actual, 
                                                            sexo = 'Hembra')
    semanas = []
    mixto_pesos_semanas = []
    objetivos_mixto = 4000
    objetivos_macho = 4275
    objetivos_hembra = 3728

    for row in machos_consumo_filtered:
        semanas.append(row.semana)
        #objetivos_macho.append(4275)
        for row2 in hembras_consumo_filtered:
            if row.semana == row2.semana:
                #objetivos_hembra.append(3728)
                #objetivos_mixto.append(4000)
                mixto_pesos_semanas.append(round((((row.peso_ave*machos_mortalidad_filtered.filter(semana = row.semana).first().saldo_aves)+(row2.peso_ave*hembras_mortalidad_filtered.filter(semana = row2.semana).first().saldo_aves))/((machos_mortalidad_filtered.filter(semana = row.semana).first().saldo_aves)+(hembras_mortalidad_filtered.filter(semana = row2.semana).first().saldo_aves))),0))


    return render(request, 'peso.html', {
        'machos_consumo_filtered' : machos_consumo_filtered, 
        'hembras_consumo_filtered' : hembras_consumo_filtered,
        'machos_peso_actual' : machos_peso_actual,
        'hembras_peso_actual' : hembras_peso_actual,
        'semanas' : semanas,
        'mixto_pesos_semanas' : mixto_pesos_semanas,
        'objetivos_hembra': objetivos_hembra,
        'objetivos_macho': objetivos_macho,
        'objetivos_mixto': objetivos_mixto,
        'mixto_peso_actual' : mixto_pesos_semanas[-1]
        })

#visual para grafica de mortalidad
@login_required
def visual_Mortalidad(request):
    ciclo_actual = int(Cicloproduccion.objects.order_by('-ciclo').first().ciclo)
    machos_mortalidad_filtered = Mortalidad.objects.filter(user = request.user, 
                                                            ciclo = ciclo_actual,
                                                            sexo = 'Macho')
    hembras_mortalidad_filtered = Mortalidad.objects.filter(user = request.user,
                                                            ciclo = ciclo_actual, 
                                                            sexo = 'Hembra')
    machos_final = machos_mortalidad_filtered.order_by('-semana').first().saldo_aves
    hembras_final = hembras_mortalidad_filtered.order_by('-semana').first().saldo_aves
    machos_inicial = Cicloproduccion.objects.filter(user = request.user, 
                                                    ciclo = ciclo_actual, 
                                                    sexo = 'Macho').first().aves_iniciales
    hembras_inicial = Cicloproduccion.objects.filter(user = request.user, 
                                                     ciclo = ciclo_actual, 
                                                     sexo = 'Hembra').first().aves_iniciales
    mixto_inicial = machos_inicial + hembras_inicial
    semanas = []
    mixto_acumulados_porcentaje = []
    objetivo = []
    for row in machos_mortalidad_filtered:
        semanas.append(row.semana)
        for row2 in hembras_mortalidad_filtered:
            if row2.semana == row.semana:
                objetivo.append(10)
                mixto_acumulados_porcentaje.append(
                    round(((mixto_inicial-row.saldo_aves-row2.saldo_aves)/mixto_inicial),2))
            
    
    return render(request, 'mortalidad.html', { 'user' : request.user,
        'data_machos': machos_mortalidad_filtered, 
        'data_hembras': hembras_mortalidad_filtered, 'semanas' :semanas, 
        'mixto_acumulados_porcentaje' : mixto_acumulados_porcentaje, 
        'machos_inicial' : machos_inicial, 'hembras_inicial': hembras_inicial, 
        'mixto_inicial': mixto_inicial, 'objetivo' : objetivo ,
        'mixto_final': (machos_final+hembras_final),
        'machos_final': machos_final, 'hembras_final':hembras_final})