from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.shortcuts import redirect
from django.db import IntegrityError
from django.contrib.auth.forms import AuthenticationForm
from django.views.generic import TemplateView
from .models import Cicloproduccion, Mortalidad, Alimento, imagenes_calificacion
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

# class Graficos(TemplateView):
#     template_name = 'indiceproductividad.html'

#     #@login_required
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context["qs"] = Cicloproduccion.objects.filter(ciclo = 6, sexo = 'Macho')
#         return context

# #grafica mortalidad machos

# class Graficos2(TemplateView):
#     template_name = 'mortalidad.html'

#     #@login_required
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context["qs"] = Mortalidad.objects.filter( productor = 'Albeiro Hernández', semana = 7, sexo = 'Macho')
#         return context

# #Pendiente de realizar grafica

# class Graficos3(TemplateView):
#     template_name = 'conversion.html'
    
#     #@login_required
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context["qs"] = Alimento.objects.all()
#         return context
    


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


#visual para grafica de indice de productividad
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


# #visual para grafica de conversion alimenticia
# @login_required
# def visual_Conversion_Alimentica(request):
#     ciclo_actual = int(Cicloproduccion.objects.order_by('-ciclo').first().ciclo)
#     machos_consumo_filtered = Alimento.objects.filter(user = request.user, 
#                                                       ciclo = ciclo_actual,
#                                                       sexo = 'Macho')
#     hembras_consumo_filtered = Alimento.objects.filter(user = request.user, 
#                                                       ciclo = ciclo_actual,
#                                                       sexo = 'Hembra')
#     machos_conversion_actual = round(machos_consumo_filtered.order_by('-semana').first().c_a_acum,2)
#     hembras_conversion_actual = round(hembras_consumo_filtered.order_by('-semana').first().c_a_acum,2)
#     machos_mortalidad_filtered = Mortalidad.objects.filter(user = request.user, 
#                                                             ciclo = ciclo_actual,
#                                                             sexo = 'Macho')
#     hembras_mortalidad_filtered = Mortalidad.objects.filter(user = request.user,
#                                                             ciclo = ciclo_actual, 
#                                                             sexo = 'Hembra')
#     semanas = []
#     a = 0
#     b = 0
#     mixto_pesos_semanas = []
#     mixto_conversion_semanas = []
#     objetivos_mixto = 1.69
#     objetivos_macho = 1.65
#     objetivos_hembra = 1.72

#     for row in machos_consumo_filtered:
#         semanas.append(row.semana)
#         #objetivos_macho.append(4275)
#         for row2 in hembras_consumo_filtered:
#             if row.semana == row2.semana:
#                 #objetivos_hembra.append(3728)
#                 #objetivos_mixto.append(4000)
#                 a = (((row.peso_ave*machos_mortalidad_filtered.filter(semana = row.semana).first().saldo_aves)+(row2.peso_ave*hembras_mortalidad_filtered.filter(semana = row2.semana).first().saldo_aves))/((machos_mortalidad_filtered.filter(semana = row.semana).first().saldo_aves)+(hembras_mortalidad_filtered.filter(semana = row2.semana).first().saldo_aves)))
#                 b = ((row.peso_ave*machos_mortalidad_filtered.filter(semana = row.semana).first().saldo_aves)+(row2.peso_ave*hembras_mortalidad_filtered.filter(semana = row2.semana).first().saldo_aves))
#                 mixto_pesos_semanas.append(round(a,0))
#                 mixto_conversion_semanas.append(round(((row.consumo_ave*machos_mortalidad_filtered.filter(semana = row.semana).first().saldo_aves)+(row2.consumo_ave*hembras_mortalidad_filtered.filter(semana = row2.semana).first().saldo_aves))/b,2))

#     return render(request, 'conversion.html', {
#         'machos_consumo_filtered' : machos_consumo_filtered,
#         'hembras_consumo_filtered' : hembras_consumo_filtered,
#         'machos_conversion_actual' : machos_conversion_actual,
#         'hembras_conversion_actual' : hembras_conversion_actual,
#         'semanas' : semanas,
#         'mixto_conversion_semanas' : mixto_conversion_semanas,
#         'objetivos_mixto' : objetivos_mixto,
#         'objetivos_macho' : objetivos_macho,
#         'objetivos_hembra' : objetivos_hembra,
#         'mixto_conversion_actual' : mixto_conversion_semanas[-1],
#         'ciclo_actual': ciclo_actual
#         })

# #visual para grafica de evolución de peso
# @login_required
# def visual_Evolucion_Peso(request):
#     ciclo_actual = int(Cicloproduccion.objects.order_by('-ciclo').first().ciclo)
#     machos_consumo_filtered = Alimento.objects.filter(user = request.user, 
#                                                       ciclo = ciclo_actual,
#                                                       sexo = 'Macho')
#     hembras_consumo_filtered = Alimento.objects.filter(user = request.user, 
#                                                       ciclo = ciclo_actual,
#                                                       sexo = 'Hembra')
#     machos_peso_actual = round(machos_consumo_filtered.order_by('-semana').first().peso_ave,0)
#     hembras_peso_actual = round(hembras_consumo_filtered.order_by('-semana').first().peso_ave,0)
#     machos_mortalidad_filtered = Mortalidad.objects.filter(user = request.user, 
#                                                             ciclo = ciclo_actual,
#                                                             sexo = 'Macho')
#     hembras_mortalidad_filtered = Mortalidad.objects.filter(user = request.user,
#                                                             ciclo = ciclo_actual, 
#                                                             sexo = 'Hembra')
#     semanas = []
#     mixto_pesos_semanas = []
#     objetivos_mixto = 4000
#     objetivos_macho = 4275
#     objetivos_hembra = 3728

#     for row in machos_consumo_filtered:
#         semanas.append(row.semana)
#         #objetivos_macho.append(4275)
#         for row2 in hembras_consumo_filtered:
#             if row.semana == row2.semana:
#                 #objetivos_hembra.append(3728)
#                 #objetivos_mixto.append(4000)
#                 mixto_pesos_semanas.append(round((((row.peso_ave*machos_mortalidad_filtered.filter(semana = row.semana).first().saldo_aves)+(row2.peso_ave*hembras_mortalidad_filtered.filter(semana = row2.semana).first().saldo_aves))/((machos_mortalidad_filtered.filter(semana = row.semana).first().saldo_aves)+(hembras_mortalidad_filtered.filter(semana = row2.semana).first().saldo_aves))),0))


#     return render(request, 'peso.html', {
#         'machos_consumo_filtered' : machos_consumo_filtered, 
#         'hembras_consumo_filtered' : hembras_consumo_filtered,
#         'machos_peso_actual' : machos_peso_actual,
#         'hembras_peso_actual' : hembras_peso_actual,
#         'semanas' : semanas,
#         'mixto_pesos_semanas' : mixto_pesos_semanas,
#         'objetivos_hembra': objetivos_hembra,
#         'objetivos_macho': objetivos_macho,
#         'objetivos_mixto': objetivos_mixto,
#         'mixto_peso_actual' : mixto_pesos_semanas[-1],
#         'ciclo_actual': ciclo_actual
#         })

# #visual para grafica de mortalidad
# @login_required
# def visual_Mortalidad(request):
#     ciclo_actual = int(Cicloproduccion.objects.order_by('-ciclo').first().ciclo)
#     machos_mortalidad_filtered = Mortalidad.objects.filter(user = request.user, 
#                                                             ciclo = ciclo_actual,
#                                                             sexo = 'Macho')
#     hembras_mortalidad_filtered = Mortalidad.objects.filter(user = request.user,
#                                                             ciclo = ciclo_actual, 
#                                                             sexo = 'Hembra')
#     machos_final = machos_mortalidad_filtered.order_by('-semana').first().saldo_aves
#     hembras_final = hembras_mortalidad_filtered.order_by('-semana').first().saldo_aves
#     machos_inicial = Cicloproduccion.objects.filter(user = request.user, 
#                                                     ciclo = ciclo_actual, 
#                                                     sexo = 'Macho').first().aves_iniciales
#     hembras_inicial = Cicloproduccion.objects.filter(user = request.user, 
#                                                      ciclo = ciclo_actual, 
#                                                      sexo = 'Hembra').first().aves_iniciales
#     mixto_inicial = machos_inicial + hembras_inicial
#     semanas = []
#     mixto_acumulados_porcentaje = []
#     objetivo = []
#     for row in machos_mortalidad_filtered:
#         semanas.append(row.semana)
#         for row2 in hembras_mortalidad_filtered:
#             if row2.semana == row.semana:
#                 mixto_acumulados_porcentaje.append(
#                     round(((mixto_inicial-row.saldo_aves-row2.saldo_aves)/mixto_inicial),2))
                
#     for sem in semanas:
#         objetivo.append(round(sem*(5/semanas[-1]),2))
            
    
#     return render(request, 'mortalidad.html', { 'user' : request.user,
#         'data_machos': machos_mortalidad_filtered, 
#         'data_hembras': hembras_mortalidad_filtered, 'semanas' :semanas, 
#         'mixto_acumulados_porcentaje' : mixto_acumulados_porcentaje, 
#         'machos_inicial' : machos_inicial, 'hembras_inicial': hembras_inicial, 
#         'mixto_inicial': mixto_inicial, 'objetivo' : objetivo ,
#         'mixto_final': (machos_final+hembras_final),
#         'machos_final': machos_final, 'hembras_final':hembras_final, 'ciclo_actual' : ciclo_actual})


#visual para grafica de mortalidad
@login_required
def visual_Mortalidad2(request):
    if request.user.username == "admin":
        logout(request)
        return redirect('home')
    else:
        diccionarios_Medidas_Ciclo_actual = obtenerMedidasGraficos(request)

        datos_mortalidad = diccionarios_Medidas_Ciclo_actual['diccionario_mortalidad']
        
        return render(request, 'mortalidad.html', { 'user' : request.user,
            'machos_acumulados_porcentaje': datos_mortalidad['machos_acumulados_porcentaje'], 
            'hembras_acumulados_porcentaje': datos_mortalidad['hembras_acumulados_porcentaje'], 
            'semanas_posibles' :datos_mortalidad['semanas_posibles'], 
            'mixto_acumulados_porcentaje' : datos_mortalidad['mixto_acumulados_porcentaje'], 
            'machos_aves_inicial' : datos_mortalidad['machos_aves_inicial'], 
            'hembras_aves_inicial': datos_mortalidad['hembras_aves_inicial'], 
            'mixto_aves_inicial': datos_mortalidad['mixto_aves_inicial'], 
            'objetivo_mortalidad':datos_mortalidad['objetivo_mortalidad'],
            'objetivo_aves_semana_mixto':datos_mortalidad['objetivo_aves_semana_mixto'],
            'objetivo_aves_semana_machos':datos_mortalidad['objetivo_aves_semana_machos'],
            'objetivo_aves_semana_hembras':datos_mortalidad['objetivo_aves_semana_hembras'],
            'objetivo_aves_final_mixto' : datos_mortalidad['objetivo_aves_final_mixto'],
            'objetivo_aves_final_machos' : datos_mortalidad['objetivo_aves_final_machos'],
            'objetivo_aves_final_hembras': datos_mortalidad['objetivo_aves_final_hembras'],
            'objetivo_aves_actual_mixto' :  datos_mortalidad['objetivo_aves_actual_mixto'],
            'objetivo_aves_actual_machos' :  datos_mortalidad['objetivo_aves_actual_machos'],
            'objetivo_aves_actual_hembras':  datos_mortalidad['objetivo_aves_actual_hembras'],
            'mixto_aves_final': datos_mortalidad['mixto_aves_final'],
            'machos_aves_final': datos_mortalidad['machos_aves_final'], 
            'hembras_aves_final':datos_mortalidad['hembras_aves_final'], 
            'ultimo_ciclo_mortalidad' : datos_mortalidad['ultimo_ciclo_mortalidad'],
            'ultima_semana_ciclo_mortalidad' : datos_mortalidad['ultima_semana_ciclo_mortalidad']
            }
    )

#visual para grafica de evolución de peso
@login_required
def visual_Evolucion_Peso2(request):
    if request.user.username == "admin":
        logout(request)
        return redirect('home')
    else:
        diccionarios_Medidas_Ciclo_actual = obtenerMedidasGraficos(request)

        datos_pesos = diccionarios_Medidas_Ciclo_actual['diccionario_pesos_CA']
        return render(request, 'peso.html', {
            'ultimo_ciclo_alimento': datos_pesos['ultimo_ciclo_alimento'],
            'ultima_semana_ciclo_alimento':datos_pesos['ultima_semana_ciclo_alimento'],
            'semanas_posibles': datos_pesos['semanas_posibles'], 
            'machos_peso_inicial' : datos_pesos['machos_peso_inicial'],
            'hembras_peso_inicial' : datos_pesos['hembras_peso_inicial'],
            'mixto_peso_inicial' : datos_pesos['mixto_peso_inicial'],
            'machos_peso_final' :datos_pesos['machos_peso_final'],
            'hembras_peso_final':datos_pesos['hembras_peso_final'],
            'mixto_peso_final':datos_pesos['mixto_peso_final'],
            'machos_peso_semanas':datos_pesos['machos_peso_semanas'],
            'hembras_peso_semanas':datos_pesos['hembras_peso_semanas'],
            'mixto_peso_semanas':datos_pesos['mixto_peso_semanas'],
            'objetivo_conversion_alimento_mixto':datos_pesos['objetivo_conversion_alimento_mixto'],
            'objetivo_peso_final_mixto':datos_pesos['objetivo_peso_final_mixto'],
            'objetivo_peso_actual_mixto' : datos_pesos['objetivo_peso_actual_mixto'],
            'objetivo_conversion_alimento_machos':datos_pesos['objetivo_conversion_alimento_machos'],
            'objetivo_peso_final_machos':datos_pesos['objetivo_peso_final_machos'],
            'objetivo_peso_actual_machos' : datos_pesos['objetivo_peso_actual_machos'],
            'objetivo_conversion_alimento_hembras':datos_pesos['objetivo_conversion_alimento_hembras'],
            'objetivo_peso_final_hembras':datos_pesos['objetivo_peso_final_hembras'],
            'objetivo_peso_actual_hembras' : datos_pesos['objetivo_peso_actual_hembras'],
            'objetivo_peso_mixto' : datos_pesos['objetivo_peso_mixto'] ,
            'objetivo_peso_machos' : datos_pesos['objetivo_peso_mixto'],
            'objetivo_peso_hembras' : datos_pesos['objetivo_peso_mixto'],
            'machos_CA_semanas':datos_pesos['machos_CA_semanas'],
            'hembras_CA_semanas':datos_pesos['hembras_CA_semanas'],
            'mixto_CA_semanas': datos_pesos['mixto_CA_semanas'],
            'machos_CA_final':datos_pesos['machos_CA_final'],
            'hembras_CA_final':datos_pesos['hembras_CA_final'],
            'mixto_CA_final':datos_pesos['mixto_CA_final']
            })

#visual para grafica de conversión alimenticia
@login_required
def visual_Conversion_Alimenticia2(request):
    if request.user.username == "admin":
        logout(request)
        return redirect('home')
    else:
        diccionarios_Medidas_Ciclo_actual = obtenerMedidasGraficos(request)

        datos_pesos = diccionarios_Medidas_Ciclo_actual['diccionario_pesos_CA']
        return render(request, 'conversion.html', {
            'ultimo_ciclo_alimento': datos_pesos['ultimo_ciclo_alimento'],
            'ultima_semana_ciclo_alimento':datos_pesos['ultima_semana_ciclo_alimento'],
            'semanas_posibles': datos_pesos['semanas_posibles'], 
            'machos_peso_inicial' : datos_pesos['machos_peso_inicial'],
            'hembras_peso_inicial' : datos_pesos['hembras_peso_inicial'],
            'mixto_peso_inicial' : datos_pesos['mixto_peso_inicial'],
            'machos_peso_final' :datos_pesos['machos_peso_final'],
            'hembras_peso_final':datos_pesos['hembras_peso_final'],
            'mixto_peso_final':datos_pesos['mixto_peso_final'],
            'machos_peso_semanas':datos_pesos['machos_peso_semanas'],
            'hembras_peso_semanas':datos_pesos['hembras_peso_semanas'],
            'mixto_peso_semanas':datos_pesos['mixto_peso_semanas'],
            'objetivo_conversion_alimento_mixto':datos_pesos['objetivo_conversion_alimento_mixto'],
            'objetivo_peso_final_mixto':datos_pesos['objetivo_peso_final_mixto'],
            'objetivo_peso_actual_mixto' : datos_pesos['objetivo_peso_actual_mixto'],
            'objetivo_conversion_alimento_machos':datos_pesos['objetivo_conversion_alimento_machos'],
            'objetivo_peso_final_machos':datos_pesos['objetivo_peso_final_machos'],
            'objetivo_peso_actual_machos' : datos_pesos['objetivo_peso_actual_machos'],
            'objetivo_conversion_alimento_hembras':datos_pesos['objetivo_conversion_alimento_hembras'],
            'objetivo_peso_final_hembras':datos_pesos['objetivo_peso_final_hembras'],
            'objetivo_peso_actual_hembras' : datos_pesos['objetivo_peso_actual_hembras'],
            'objetivo_peso_mixto' : datos_pesos['objetivo_peso_mixto'] ,
            'objetivo_peso_machos' : datos_pesos['objetivo_peso_mixto'],
            'objetivo_peso_hembras' : datos_pesos['objetivo_peso_mixto'],
            'machos_CA_semanas':datos_pesos['machos_CA_semanas'],
            'hembras_CA_semanas':datos_pesos['hembras_CA_semanas'],
            'mixto_CA_semanas': datos_pesos['mixto_CA_semanas'],
            'machos_CA_final':datos_pesos['machos_CA_final'],
            'hembras_CA_final':datos_pesos['hembras_CA_final'],
            'mixto_CA_final':datos_pesos['mixto_CA_final'],
            'objetivo_conversion_actual_machos' : datos_pesos['objetivo_conversion_actual_machos'],
            'objetivo_conversion_actual_hembras' : datos_pesos['objetivo_conversion_actual_hembras'],
            'objetivo_conversion_actual_mixto' : datos_pesos['objetivo_conversion_actual_mixto'],
            'objetivo_conversion_final_machos' : datos_pesos['objetivo_conversion_final_machos'],
            'objetivo_conversion_final_hembras': datos_pesos['objetivo_conversion_final_hembras'],
            'objetivo_conversion_final_mixto' : datos_pesos['objetivo_conversion_final_mixto']
            })

@login_required
def visual_Resumen(request):
    if request.user.username == "admin":
        logout(request)
        return redirect('home')
    else:
        diccionarios_Medidas_Ciclo_actual = obtenerMedidasGraficos(request)

        datos_mortalidad = diccionarios_Medidas_Ciclo_actual['diccionario_mortalidad']
        datos_pesos = diccionarios_Medidas_Ciclo_actual['diccionario_pesos_CA']
        datos_IP = diccionarios_Medidas_Ciclo_actual['diccionario_ciclos_IP']
        bueno = imagenes_calificacion.objects.filter( clasificacion = 'bueno')
        excelente = imagenes_calificacion.objects.filter( clasificacion = 'excelente').distinct()
        regular = imagenes_calificacion.objects.filter( clasificacion = 'regular').distinct()
        
        return render(request, 'resumen.html', { 'user' : request.user,
            'machos_acumulados_porcentaje': datos_mortalidad['machos_acumulados_porcentaje'], 
            'hembras_acumulados_porcentaje': datos_mortalidad['hembras_acumulados_porcentaje'], 
            'semanas_posibles' :datos_mortalidad['semanas_posibles'], 
            'mixto_acumulados_porcentaje' : datos_mortalidad['mixto_acumulados_porcentaje'], 
            'machos_aves_inicial' : datos_mortalidad['machos_aves_inicial'], 
            'hembras_aves_inicial': datos_mortalidad['hembras_aves_inicial'], 
            'mixto_aves_inicial': datos_mortalidad['mixto_aves_inicial'], 
            'objetivo_mortalidad':datos_mortalidad['objetivo_mortalidad'],
            'objetivo_aves_semana_mixto':datos_mortalidad['objetivo_aves_semana_mixto'],
            'objetivo_aves_semana_machos':datos_mortalidad['objetivo_aves_semana_machos'],
            'objetivo_aves_semana_hembras':datos_mortalidad['objetivo_aves_semana_hembras'],
            'objetivo_aves_final_mixto' : datos_mortalidad['objetivo_aves_final_mixto'],
            'objetivo_aves_final_machos' : datos_mortalidad['objetivo_aves_final_machos'],
            'objetivo_aves_final_hembras': datos_mortalidad['objetivo_aves_final_hembras'],
            'objetivo_aves_actual_mixto' :  datos_mortalidad['objetivo_aves_actual_mixto'],
            'objetivo_aves_actual_machos' :  datos_mortalidad['objetivo_aves_actual_machos'],
            'objetivo_aves_actual_hembras':  datos_mortalidad['objetivo_aves_actual_hembras'],
            'mixto_aves_final': datos_mortalidad['mixto_aves_final'],
            'machos_aves_final': datos_mortalidad['machos_aves_final'], 
            'hembras_aves_final':datos_mortalidad['hembras_aves_final'], 
            'ultimo_ciclo_mortalidad' : datos_mortalidad['ultimo_ciclo_mortalidad'],
            'ultima_semana_ciclo_mortalidad' : datos_mortalidad['ultima_semana_ciclo_mortalidad'],
            'ultimo_ciclo_alimento': datos_pesos['ultimo_ciclo_alimento'],
            'ultima_semana_ciclo_alimento':datos_pesos['ultima_semana_ciclo_alimento'],
            'machos_peso_inicial' : datos_pesos['machos_peso_inicial'],
            'hembras_peso_inicial' : datos_pesos['hembras_peso_inicial'],
            'mixto_peso_inicial' : datos_pesos['mixto_peso_inicial'],
            'machos_peso_final' :datos_pesos['machos_peso_final'],
            'hembras_peso_final':datos_pesos['hembras_peso_final'],
            'mixto_peso_final':datos_pesos['mixto_peso_final'],
            'machos_peso_semanas':datos_pesos['machos_peso_semanas'],
            'hembras_peso_semanas':datos_pesos['hembras_peso_semanas'],
            'mixto_peso_semanas':datos_pesos['mixto_peso_semanas'],
            'objetivo_conversion_alimento_mixto':datos_pesos['objetivo_conversion_alimento_mixto'],
            'objetivo_peso_final_mixto':datos_pesos['objetivo_peso_final_mixto'],
            'objetivo_peso_actual_mixto' : datos_pesos['objetivo_peso_actual_mixto'],
            'objetivo_conversion_alimento_machos':datos_pesos['objetivo_conversion_alimento_machos'],
            'objetivo_peso_final_machos':datos_pesos['objetivo_peso_final_machos'],
            'objetivo_peso_actual_machos' : datos_pesos['objetivo_peso_actual_machos'],
            'objetivo_conversion_alimento_hembras':datos_pesos['objetivo_conversion_alimento_hembras'],
            'objetivo_peso_final_hembras':datos_pesos['objetivo_peso_final_hembras'],
            'objetivo_peso_actual_hembras' : datos_pesos['objetivo_peso_actual_hembras'],
            'objetivo_peso_mixto' : datos_pesos['objetivo_peso_mixto'] ,
            'objetivo_peso_machos' : datos_pesos['objetivo_peso_mixto'],
            'objetivo_peso_hembras' : datos_pesos['objetivo_peso_mixto'],
            'machos_CA_semanas':datos_pesos['machos_CA_semanas'],
            'hembras_CA_semanas':datos_pesos['hembras_CA_semanas'],
            'mixto_CA_semanas': datos_pesos['mixto_CA_semanas'],
            'machos_CA_final':datos_pesos['machos_CA_final'],
            'hembras_CA_final':datos_pesos['hembras_CA_final'],
            'mixto_CA_final':datos_pesos['mixto_CA_final'],
            'objetivo_conversion_actual_machos' : datos_pesos['objetivo_conversion_actual_machos'],
            'objetivo_conversion_actual_hembras' : datos_pesos['objetivo_conversion_actual_hembras'],
            'objetivo_conversion_actual_mixto' : datos_pesos['objetivo_conversion_actual_mixto'],
            'objetivo_conversion_final_machos' : datos_pesos['objetivo_conversion_final_machos'],
            'objetivo_conversion_final_hembras': datos_pesos['objetivo_conversion_final_hembras'],
            'objetivo_conversion_final_mixto' : datos_pesos['objetivo_conversion_final_mixto'],
            'ultimo_ciclo_ciclos_produccion' : datos_IP['ultimo_ciclo_ciclos_produccion'],
            'ultimo_ip_usuario' : datos_IP['ultimo_ip_usuario'],
            'regular' : regular,
            'bueno' : bueno,
            'excelente' : excelente
            })

@login_required
def visual_Indice_productividad2(request):
    if request.user.username == "admin":
        logout(request)
        return redirect('home')
    else:
        diccionarios_Medidas_Ciclo_actual = obtenerMedidasGraficos(request)
        datos_IP = diccionarios_Medidas_Ciclo_actual['diccionario_ciclos_IP']
        bueno = imagenes_calificacion.objects.filter( clasificacion = 'bueno')
        excelente = imagenes_calificacion.objects.filter( clasificacion = 'excelente').distinct()
        regular = imagenes_calificacion.objects.filter( clasificacion = 'regular').distinct()
        return render(request, "indiceproductividad.html", {
            'ciclos_posibles' : datos_IP['ciclos_posibles'],
            'ip_ciclos_posibles' : datos_IP['ip_ciclos_posibles'],
            'productores' : datos_IP['productores'],
            'ip_productores' : datos_IP['ip_productores'],
            'ultimo_ciclo_ciclos_produccion' : datos_IP['ultimo_ciclo_ciclos_produccion'],
            'ultimo_ip_usuario' : datos_IP['ultimo_ip_usuario'],
            'regular' : regular,
            'bueno' : bueno,
            'excelente' : excelente
            }
        )



@login_required
def obtenerMedidasGraficos(request):
    alimento_filto = Alimento.objects.filter(user = request.user)
    mortalidad_filtro = Mortalidad.objects.filter(user = request.user)
    ciclos_filtro_usuario = Cicloproduccion.objects.filter(user = request.user)
    ultimo_ciclo_alimento = int(alimento_filto.order_by('-ciclo').first().ciclo)
    ultimo_ciclo_mortalidad = int(mortalidad_filtro.order_by('-ciclo').first().ciclo)
    ultimo_ciclo_ciclos_produccion = int(ciclos_filtro_usuario.order_by('-ciclo').first().ciclo)
    alimento_filto = alimento_filto.filter(ciclo = ultimo_ciclo_alimento)
    #mortalidad_filtro = mortalidad_filtro.filter(ciclo = ultimo_ciclo_mortalidad)


    ultima_semana_ciclo_alimento = int(alimento_filto.order_by('-semana').first().semana)
    ultima_semana_ciclo_mortalidad = int(mortalidad_filtro.filter(ciclo = ultimo_ciclo_mortalidad).order_by('-semana').first().semana)
    
    #definicion de objetivos
    semanas_posibles = list(range(1,8))
    objetivo_conversion_alimento_mixto =[0.891, 1.029,1.182,1.322,1.441,1.555,1.686]
    objetivo_peso_mixto =[202,570,1116,1783,2521,3278,4001]
    objetivo_conversion_alimento_machos =[0.883,1.018,1.166,1.301,1.417,1.518,1.653]
    objetivo_peso_machos =[205,603,1188,1904,2694,3503,4275]
    objetivo_conversion_alimento_hembras =[0.884,1.041,1.200,1.346,1.469,1.527,1.724]
    objetivo_peso_hembras =[199,537,1043,1662,2348,3052,3728]
    objetivo_mortalidad =[0.0071,0.0224,0.0313,0.0377,0.0426,0.0466,0.05]
    objetivo_supervivencia = [1 - obj for obj in objetivo_mortalidad ]

    # Informacion relevante diccionario mortalidad: aves iniciales, actuales y finales, objetivos, mortalidades acumuladas
    machos_aves_inicial = int(ciclos_filtro_usuario.filter(ciclo = ultimo_ciclo_mortalidad, sexo = 'Macho').first().aves_iniciales)
    hembras_aves_inicial = int(ciclos_filtro_usuario.filter(ciclo = ultimo_ciclo_mortalidad, sexo = 'Hembra').first().aves_iniciales)
    mixto_aves_inicial = machos_aves_inicial + hembras_aves_inicial
    machos_aves_final = int(mortalidad_filtro.filter(sexo ='Macho', ciclo = ultimo_ciclo_mortalidad).order_by('-semana').first().saldo_aves)
    hembras_aves_final = int(mortalidad_filtro.filter(sexo ='Hembra', ciclo = ultimo_ciclo_mortalidad).order_by('-semana').first().saldo_aves)
    mixto_aves_final = machos_aves_final + hembras_aves_final
    objetivo_aves_semana_mixto = [i*mixto_aves_inicial for i in objetivo_supervivencia]
    objetivo_aves_semana_machos = [i*machos_aves_inicial for i in objetivo_supervivencia]
    objetivo_aves_semana_hembras = [i*hembras_aves_inicial for i in objetivo_supervivencia]

    machos_acumulados_porcentaje = list(mortalidad_filtro.filter(sexo = "Macho", ciclo = ultimo_ciclo_mortalidad).order_by('semana').values_list("acumulada_porcentaje", flat = True))
    hembras_acumulados_porcentaje = list(mortalidad_filtro.filter(sexo = "Hembra",ciclo = ultimo_ciclo_mortalidad).order_by('semana').values_list("acumulada_porcentaje", flat = True))
    mixto_acumulados_porcentaje =[]

    # if len(machos_acumulados_porcentaje) <7:
    #     for i in range(1, 8 -len(machos_acumulados_porcentaje)):
    #         machos_acumulados_porcentaje.append(None)
        
    # if len(hembras_acumulados_porcentaje) <7:
    #     for i in range(1, 8 -len(machos_acumulados_porcentaje)):
    #         machos_acumulados_porcentaje.append(None)    

    for row in mortalidad_filtro.filter(sexo = "Macho", ciclo = ultimo_ciclo_mortalidad).order_by('semana'):
        for row2 in mortalidad_filtro.filter(sexo = "Hembra", ciclo = ultimo_ciclo_mortalidad).order_by('semana'):
            if row2.semana == row.semana:
                mixto_acumulados_porcentaje.append(
                    ((mixto_aves_inicial-row.saldo_aves-row2.saldo_aves)/mixto_aves_inicial))
    
    #if len(mixto_acumulados_porcentaje) <7:
    #    for i in range(1, 8 -len(mixto_acumulados_porcentaje)):
    #        mixto_acumulados_porcentaje.append(None)  


    #Información relevante diccionario peso y conversion: pesos, CA iniciales finales y por semana
    machos_peso_semanas = list(alimento_filto.filter(sexo = "Macho").order_by('semana').values_list("peso_ave", flat = True))
    hembras_peso_semanas = list(alimento_filto.filter(sexo = "Hembra").order_by('semana').values_list("peso_ave", flat = True))
    mixto_peso_semanas = []
    for row in alimento_filto.filter(sexo = "Macho").order_by('semana'):
        for row2 in alimento_filto.filter(sexo = "Macho").order_by('semana'):
            if row.semana == row2.semana:
                if (mortalidad_filtro.filter(semana = row.semana, sexo ='Macho', ciclo = ultimo_ciclo_alimento).first()!= None) & (mortalidad_filtro.filter(semana = row2.semana, sexo = 'Hembra', ciclo = ultimo_ciclo_alimento).first() != None):
                    mixto_peso_semanas.append(round((((row.peso_ave*mortalidad_filtro.filter(semana = row.semana, sexo ='Macho', ciclo = ultimo_ciclo_alimento).first().saldo_aves)+(row2.peso_ave*mortalidad_filtro.filter(semana = row2.semana, sexo = 'Hembra', ciclo = ultimo_ciclo_alimento).first().saldo_aves))/((mortalidad_filtro.filter(semana = row.semana, sexo = 'Macho', ciclo = ultimo_ciclo_alimento).first().saldo_aves)+(mortalidad_filtro.filter(semana = row2.semana, sexo = 'Hembra', ciclo = ultimo_ciclo_alimento).first().saldo_aves))),0))
                
    machos_peso_final = int(machos_peso_semanas[-1])
    hembras_peso_final = int(hembras_peso_semanas[-1])
    if len(mixto_peso_semanas)>0:
        mixto_peso_final = int(mixto_peso_semanas[-1])
    else:
        mixto_peso_final = 0

    #completar informacion de 7 semanas
    # if len(machos_peso_semanas) <7:
    #         for i in range(1, 8 -len(machos_peso_semanas)):
    #             machos_peso_semanas.append(None)

    # if len(hembras_peso_semanas) <7:
    #         for i in range(1, 8 -len(hembras_peso_semanas)):
    #             hembras_peso_semanas.append(None)

    # if len(mixto_peso_semanas) <7:
    #         for i in range(1, 8 -len(mixto_peso_semanas)):
    #             mixto_peso_semanas.append(None)
        
    machos_peso_inicial = int(ciclos_filtro_usuario.filter(ciclo = ultimo_ciclo_alimento, sexo = 'Macho').first().peso_inicial_gramos)
    hembras_peso_inicial = int(ciclos_filtro_usuario.filter(ciclo = ultimo_ciclo_alimento, sexo = 'Hembra').first().peso_inicial_gramos)
    mixto_peso_inicial = ((machos_peso_inicial*machos_aves_inicial)+(hembras_peso_inicial*hembras_aves_inicial))/mixto_aves_inicial
   

    machos_CA_semanas = list(alimento_filto.filter(sexo = "Macho").order_by('semana').values_list("c_a_acum", flat = True))
    hembras_CA_semanas = list(alimento_filto.filter(sexo = "Hembra").order_by('semana').values_list("c_a_acum", flat = True))
    mixto_CA_semanas=[]
    for row in alimento_filto.filter(sexo = "Macho").order_by('semana'):
        for row2 in alimento_filto.filter(sexo = "Macho").order_by('semana'):
            if row.semana == row2.semana:
                if (mortalidad_filtro.filter(semana = row.semana, sexo ='Macho', ciclo = ultimo_ciclo_alimento).first()!= None) & (mortalidad_filtro.filter(semana = row2.semana, sexo = 'Hembra', ciclo = ultimo_ciclo_alimento).first() != None):
                    #a = (((row.peso_ave*mortalidad_filtro.filter(semana = row.semana, sexo = 'Macho', ciclo = ultimo_ciclo_alimento).first().saldo_aves)+(row2.peso_ave*mortalidad_filtro.filter(semana = row2.semana, sexo = 'Hembra', ciclo = ultimo_ciclo_alimento).first().saldo_aves))/((mortalidad_filtro.filter(semana = row.semana, sexo = 'Macho', ciclo = ultimo_ciclo_alimento).first().saldo_aves)+(mortalidad_filtro.filter(semana = row2.semana, sexo = 'Hembra', ciclo = ultimo_ciclo_alimento).first().saldo_aves)))
                    b = ((row.peso_ave*mortalidad_filtro.filter(semana = row.semana, sexo = 'Macho', ciclo = ultimo_ciclo_alimento).first().saldo_aves)+(row2.peso_ave*mortalidad_filtro.filter(semana = row2.semana, sexo = 'Hembra', ciclo = ultimo_ciclo_alimento).first().saldo_aves))
                    mixto_CA_semanas.append(((row.consumo_ave*mortalidad_filtro.filter(semana = row.semana, sexo = 'Macho', ciclo = ultimo_ciclo_alimento).first().saldo_aves)+(row2.consumo_ave*mortalidad_filtro.filter(semana = row2.semana, sexo = 'Hembra', ciclo = ultimo_ciclo_alimento).first().saldo_aves))/b)


    machos_CA_final = round(machos_CA_semanas[-1],2)
    hembras_CA_final = round(hembras_CA_semanas[-1],2)
    if len(mixto_peso_semanas)>0:
        mixto_CA_final = round(mixto_CA_semanas[-1],2)
    else:
        mixto_CA_final = 0

    #completar informacion de 7 semanas
    # if len(machos_CA_semanas) <7:
    #         for i in range(1, 8 -len(machos_CA_semanas)):
    #             machos_CA_semanas.append(None)

    # if len(hembras_CA_semanas) <7:
    #         for i in range(1, 8 -len(hembras_CA_semanas)):
    #             hembras_CA_semanas.append(None)

    # if len(mixto_CA_semanas) <7:
    #         for i in range(1, 8 -len(mixto_CA_semanas)):
    #             mixto_CA_semanas.append(None)

    ciclos_posibles =[]
    ip_ciclos_posibles = []

    ciclos_filtro_usuario = ciclos_filtro_usuario.filter(sexo = 'Macho')

    ciclos_posibles = ciclos_filtro_usuario.order_by('-ciclo').values_list('ciclo', flat = True)
    ip_ciclos_posibles = ciclos_filtro_usuario.order_by('-ciclo').values_list('indice_productividad', flat = True)

    if len(ciclos_posibles)>6 :
        for i in range(0, len(ciclos_posibles)):
            del ciclos_posibles[6+i]
            del ip_ciclos_posibles[6+i]

    # for i in range(0,7):
    #     if len(list(ciclos_filtro_usuario.order_by('-ciclo').values_list('ciclo', flat = True))) >i:
    #         ciclos_posibles.append(ciclos_filtro_usuario.order_by('-ciclo')[i].ciclo)
    #         ip_ciclos_posibles.append(round(ciclos_filtro_usuario.order_by('-ciclo')[i].indice_productividad,2))
    
    ciclos_productores_filtro_ultimo_ciclo = Cicloproduccion.objects.filter(sexo = 'Macho', ciclo = ultimo_ciclo_ciclos_produccion).order_by('-indice_productividad')
    productores = list(ciclos_productores_filtro_ultimo_ciclo.values_list('productor', flat= True))
    ip_productores = list(ciclos_productores_filtro_ultimo_ciclo.values_list('indice_productividad', flat= True))


    diccionario_ciclos_IP ={
        'ciclos_posibles' : ciclos_posibles.reverse,
        'ip_ciclos_posibles' : ip_ciclos_posibles.reverse,
        'productores' : productores,
        'ip_productores' : ip_productores,
        'ultimo_ciclo_ciclos_produccion' : ultimo_ciclo_ciclos_produccion,
        'ultimo_ip_usuario' : round(ciclos_filtro_usuario.order_by('-ciclo')[0].indice_productividad,2)
    }

    diccionario_mortalidad = {
        'ultimo_ciclo_mortalidad' : ultimo_ciclo_mortalidad,
        'ultima_semana_ciclo_mortalidad' : ultima_semana_ciclo_mortalidad,
        'semanas_posibles': semanas_posibles, 
        'machos_acumulados_porcentaje':machos_acumulados_porcentaje,
        'hembras_acumulados_porcentaje' : hembras_acumulados_porcentaje,
        'mixto_acumulados_porcentaje' : mixto_acumulados_porcentaje,
        'objetivo_mortalidad':objetivo_mortalidad,
        'objetivo_aves_semana_mixto':objetivo_aves_semana_mixto,
        'objetivo_aves_semana_machos':objetivo_aves_semana_machos,
        'objetivo_aves_semana_hembras':objetivo_aves_semana_hembras,
        'objetivo_aves_final_mixto' : round(objetivo_aves_semana_mixto[-1]),
        'objetivo_aves_final_machos' : round(objetivo_aves_semana_machos[-1]),
        'objetivo_aves_final_hembras': round(objetivo_aves_semana_hembras[-1]),
        'objetivo_aves_actual_mixto' : round(objetivo_aves_semana_mixto[ultima_semana_ciclo_mortalidad-1]),
        'objetivo_aves_actual_machos' : round(objetivo_aves_semana_machos[ultima_semana_ciclo_mortalidad-1]),
        'objetivo_aves_actual_hembras': round(objetivo_aves_semana_hembras[ultima_semana_ciclo_mortalidad-1]),
        'machos_aves_inicial':machos_aves_inicial,
        'hembras_aves_inicial': hembras_aves_inicial,
        'mixto_aves_inicial' : mixto_aves_inicial,
        'machos_aves_final': machos_aves_final,
        'hembras_aves_final': hembras_aves_final,
        'mixto_aves_final': mixto_aves_final
    }
    
    diccionario_pesos_CA={
        'ultimo_ciclo_alimento': ultimo_ciclo_alimento,
        'ultima_semana_ciclo_alimento':ultima_semana_ciclo_alimento,
        'semanas_posibles': semanas_posibles, 
        'machos_peso_inicial' : machos_peso_inicial,
        'hembras_peso_inicial' : hembras_peso_inicial,
        'mixto_peso_inicial' : mixto_peso_inicial,
        'machos_peso_final' :machos_peso_final,
        'hembras_peso_final':hembras_peso_final,
        'mixto_peso_final':mixto_peso_final,
        'machos_peso_semanas':machos_peso_semanas,
        'hembras_peso_semanas':hembras_peso_semanas,
        'mixto_peso_semanas':mixto_peso_semanas,
        'objetivo_peso_mixto' : objetivo_peso_mixto ,
        'objetivo_peso_machos' : objetivo_peso_mixto,
        'objetivo_peso_hembras' : objetivo_peso_mixto,
        'objetivo_conversion_alimento_mixto':objetivo_conversion_alimento_mixto,
        'objetivo_peso_final_mixto':objetivo_peso_mixto[-1],
        'objetivo_peso_actual_mixto':objetivo_peso_mixto[ultima_semana_ciclo_alimento-1],
        'objetivo_conversion_actual_mixto': objetivo_conversion_alimento_mixto[ultima_semana_ciclo_alimento-1],
        'objetivo_conversion_final_mixto': objetivo_conversion_alimento_mixto[-1],
        'objetivo_conversion_alimento_machos':objetivo_conversion_alimento_machos,
        'objetivo_peso_final_machos':objetivo_peso_machos[-1],
        'objetivo_peso_actual_machos':objetivo_peso_machos[ultima_semana_ciclo_alimento-1],
        'objetivo_conversion_actual_machos':objetivo_conversion_alimento_machos[ultima_semana_ciclo_alimento-1],
        'objetivo_conversion_final_machos':objetivo_conversion_alimento_machos[-1],
        'objetivo_conversion_alimento_hembras':objetivo_conversion_alimento_hembras,
        'objetivo_peso_final_hembras':objetivo_peso_hembras[-1],
        'objetivo_peso_actual_hembras':objetivo_peso_hembras[ultima_semana_ciclo_alimento-1],
        'objetivo_conversion_actual_hembras':objetivo_conversion_alimento_hembras[ultima_semana_ciclo_alimento-1],
        'objetivo_conversion_final_hembras':objetivo_conversion_alimento_hembras[-1],
        'machos_CA_semanas':machos_CA_semanas,
        'hembras_CA_semanas':hembras_CA_semanas,
        'mixto_CA_semanas': mixto_CA_semanas,
        'machos_CA_final':machos_CA_final,
        'hembras_CA_final':hembras_CA_final,
        'mixto_CA_final':mixto_CA_final
    }

    return ({'diccionario_mortalidad':diccionario_mortalidad, 'diccionario_pesos_CA':diccionario_pesos_CA, 'diccionario_ciclos_IP' : diccionario_ciclos_IP})











