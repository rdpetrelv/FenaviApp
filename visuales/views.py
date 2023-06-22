from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.shortcuts import redirect
from django.db import IntegrityError
from django.contrib.auth.forms import AuthenticationForm
from django.views.generic import TemplateView
from .models import (
    Cicloproduccion,
    Mortalidad,
    Alimento,
    imagenes_calificacion,
    metasIP,
)
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.http import JsonResponse


# Create your views here.
# def conversion(request):
#    return render(request, 'conversion.html')

# def mortalidad(request):
#    return render(request, 'mortalidad.html')

# def indiceproductividad(request):
#    ciclos = Cicloproduccion.objects.all()
#    return render(request, 'indiceproductividad.html', {'ciclos': ciclos})

# Grafica indice de productividad

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
    filter_by_user = Cicloproduccion.objects.filter(user=request.user, sexo="Macho")
    ciclo = []
    ip_ciclo = []
    for data in filter_by_user:
        ciclo.append(data.ciclo)
        ip_ciclo.append(round(data.indice_productividad, 2))

    return JsonResponse(
        {
            "title": "IP ultimos 6 ciclos",
            "data": {
                "labels": ciclo,
                "dataset": [{"label": "Ips ciclos", "data": ip_ciclo}],
            },
        }
    )


@login_required
def ip_comparativa_integrantes(request):
    ciclo_actual = int(Cicloproduccion.objects.order_by("-ciclo").first().ciclo)
    filter_by_ultimo_ciclo = Cicloproduccion.objects.filter(
        sexo="Macho", ciclo=ciclo_actual
    )
    productor = []
    ip_productor = []
    for data in filter_by_ultimo_ciclo:
        productor.append(data.productor)
        ip_productor.append(round(data.indice_productividad, 2))

    return JsonResponse(
        {
            "title": "IP comparativo ultimo ciclo",
            "data": {
                "labels": productor,
                "dataset": [{"label": "Ips productores", "data": ip_productor}],
            },
        }
    )


# visual para grafica de indice de productividad
@login_required
def visual_Indice_productividad(request):
    filter_by_user = Cicloproduccion.objects.filter(user=request.user, sexo="Macho")
    ciclo = []
    ips_ciclo = []
    for data in filter_by_user:
        ciclo.append(data.ciclo)
        ips_ciclo.append(round(data.indice_productividad, 2))

    ciclo_actual = int(Cicloproduccion.objects.order_by("-ciclo").first().ciclo)
    filter_by_ultimo_ciclo = Cicloproduccion.objects.filter(
        sexo="Macho", ciclo=ciclo_actual
    ).order_by("-indice_productividad")
    productores = []
    ips_productor = []
    for data in filter_by_ultimo_ciclo:
        productores.append(data.productor)
        ips_productor.append(round(data.indice_productividad, 2))

    return render(
        request,
        "indiceproductividad.html",
        {
            "ciclo1": ciclo,
            "ips_ciclo": ips_ciclo,
            "productores": productores,
            "ips_productor": ips_productor,
        },
    )


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


# visual para grafica de mortalidad
@login_required
def visual_Mortalidad2(request):
    if request.user.username == "admin":
        logout(request)
        return redirect("home")
    else:
        diccionarios_Medidas_Ciclo_actual = obtenerMedidasGraficos(request)

        datos_mortalidad = diccionarios_Medidas_Ciclo_actual["diccionario_mortalidad"]
        bueno = imagenes_calificacion.objects.filter(clasificacion="bueno")
        excelente = imagenes_calificacion.objects.filter(
            clasificacion="excelente"
        ).distinct()
        regular = imagenes_calificacion.objects.filter(
            clasificacion="regular"
        ).distinct()
        try:
            hembras_porcentaje_actual = round(
                100 * datos_mortalidad["hembras_acumulados_porcentaje"][-1], 2
            )
            machos_porcentaje_actual = round(
                100 * datos_mortalidad["machos_acumulados_porcentaje"][-1], 2
            )
            mixto_porcentaje_actual = round(
                100 * datos_mortalidad["mixto_acumulados_porcentaje"][-1], 2
            )
        except:
            hembras_porcentaje_actual = 0
            machos_porcentaje_actual = 0
            mixto_porcentaje_actual = 0

        return render(
            request,
            "mortalidad.html",
            {
                "user": request.user,
                "machos_acumulados_porcentaje": datos_mortalidad[
                    "machos_acumulados_porcentaje"
                ],
                "machos_porcentaje_actual": machos_porcentaje_actual,
                "hembras_acumulados_porcentaje": datos_mortalidad[
                    "hembras_acumulados_porcentaje"
                ],
                "hembras_porcentaje_actual": hembras_porcentaje_actual,
                "semanas_posibles": datos_mortalidad["semanas_posibles"],
                "mixto_acumulados_porcentaje": datos_mortalidad[
                    "mixto_acumulados_porcentaje"
                ],
                "mixto_porcentaje_actual": mixto_porcentaje_actual,
                "machos_aves_inicial": datos_mortalidad["machos_aves_inicial"],
                "hembras_aves_inicial": datos_mortalidad["hembras_aves_inicial"],
                "mixto_aves_inicial": datos_mortalidad["mixto_aves_inicial"],
                "objetivo_mortalidad": datos_mortalidad["objetivo_mortalidad"],
                "objetivo_aves_semana_mixto": datos_mortalidad[
                    "objetivo_aves_semana_mixto"
                ],
                "objetivo_aves_semana_machos": datos_mortalidad[
                    "objetivo_aves_semana_machos"
                ],
                "objetivo_aves_semana_hembras": datos_mortalidad[
                    "objetivo_aves_semana_hembras"
                ],
                "objetivo_aves_final_mixto": datos_mortalidad[
                    "objetivo_aves_final_mixto"
                ],
                "objetivo_aves_final_machos": datos_mortalidad[
                    "objetivo_aves_final_machos"
                ],
                "objetivo_aves_final_hembras": datos_mortalidad[
                    "objetivo_aves_final_hembras"
                ],
                "objetivo_aves_actual_mixto": datos_mortalidad[
                    "objetivo_aves_actual_mixto"
                ],
                "objetivo_aves_actual_machos": datos_mortalidad[
                    "objetivo_aves_actual_machos"
                ],
                "objetivo_aves_actual_hembras": datos_mortalidad[
                    "objetivo_aves_actual_hembras"
                ],
                "mixto_aves_final": datos_mortalidad["mixto_aves_final"],
                "machos_aves_final": datos_mortalidad["machos_aves_final"],
                "hembras_aves_final": datos_mortalidad["hembras_aves_final"],
                "ultimo_ciclo_mortalidad": datos_mortalidad["ultimo_ciclo_mortalidad"],
                "ultima_semana_ciclo_mortalidad": datos_mortalidad[
                    "ultima_semana_ciclo_mortalidad"
                ],
                "regular": regular,
                "bueno": bueno,
                "excelente": excelente,
            },
        )


# visual para grafica de evolución de peso
@login_required
def visual_Evolucion_Peso2(request):
    if request.user.username == "admin":
        logout(request)
        return redirect("home")
    else:
        diccionarios_Medidas_Ciclo_actual = obtenerMedidasGraficos(request)
        bueno = imagenes_calificacion.objects.filter(clasificacion="bueno")
        excelente = imagenes_calificacion.objects.filter(
            clasificacion="excelente"
        ).distinct()
        regular = imagenes_calificacion.objects.filter(
            clasificacion="regular"
        ).distinct()

        datos_pesos = diccionarios_Medidas_Ciclo_actual["diccionario_pesos_CA"]
        return render(
            request,
            "peso.html",
            {
                "ultimo_ciclo_alimento": datos_pesos["ultimo_ciclo_alimento"],
                "ultima_semana_ciclo_alimento": datos_pesos[
                    "ultima_semana_ciclo_alimento"
                ],
                "semanas_posibles": datos_pesos["semanas_posibles"],
                "machos_peso_inicial": datos_pesos["machos_peso_inicial"],
                "hembras_peso_inicial": datos_pesos["hembras_peso_inicial"],
                "mixto_peso_inicial": datos_pesos["mixto_peso_inicial"],
                "machos_peso_final": datos_pesos["machos_peso_final"],
                "hembras_peso_final": datos_pesos["hembras_peso_final"],
                "mixto_peso_final": datos_pesos["mixto_peso_final"],
                "machos_peso_semanas": datos_pesos["machos_peso_semanas"],
                "hembras_peso_semanas": datos_pesos["hembras_peso_semanas"],
                "mixto_peso_semanas": datos_pesos["mixto_peso_semanas"],
                "objetivo_conversion_alimento_mixto": datos_pesos[
                    "objetivo_conversion_alimento_mixto"
                ],
                "objetivo_peso_final_mixto": datos_pesos["objetivo_peso_final_mixto"],
                "objetivo_peso_actual_mixto": datos_pesos["objetivo_peso_actual_mixto"],
                "objetivo_conversion_alimento_machos": datos_pesos[
                    "objetivo_conversion_alimento_machos"
                ],
                "objetivo_peso_final_machos": datos_pesos["objetivo_peso_final_machos"],
                "objetivo_peso_actual_machos": datos_pesos[
                    "objetivo_peso_actual_machos"
                ],
                "objetivo_conversion_alimento_hembras": datos_pesos[
                    "objetivo_conversion_alimento_hembras"
                ],
                "objetivo_peso_final_hembras": datos_pesos[
                    "objetivo_peso_final_hembras"
                ],
                "objetivo_peso_actual_hembras": datos_pesos[
                    "objetivo_peso_actual_hembras"
                ],
                "objetivo_peso_mixto": datos_pesos["objetivo_peso_mixto"],
                "objetivo_peso_machos": datos_pesos["objetivo_peso_machos"],
                "objetivo_peso_hembras": datos_pesos["objetivo_peso_hembras"],
                "machos_CA_semanas": datos_pesos["machos_CA_semanas"],
                "hembras_CA_semanas": datos_pesos["hembras_CA_semanas"],
                "mixto_CA_semanas": datos_pesos["mixto_CA_semanas"],
                "machos_CA_final": datos_pesos["machos_CA_final"],
                "hembras_CA_final": datos_pesos["hembras_CA_final"],
                "mixto_CA_final": datos_pesos["mixto_CA_final"],
                "regular": regular,
                "bueno": bueno,
                "excelente": excelente,
                "raza_ultimo_ciclo": datos_pesos["raza_ultimo_ciclo"],
                "dias_ultimo_ciclo": datos_pesos["dias_ultimo_ciclo"],
            },
        )

# visual para grafica de ganancia de peso
@login_required
def visual_Ganancia_Peso2(request):
    if request.user.username == "admin":
        logout(request)
        return redirect("home")
    else:
        diccionarios_Medidas_Ciclo_actual = obtenerMedidasGraficos(request)
        bueno = imagenes_calificacion.objects.filter(clasificacion="bueno")
        excelente = imagenes_calificacion.objects.filter(
            clasificacion="excelente"
        ).distinct()
        regular = imagenes_calificacion.objects.filter(
            clasificacion="regular"
        ).distinct()
        

        datos_pesos = diccionarios_Medidas_Ciclo_actual["diccionario_pesos_CA"]
        ganancia_total_mixto = datos_pesos["mixto_peso_final"] -datos_pesos["mixto_peso_inicial"]
        ganancia_total_machos =  datos_pesos["machos_peso_final"] - datos_pesos["machos_peso_inicial"]
        ganancia_total_hembras = datos_pesos["hembras_peso_final"] - datos_pesos["hembras_peso_inicial"]
        meta_machos = datos_pesos["objetivo_peso_actual_machos"] - datos_pesos["machos_peso_inicial"]
        meta_hembras = datos_pesos["objetivo_peso_actual_hembras"] - datos_pesos["hembras_peso_inicial"]
        meta_mixto = datos_pesos["objetivo_peso_actual_mixto"] -datos_pesos["mixto_peso_inicial"]
        return render(
            request,
            "ganancia.html",
            {
                "ultimo_ciclo_alimento": datos_pesos["ultimo_ciclo_alimento"],
                "ultima_semana_ciclo_alimento": datos_pesos[
                    "ultima_semana_ciclo_alimento"
                ],
                "semanas_posibles": datos_pesos["semanas_posibles"],
                "machos_peso_inicial": datos_pesos["machos_peso_inicial"],
                "hembras_peso_inicial": datos_pesos["hembras_peso_inicial"],
                "mixto_peso_inicial": datos_pesos["mixto_peso_inicial"],
                "machos_peso_final": datos_pesos["machos_peso_final"],
                "hembras_peso_final": datos_pesos["hembras_peso_final"],
                "mixto_peso_final": datos_pesos["mixto_peso_final"],
                "machos_peso_semanas": datos_pesos["machos_peso_semanas"],
                "hembras_peso_semanas": datos_pesos["hembras_peso_semanas"],
                "mixto_peso_semanas": datos_pesos["mixto_peso_semanas"],
                "objetivo_conversion_alimento_mixto": datos_pesos[
                    "objetivo_conversion_alimento_mixto"
                ],
                "objetivo_peso_final_mixto": datos_pesos["objetivo_peso_final_mixto"],
                "objetivo_peso_actual_mixto": datos_pesos["objetivo_peso_actual_mixto"],
                "objetivo_conversion_alimento_machos": datos_pesos[
                    "objetivo_conversion_alimento_machos"
                ],
                "objetivo_peso_final_machos": datos_pesos["objetivo_peso_final_machos"],
                "objetivo_peso_actual_machos": datos_pesos[
                    "objetivo_peso_actual_machos"
                ],
                "objetivo_conversion_alimento_hembras": datos_pesos[
                    "objetivo_conversion_alimento_hembras"
                ],
                "objetivo_peso_final_hembras": datos_pesos[
                    "objetivo_peso_final_hembras"
                ],
                "objetivo_peso_actual_hembras": datos_pesos[
                    "objetivo_peso_actual_hembras"
                ],
                "objetivo_peso_mixto": datos_pesos["objetivo_peso_mixto"],
                "objetivo_peso_machos": datos_pesos["objetivo_peso_machos"],
                "objetivo_peso_hembras": datos_pesos["objetivo_peso_hembras"],
                "machos_CA_semanas": datos_pesos["machos_CA_semanas"],
                "hembras_CA_semanas": datos_pesos["hembras_CA_semanas"],
                "mixto_CA_semanas": datos_pesos["mixto_CA_semanas"],
                "machos_CA_final": datos_pesos["machos_CA_final"],
                "hembras_CA_final": datos_pesos["hembras_CA_final"],
                "mixto_CA_final": datos_pesos["mixto_CA_final"],
                'ganancia_machos': datos_pesos['ganancia_machos'],
                'ganancia_hembras': datos_pesos['ganancia_hembras'],
                'ganancia_mixto': datos_pesos['ganancia_mixto'],
                'objetivo_ganancia_machos' : datos_pesos['objetivo_ganancia_machos'],
                'objetivo_ganancia_hembras': datos_pesos['objetivo_ganancia_hembras'], 
                'objetivo_ganancia_mixto': datos_pesos['objetivo_ganancia_mixto'],
                "regular": regular,
                "bueno": bueno,
                "excelente": excelente,
                "raza_ultimo_ciclo": datos_pesos["raza_ultimo_ciclo"],
                "dias_ultimo_ciclo": datos_pesos["dias_ultimo_ciclo"],
                "objetivo_ganancia_actual_machos": datos_pesos['objetivo_ganancia_actual_machos'],
                'objetivo_ganancia_final_machos' : datos_pesos['objetivo_ganancia_final_machos'],
                "objetivo_ganancia_actual_hembras": datos_pesos['objetivo_ganancia_actual_hembras'],
                'objetivo_ganancia_final_hembras' : datos_pesos['objetivo_ganancia_final_hembras'],
                "objetivo_ganancia_actual_mixto": datos_pesos['objetivo_ganancia_actual_mixto'],
                'objetivo_ganancia_final_mixto': datos_pesos['objetivo_ganancia_final_mixto'],
                'ganancia_final_machos': datos_pesos['ganancia_final_machos'],
                'ganancia_final_hembras' : datos_pesos['ganancia_final_hembras'],
                'ganancia_final_mixto': datos_pesos['ganancia_final_mixto'],
                'ganancia_total_mixto' : ganancia_total_mixto,
                'ganancia_total_machos' :  ganancia_total_machos,
                'ganancia_total_hembras': ganancia_total_hembras,
                'meta_machos' : meta_machos,
                'meta_hembras' : meta_hembras,
                'meta_mixto': meta_mixto,
            },
        )


# visual para grafica de conversión alimenticia
@login_required
def visual_Conversion_Alimenticia2(request):
    if request.user.username == "admin":
        logout(request)
        return redirect("home")
    else:
        diccionarios_Medidas_Ciclo_actual = obtenerMedidasGraficos(request)
        bueno = imagenes_calificacion.objects.filter(clasificacion="bueno")
        excelente = imagenes_calificacion.objects.filter(
            clasificacion="excelente"
        ).distinct()
        regular = imagenes_calificacion.objects.filter(
            clasificacion="regular"
        ).distinct()

        datos_pesos = diccionarios_Medidas_Ciclo_actual["diccionario_pesos_CA"]
        return render(
            request,
            "conversion.html",
            {
                "ultimo_ciclo_alimento": datos_pesos["ultimo_ciclo_alimento"],
                "ultima_semana_ciclo_alimento": datos_pesos[
                    "ultima_semana_ciclo_alimento"
                ],
                "semanas_posibles": datos_pesos["semanas_posibles"],
                "machos_peso_inicial": datos_pesos["machos_peso_inicial"],
                "hembras_peso_inicial": datos_pesos["hembras_peso_inicial"],
                "mixto_peso_inicial": datos_pesos["mixto_peso_inicial"],
                "machos_peso_final": datos_pesos["machos_peso_final"],
                "hembras_peso_final": datos_pesos["hembras_peso_final"],
                "mixto_peso_final": datos_pesos["mixto_peso_final"],
                "machos_peso_semanas": datos_pesos["machos_peso_semanas"],
                "hembras_peso_semanas": datos_pesos["hembras_peso_semanas"],
                "mixto_peso_semanas": datos_pesos["mixto_peso_semanas"],
                "objetivo_conversion_alimento_mixto": datos_pesos[
                    "objetivo_conversion_alimento_mixto"
                ],
                "objetivo_peso_final_mixto": datos_pesos["objetivo_peso_final_mixto"],
                "objetivo_peso_actual_mixto": datos_pesos["objetivo_peso_actual_mixto"],
                "objetivo_conversion_alimento_machos": datos_pesos[
                    "objetivo_conversion_alimento_machos"
                ],
                "objetivo_peso_final_machos": datos_pesos["objetivo_peso_final_machos"],
                "objetivo_peso_actual_machos": datos_pesos[
                    "objetivo_peso_actual_machos"
                ],
                "objetivo_conversion_alimento_hembras": datos_pesos[
                    "objetivo_conversion_alimento_hembras"
                ],
                "objetivo_peso_final_hembras": datos_pesos[
                    "objetivo_peso_final_hembras"
                ],
                "objetivo_peso_actual_hembras": datos_pesos[
                    "objetivo_peso_actual_hembras"
                ],
                "objetivo_peso_mixto": datos_pesos["objetivo_peso_mixto"],
                "objetivo_peso_machos": datos_pesos["objetivo_peso_machos"],
                "objetivo_peso_hembras": datos_pesos["objetivo_peso_hembras"],
                "machos_CA_semanas": datos_pesos["machos_CA_semanas"],
                "hembras_CA_semanas": datos_pesos["hembras_CA_semanas"],
                "mixto_CA_semanas": datos_pesos["mixto_CA_semanas"],
                "machos_CA_final": datos_pesos["machos_CA_final"],
                "hembras_CA_final": datos_pesos["hembras_CA_final"],
                "mixto_CA_final": datos_pesos["mixto_CA_final"],
                "objetivo_conversion_actual_machos": datos_pesos[
                    "objetivo_conversion_actual_machos"
                ],
                "objetivo_conversion_actual_hembras": datos_pesos[
                    "objetivo_conversion_actual_hembras"
                ],
                "objetivo_conversion_actual_mixto": datos_pesos[
                    "objetivo_conversion_actual_mixto"
                ],
                "objetivo_conversion_final_machos": datos_pesos[
                    "objetivo_conversion_final_machos"
                ],
                "objetivo_conversion_final_hembras": datos_pesos[
                    "objetivo_conversion_final_hembras"
                ],
                "objetivo_conversion_final_mixto": datos_pesos[
                    "objetivo_conversion_final_mixto"
                ],
                "regular": regular,
                "bueno": bueno,
                "excelente": excelente,
                "raza_ultimo_ciclo": datos_pesos["raza_ultimo_ciclo"],
                "dias_ultimo_ciclo": datos_pesos["dias_ultimo_ciclo"],
            },
        )


@login_required
def visual_Resumen(request):
    if request.user.username == "admin":
        logout(request)
        return redirect("home")
    else:
        diccionarios_Medidas_Ciclo_actual = obtenerMedidasGraficos(request)

        datos_mortalidad = diccionarios_Medidas_Ciclo_actual["diccionario_mortalidad"]
        datos_pesos = diccionarios_Medidas_Ciclo_actual["diccionario_pesos_CA"]
        datos_IP = diccionarios_Medidas_Ciclo_actual["diccionario_ciclos_IP"]
        bueno = imagenes_calificacion.objects.filter(clasificacion="bueno")
        excelente = imagenes_calificacion.objects.filter(
            clasificacion="excelente"
        ).distinct()
        regular = imagenes_calificacion.objects.filter(
            clasificacion="regular"
        ).distinct()
        objetivo_IP_bueno = datos_IP["datos_metas_ip"][1]
        objetivo_IP_regular = datos_IP["datos_metas_ip"][2]
        try:
            hembras_porcentaje_actual = round(
                100 * datos_mortalidad["hembras_acumulados_porcentaje"][-1], 2
            )
            machos_porcentaje_actual = round(
                100 * datos_mortalidad["machos_acumulados_porcentaje"][-1], 2
            )
            mixto_porcentaje_actual = round(
                100 * datos_mortalidad["mixto_acumulados_porcentaje"][-1], 2
            )
        except:
            hembras_porcentaje_actual = 0
            machos_porcentaje_actual = 0
            mixto_porcentaje_actual = 0
        ganancia_total_mixto = datos_pesos["mixto_peso_final"] -datos_pesos["mixto_peso_inicial"]
        ganancia_total_machos =  datos_pesos["machos_peso_final"] - datos_pesos["machos_peso_inicial"]
        ganancia_total_hembras = datos_pesos["hembras_peso_final"] - datos_pesos["hembras_peso_inicial"]
        meta_machos = datos_pesos["objetivo_peso_actual_machos"] - datos_pesos["machos_peso_inicial"]
        meta_hembras = datos_pesos["objetivo_peso_actual_hembras"] - datos_pesos["hembras_peso_inicial"]
        meta_mixto = datos_pesos["objetivo_peso_actual_mixto"] -datos_pesos["mixto_peso_inicial"]

        return render(
            request,
            "resumen.html",
            {
                "user": request.user,
                "machos_acumulados_porcentaje": datos_mortalidad[
                    "machos_acumulados_porcentaje"
                ],
                "hembras_acumulados_porcentaje": datos_mortalidad[
                    "hembras_acumulados_porcentaje"
                ],
                "semanas_posibles": datos_mortalidad["semanas_posibles"],
                "mixto_acumulados_porcentaje": datos_mortalidad[
                    "mixto_acumulados_porcentaje"
                ],
                "machos_aves_inicial": datos_mortalidad["machos_aves_inicial"],
                "hembras_aves_inicial": datos_mortalidad["hembras_aves_inicial"],
                "mixto_aves_inicial": datos_mortalidad["mixto_aves_inicial"],
                "objetivo_mortalidad": datos_mortalidad["objetivo_mortalidad"],
                "objetivo_aves_semana_mixto": datos_mortalidad[
                    "objetivo_aves_semana_mixto"
                ],
                "objetivo_aves_semana_machos": datos_mortalidad[
                    "objetivo_aves_semana_machos"
                ],
                "objetivo_aves_semana_hembras": datos_mortalidad[
                    "objetivo_aves_semana_hembras"
                ],
                "objetivo_aves_final_mixto": datos_mortalidad[
                    "objetivo_aves_final_mixto"
                ],
                "objetivo_aves_final_machos": datos_mortalidad[
                    "objetivo_aves_final_machos"
                ],
                "objetivo_aves_final_hembras": datos_mortalidad[
                    "objetivo_aves_final_hembras"
                ],
                "objetivo_aves_actual_mixto": datos_mortalidad[
                    "objetivo_aves_actual_mixto"
                ],
                "objetivo_aves_actual_machos": datos_mortalidad[
                    "objetivo_aves_actual_machos"
                ],
                "objetivo_aves_actual_hembras": datos_mortalidad[
                    "objetivo_aves_actual_hembras"
                ],
                "mixto_aves_final": datos_mortalidad["mixto_aves_final"],
                "machos_aves_final": datos_mortalidad["machos_aves_final"],
                "hembras_aves_final": datos_mortalidad["hembras_aves_final"],
                "machos_porcentaje_actual": machos_porcentaje_actual,
                "hembras_porcentaje_actual": hembras_porcentaje_actual,
                "mixto_porcentaje_actual": mixto_porcentaje_actual,
                "ultimo_ciclo_mortalidad": datos_mortalidad["ultimo_ciclo_mortalidad"],
                "ultima_semana_ciclo_mortalidad": datos_mortalidad[
                    "ultima_semana_ciclo_mortalidad"
                ],
                "ultimo_ciclo_alimento": datos_pesos["ultimo_ciclo_alimento"],
                "ultima_semana_ciclo_alimento": datos_pesos[
                    "ultima_semana_ciclo_alimento"
                ],
                "machos_peso_inicial": datos_pesos["machos_peso_inicial"],
                "hembras_peso_inicial": datos_pesos["hembras_peso_inicial"],
                "mixto_peso_inicial": datos_pesos["mixto_peso_inicial"],
                "machos_peso_final": datos_pesos["machos_peso_final"],
                "hembras_peso_final": datos_pesos["hembras_peso_final"],
                "mixto_peso_final": datos_pesos["mixto_peso_final"],
                "machos_peso_semanas": datos_pesos["machos_peso_semanas"],
                "hembras_peso_semanas": datos_pesos["hembras_peso_semanas"],
                "mixto_peso_semanas": datos_pesos["mixto_peso_semanas"],
                "objetivo_conversion_alimento_mixto": datos_pesos[
                    "objetivo_conversion_alimento_mixto"
                ],
                "objetivo_peso_final_mixto": datos_pesos["objetivo_peso_final_mixto"],
                "objetivo_peso_actual_mixto": datos_pesos["objetivo_peso_actual_mixto"],
                "objetivo_conversion_alimento_machos": datos_pesos[
                    "objetivo_conversion_alimento_machos"
                ],
                "objetivo_peso_final_machos": datos_pesos["objetivo_peso_final_machos"],
                "objetivo_peso_actual_machos": datos_pesos[
                    "objetivo_peso_actual_machos"
                ],
                "objetivo_conversion_alimento_hembras": datos_pesos[
                    "objetivo_conversion_alimento_hembras"
                ],
                "objetivo_peso_final_hembras": datos_pesos[
                    "objetivo_peso_final_hembras"
                ],
                "objetivo_peso_actual_hembras": datos_pesos[
                    "objetivo_peso_actual_hembras"
                ],
                "objetivo_peso_mixto": datos_pesos["objetivo_peso_mixto"],
                "objetivo_peso_machos": datos_pesos["objetivo_peso_machos"],
                "objetivo_peso_hembras": datos_pesos["objetivo_peso_hembras"],
                "machos_CA_semanas": datos_pesos["machos_CA_semanas"],
                "hembras_CA_semanas": datos_pesos["hembras_CA_semanas"],
                "mixto_CA_semanas": datos_pesos["mixto_CA_semanas"],
                "machos_CA_final": datos_pesos["machos_CA_final"],
                "hembras_CA_final": datos_pesos["hembras_CA_final"],
                "mixto_CA_final": datos_pesos["mixto_CA_final"],
                "objetivo_conversion_actual_machos": datos_pesos[
                    "objetivo_conversion_actual_machos"
                ],
                "objetivo_conversion_actual_hembras": datos_pesos[
                    "objetivo_conversion_actual_hembras"
                ],
                "objetivo_conversion_actual_mixto": datos_pesos[
                    "objetivo_conversion_actual_mixto"
                ],
                "objetivo_conversion_final_machos": datos_pesos[
                    "objetivo_conversion_final_machos"
                ],
                "objetivo_conversion_final_hembras": datos_pesos[
                    "objetivo_conversion_final_hembras"
                ],
                "objetivo_conversion_final_mixto": datos_pesos[
                    "objetivo_conversion_final_mixto"
                ],
                "ultimo_ciclo_ciclos_produccion": datos_IP[
                    "ultimo_ciclo_ciclos_produccion"
                ],
                "ultimo_ip_usuario_machos": datos_IP["ultimo_ip_usuario_machos"],
                "ultimo_ip_usuario_hembras": datos_IP["ultimo_ip_usuario_hembras"],
                "ultimo_ip_usuario_mixto": datos_IP["ultimo_ip_usuario_mixto"],
                "regular": regular,
                "bueno": bueno,
                "excelente": excelente,
                'objetivo_IP_bueno': objetivo_IP_bueno,
                'objetivo_IP_regular' : objetivo_IP_regular,
                'objetivo_ganancia_machos' : datos_pesos['objetivo_ganancia_machos'],
                'objetivo_ganancia_hembras': datos_pesos['objetivo_ganancia_hembras'], 
                'objetivo_ganancia_mixto': datos_pesos['objetivo_ganancia_mixto'],
                "objetivo_ganancia_actual_machos": datos_pesos['objetivo_ganancia_actual_machos'],
                'objetivo_ganancia_final_machos' : datos_pesos['objetivo_ganancia_final_machos'],
                "objetivo_ganancia_actual_hembras": datos_pesos['objetivo_ganancia_actual_hembras'],
                'objetivo_ganancia_final_hembras' : datos_pesos['objetivo_ganancia_final_hembras'],
                "objetivo_ganancia_actual_mixto": datos_pesos['objetivo_ganancia_actual_mixto'],
                'objetivo_ganancia_final_mixto': datos_pesos['objetivo_ganancia_final_mixto'],
                'ganancia_final_machos': datos_pesos['ganancia_final_machos'],
                'ganancia_final_hembras' : datos_pesos['ganancia_final_hembras'],
                'ganancia_final_mixto': datos_pesos['ganancia_final_mixto'],
                'ganancia_total_mixto' : ganancia_total_mixto,
                'ganancia_total_machos' :  ganancia_total_machos,
                'ganancia_total_hembras': ganancia_total_hembras,
                'meta_machos' : meta_machos,
                'meta_hembras' : meta_hembras,
                'meta_mixto': meta_mixto,
            },
        )


@login_required
def visual_Indice_productividad2(request):
    if request.user.username == "admin":
        logout(request)
        return redirect("home")
    else:
        diccionarios_Medidas_Ciclo_actual = obtenerMedidasGraficos(request)
        datos_IP = diccionarios_Medidas_Ciclo_actual["diccionario_ciclos_IP"]
        bueno = imagenes_calificacion.objects.filter(clasificacion="bueno")
        excelente = imagenes_calificacion.objects.filter(
            clasificacion="excelente"
        ).distinct()
        regular = imagenes_calificacion.objects.filter(
            clasificacion="regular"
        ).distinct()
        objetivo_IP_bueno = datos_IP["datos_metas_ip"][1]
        objetivo_IP_regular = datos_IP["datos_metas_ip"][2]

        return render(
            request,
            "indiceproductividad.html",
            {
                "ciclos_posibles": datos_IP["ciclos_posibles"],
                "ciclos_posibles_hembras": datos_IP["ciclos_posibles_hembras"],
                "ip_ciclos_posibles_machos": datos_IP["ip_ciclos_posibles_machos"],
                "ip_ciclos_posibles_hembras": datos_IP["ip_ciclos_posibles_hembras"],
                "ip_ciclos_posibles_mixto": datos_IP["ip_ciclos_posibles_mixto"],
                "productores_machos": datos_IP["productores_machos"],
                "ip_productores_machos": datos_IP["ip_productores_machos"],
                "productores_hembras": datos_IP["productores_hembras"],
                "ip_productores_hembras": datos_IP["ip_productores_hembras"],
                "productores_mixto": datos_IP["productores_mixto"],
                "ip_productores_mixtos": datos_IP["ip_productores_mixtos"],
                "ultimo_ciclo_ciclos_produccion": datos_IP[
                    "ultimo_ciclo_ciclos_produccion"
                ],
                "ultimo_ip_usuario_machos": datos_IP["ultimo_ip_usuario_machos"],
                "ultimo_ip_usuario_hembras": datos_IP["ultimo_ip_usuario_hembras"],
                "ultimo_ip_usuario_mixto": datos_IP["ultimo_ip_usuario_mixto"],
                "regular": regular,
                "bueno": bueno,
                "excelente": excelente,
                "safcm": datos_IP["safcm"],
                "productor": datos_IP["productor"],
                'objetivo_IP_bueno': objetivo_IP_bueno,
                'objetivo_IP_regular' : objetivo_IP_regular,
            },
        )


@login_required
def obtenerMedidasGraficos(request):
    alimento_filto = Alimento.objects.filter(user=request.user).order_by("-ciclo")
    mortalidad_filtro = Mortalidad.objects.filter(user=request.user).order_by("-ciclo")
    ciclos_filtro_usuario = Cicloproduccion.objects.filter(user=request.user).order_by(
        "-ciclo"
    )
    productor = str(ciclos_filtro_usuario.order_by("-ciclo").first().productor)
    raza_ultimo_ciclo = ciclos_filtro_usuario.order_by("-ciclo").first().raza
    dias_ultimo_ciclo = ciclos_filtro_usuario.order_by("-ciclo").first().dias_ciclo
    ultimo_ciclo_alimento = int(alimento_filto.order_by("-ciclo").first().ciclo)
    ultimo_ciclo_mortalidad = int(mortalidad_filtro.order_by("-ciclo").first().ciclo)
    ultimo_ciclo_ciclos_produccion = int(
        ciclos_filtro_usuario.order_by("-ciclo").first().ciclo
    )
    alimento_filto = alimento_filto.filter(ciclo=ultimo_ciclo_alimento)
    # mortalidad_filtro = mortalidad_filtro.filter(ciclo = ultimo_ciclo_mortalidad)
    try:
        datos_metas_ip = [
            metasIP.objects.first().meta_IP_excelente,
            metasIP.objects.first().meta_IP_bueno,
            metasIP.objects.first().meta_IP_regular,
        ]
    except:
        datos_metas_ip = [115, 100, 85]

    ultima_semana_ciclo_alimento = int(
        alimento_filto.order_by("-semana").first().semana
    )
    ultima_semana_ciclo_mortalidad = int(
        mortalidad_filtro.filter(ciclo=ultimo_ciclo_mortalidad)
        .order_by("-semana")
        .first()
        .semana
    )

    # definicion de objetivos
    semanas_posibles = list(range(1, 7))
    # objetivo_conversion_alimento_mixto =[0.891, 1.029,1.182,1.322,1.441,1.555,1.686]
    objetivo_conversion_alimento_mixto = [0.772, 0.995, 1.13, 1.257, 1.3855, 1.516]

    # objetivo_peso_mixto =[202,570,1116,1783,2521,3278,4001]
    objetivo_peso_mixto = [213.5, 540.5, 1032.5, 1657, 2360, 3086]

    # objetivo_conversion_alimento_machos =[0.883,1.018,1.166,1.301,1.417,1.518,1.653]
    # objetivo_peso_machos =[205,603,1188,1904,2694,3503,4275]
    # objetivo_conversion_alimento_hembras =[0.884,1.041,1.200,1.346,1.469,1.527,1.724]
    # objetivo_peso_hembras =[199,537,1043,1662,2348,3052,3728]

    objetivo_conversion_alimento_machos = [0.752, 0.991, 1.129, 1.253, 1.377, 1.502]
    objetivo_peso_machos = [213, 549, 1067, 1739, 2509, 3316]
    objetivo_conversion_alimento_hembras = [0.792, 0.999, 1.131, 1.261, 1.394, 1.53]
    objetivo_peso_hembras = [214, 532, 998, 1575, 2211, 2856]
    objetivo_mortalidad = [0.0070, 0.014, 0.0210, 0.0280, 0.0350, 0.0420, 0.0490]
    objetivo_supervivencia = [1 - obj for obj in objetivo_mortalidad]

    objetivo_ganancia_machos = [24, 36, 49, 61, 70, 78, 83]
    objetivo_ganancia_hembras = [24, 35, 45, 55, 62, 67, 70]
    objetivo_ganancia_mixto = [24, 35, 47, 58, 66, 72, 76]

    objetivo_dias_ganancia_machos =[72,73,74,75,76,77,78,79,80,80,81,82,82,83]
    objetivo_dias_ganancia_hembras =[63,64,64,65,66,66,67,68,68,68,69,69,70,70]
    objetivo_dias_ganancia_mixto =[67,68,69,70,71,72,72,73,74,74,75,76,76,76]

    objetivo_dias_ca_machos = [
        1.395,
        1.413,
        1.43,
        1.448,
        1.466,
        1.484,
        1.502,
        1.52,
        1.538,
        1.555,
        1.573,
        1.591,
        1.609,
        1.627,
    ]
    objetivo_dias_peso_machos = [
        2623,
        2738,
        2853,
        2969,
        3085,
        3200,
        3316,
        3431,
        3546,
        3660,
        3773,
        3886,
        3998,
        4109,
    ]

    objetivo_dias_ca_hembras = [
        1.413,
        1.433,
        1.452,
        1.472,
        1.491,
        1.511,
        1.53,
        1.549,
        1.569,
        1.588,
        1.608,
        1.627,
        1.647,
        1.666,
    ]
    objetivo_dias_peso_hembras = [
        2303,
        2396,
        2489,
        2581,
        2673,
        2765,
        2856,
        2946,
        3036,
        3125,
        3214,
        3301,
        3387,
        3473,
    ]

    objetivo_dias_ca_mixto = [
        1.404,
        1.423,
        1.441,
        1.46,
        1.479,
        1.497,
        1.516,
        1.535,
        1.553,
        1.572,
        1.591,
        1.609,
        1.628,
        1.646,
    ]

    objetivo_dias_peso_mixto = [
        2463,
        2567,
        2671,
        2775,
        2879,
        2982,
        3086,
        3189,
        3291,
        3393,
        3493,
        3594,
        3693,
        3791,
    ]
    if dias_ultimo_ciclo > 35 and dias_ultimo_ciclo < 49:
        objetivo_conversion_alimento_machos[5] = objetivo_dias_ca_machos[
            dias_ultimo_ciclo - 36
        ]
        objetivo_peso_machos[5] = objetivo_dias_peso_machos[dias_ultimo_ciclo - 36]
        objetivo_conversion_alimento_hembras[5] = objetivo_dias_ca_hembras[
            dias_ultimo_ciclo - 36
        ]
        objetivo_peso_hembras[5] = objetivo_dias_peso_hembras[dias_ultimo_ciclo - 36]
        objetivo_conversion_alimento_mixto[5] = objetivo_dias_ca_mixto[
            dias_ultimo_ciclo - 36
        ]
        objetivo_peso_mixto[5] = objetivo_dias_peso_mixto[dias_ultimo_ciclo - 36]
        objetivo_ganancia_machos[5] = objetivo_dias_ganancia_machos[dias_ultimo_ciclo - 36]
        objetivo_ganancia_hembras[5] = objetivo_dias_ganancia_hembras[dias_ultimo_ciclo - 36]
        objetivo_ganancia_mixto[5] = objetivo_dias_ganancia_mixto[dias_ultimo_ciclo - 36]

    objetivo_conversion_alimento_machos_Cobb = [
        0.883,
        1.018,
        1.166,
        1.301,
        1.417,
        1.528,
    ]
    objetivo_conversion_alimento_hembras_Cobb = [0.884, 1.041, 1.2, 1.346, 1.469, 1.587]
    objetivo_conversion_alimento_mixto_Cobb = [0.891, 1.029, 1.182, 1.322, 1.441, 1.555]
    objetivo_peso_machos_Cobb = [205, 603, 1188, 1904, 2694, 3503]
    objetivo_peso_hembras_Cobb = [199, 537, 1043, 1662, 2348, 3052]
    objetivo_peso_mixto_Cobb = [202, 570, 1116, 1783, 2521, 3278]
    objetivo_ganancia_machos_Cobb = [23,40,55,67,76,82]
    objetivo_ganancia_hembras_Cobb = [23,35,48,58,66,72]
    objetivo_ganancia_mixto_Cobb = [23,38,51,62,71,77]

    objetivo_dias_ganancia_machos_Cobb =[77,78,79,80,81,82,82,83,84,84,85,86,86,86]
    objetivo_dias_ganancia_hembras_Cobb =[67,68,69,70,70,71,72,72,73,74,74,74,75,75]
    objetivo_dias_ganancia_mixto_Cobb =[72,73,74,75,76,76,77,78,78,79,80,80,80,81]

    objetivo_dias_ca_machos_Cobb = [
        1.433,
        1.449,
        1.464,
        1.48,
        1.496,
        1.512,
        1.528,
        1.544,
        1.561,
        1.579,
        1.597,
        1.615,
        1.633,
        1.653,
    ]
    objetivo_dias_peso_machos_Cobb = [
        2810,
        2926,
        3042,
        3158,
        3274,
        3389,
        3503,
        3617,
        3730,
        3842,
        3952,
        4062,
        4169,
        4275,
    ]

    objetivo_dias_ca_hembras_Cobb = [
        1.486,
        1.502,
        1.519,
        1.535,
        1.552,
        1.57,
        1.587,
        1.605,
        1.623,
        1.642,
        1.662,
        1.682,
        1.703,
        1.724,
    ]
    objetivo_dias_peso_hembras_Cobb = [
        2448,
        2549,
        2650,
        2751,
        2852,
        2952,
        3052,
        3151,
        3250,
        3348,
        3445,
        3540,
        3635,
        3728,
    ]

    objetivo_dias_ca_mixto_Cobb = [
        1.457,
        1.474,
        1.49,
        1.506,
        1.522,
        1.539,
        1.555,
        1.573,
        1.59,
        1.608,
        1.627,
        1.646,
        1.666,
        1.686,
    ]
    objetivo_dias_peso_mixto_Cobb = [
        2629,
        2738,
        2846,
        2954,
        3062,
        3170,
        3278,
        3384,
        3490,
        3595,
        3699,
        3801,
        3902,
        4001,
    ]

    if raza_ultimo_ciclo == "COBB":
        objetivo_conversion_alimento_machos = objetivo_conversion_alimento_machos_Cobb
        objetivo_peso_machos = objetivo_peso_machos_Cobb
        objetivo_conversion_alimento_hembras = objetivo_conversion_alimento_hembras_Cobb
        objetivo_peso_hembras = objetivo_peso_hembras_Cobb
        objetivo_conversion_alimento_mixto = objetivo_conversion_alimento_mixto_Cobb
        objetivo_peso_mixto = objetivo_peso_mixto_Cobb
        objetivo_ganancia_machos = objetivo_ganancia_machos_Cobb
        objetivo_ganancia_hembras = objetivo_ganancia_hembras_Cobb
        objetivo_ganancia_mixto = objetivo_ganancia_mixto_Cobb
        if dias_ultimo_ciclo > 35 and dias_ultimo_ciclo < 49:
            objetivo_conversion_alimento_machos[5] = objetivo_dias_ca_machos_Cobb[
                dias_ultimo_ciclo - 36
            ]
            objetivo_peso_machos[5] = objetivo_dias_peso_machos_Cobb[
                dias_ultimo_ciclo - 36
            ]
            objetivo_conversion_alimento_hembras[5] = objetivo_dias_ca_hembras_Cobb[
                dias_ultimo_ciclo - 36
            ]
            objetivo_peso_hembras[5] = objetivo_dias_peso_hembras_Cobb[
                dias_ultimo_ciclo - 36
            ]
            objetivo_conversion_alimento_mixto[5] = objetivo_dias_ca_mixto_Cobb[
                dias_ultimo_ciclo - 36
            ]
            objetivo_peso_mixto[5] = objetivo_dias_peso_mixto_Cobb[
                dias_ultimo_ciclo - 36
            ]
            objetivo_ganancia_machos[5] = objetivo_dias_ganancia_machos_Cobb[dias_ultimo_ciclo - 36]
            objetivo_ganancia_hembras[5] = objetivo_dias_ganancia_hembras_Cobb[dias_ultimo_ciclo - 36]
            objetivo_ganancia_mixto[5] = objetivo_dias_ganancia_mixto_Cobb[dias_ultimo_ciclo - 36]


    # Informacion relevante diccionario mortalidad: aves iniciales, actuales y finales, objetivos, mortalidades acumuladas
    machos_aves_inicial = int(
        ciclos_filtro_usuario.filter(ciclo=ultimo_ciclo_mortalidad, sexo="Macho")
        .first()
        .aves_iniciales
    )
    try:
        hembras_aves_inicial = int(
            ciclos_filtro_usuario.filter(ciclo=ultimo_ciclo_mortalidad, sexo="Hembra")
            .first()
            .aves_iniciales
        )
    except:
        hembras_aves_inicial = 0
    mixto_aves_inicial = machos_aves_inicial + hembras_aves_inicial

    machos_aves_final = int(
        mortalidad_filtro.filter(sexo="Macho", ciclo=ultimo_ciclo_mortalidad)
        .order_by("-semana")
        .first()
        .saldo_aves
    )
    try:
        hembras_aves_final = int(
            mortalidad_filtro.filter(sexo="Hembra", ciclo=ultimo_ciclo_mortalidad)
            .order_by("-semana")
            .first()
            .saldo_aves
        )
    except:
        hembras_aves_final = 0
    mixto_aves_final = machos_aves_final + hembras_aves_final
    objetivo_aves_semana_mixto = [
        i * mixto_aves_inicial for i in objetivo_supervivencia
    ]
    objetivo_aves_semana_machos = [
        i * machos_aves_inicial for i in objetivo_supervivencia
    ]
    objetivo_aves_semana_hembras = [
        i * hembras_aves_inicial for i in objetivo_supervivencia
    ]

    machos_acumulados_porcentaje = list(
        mortalidad_filtro.filter(sexo="Macho", ciclo=ultimo_ciclo_mortalidad)
        .order_by("semana")
        .values_list("acumulada_porcentaje", flat=True)
    )
    try:
        hembras_acumulados_porcentaje = list(
            mortalidad_filtro.filter(sexo="Hembra", ciclo=ultimo_ciclo_mortalidad)
            .order_by("semana")
            .values_list("acumulada_porcentaje", flat=True)
        )
    except:
        hembras_acumulados_porcentaje = []
    mixto_acumulados_porcentaje = []

    # if len(machos_acumulados_porcentaje) <7:
    #     for i in range(1, 8 -len(machos_acumulados_porcentaje)):
    #         machos_acumulados_porcentaje.append(None)

    # if len(hembras_acumulados_porcentaje) <7:
    #     for i in range(1, 8 -len(machos_acumulados_porcentaje)):
    #         machos_acumulados_porcentaje.append(None)

    for row in mortalidad_filtro.filter(
        sexo="Macho", ciclo=ultimo_ciclo_mortalidad
    ).order_by("semana"):
        for row2 in mortalidad_filtro.filter(
            sexo="Hembra", ciclo=ultimo_ciclo_mortalidad
        ).order_by("semana"):
            if row2.semana == row.semana:
                m = round(
                    (mixto_aves_inicial - row.saldo_aves - row2.saldo_aves)
                    / mixto_aves_inicial,
                    5,
                )
                mixto_acumulados_porcentaje.append(round(m, 4))

    # if len(mixto_acumulados_porcentaje) <7:
    #    for i in range(1, 8 -len(mixto_acumulados_porcentaje)):
    #        mixto_acumulados_porcentaje.append(None)

    # Información relevante diccionario peso y conversion: pesos, CA iniciales finales y por semana
    machos_peso_semanas = list(
        alimento_filto.filter(sexo="Macho")
        .order_by("semana")
        .values_list("peso_ave", flat=True)
    )
    hembras_peso_semanas = list(
        alimento_filto.filter(sexo="Hembra")
        .order_by("semana")
        .values_list("peso_ave", flat=True)
    )
    mixto_peso_semanas = []
    for row in alimento_filto.filter(sexo="Macho").order_by("semana"):
        for row2 in alimento_filto.filter(sexo="Hembra").order_by("semana"):
            if row.semana == row2.semana:
                if (
                    mortalidad_filtro.filter(
                        semana=row.semana, sexo="Macho", ciclo=ultimo_ciclo_alimento
                    ).first()
                    != None
                ) & (
                    mortalidad_filtro.filter(
                        semana=row2.semana, sexo="Hembra", ciclo=ultimo_ciclo_alimento
                    ).first()
                    != None
                ):
                    s1 = (
                        row.peso_ave
                        * mortalidad_filtro.filter(
                            semana=row.semana, sexo="Macho", ciclo=ultimo_ciclo_alimento
                        )
                        .first()
                        .saldo_aves
                    )
                    s2 = (
                        row2.peso_ave
                        * mortalidad_filtro.filter(
                            semana=row2.semana,
                            sexo="Hembra",
                            ciclo=ultimo_ciclo_alimento,
                        )
                        .first()
                        .saldo_aves
                    )
                    s3 = (
                        mortalidad_filtro.filter(
                            semana=row.semana, sexo="Macho", ciclo=ultimo_ciclo_alimento
                        )
                        .first()
                        .saldo_aves
                    )
                    s4 = (
                        mortalidad_filtro.filter(
                            semana=row2.semana,
                            sexo="Hembra",
                            ciclo=ultimo_ciclo_alimento,
                        )
                        .first()
                        .saldo_aves
                    )
                    mps = round(((s1 + s2) / (s3 + s4)), 0)
                    mixto_peso_semanas.append(mps)

    machos_peso_final = int(machos_peso_semanas[-1])
    try:
        hembras_peso_final = int(hembras_peso_semanas[-1])
    except:
        hembras_peso_final = 0
    if len(mixto_peso_semanas) > 0:
        mixto_peso_final = int(mixto_peso_semanas[-1])
    else:
        mixto_peso_final = 0

    # completar informacion de 7 semanas
    # if len(machos_peso_semanas) <7:
    #         for i in range(1, 8 -len(machos_peso_semanas)):
    #             machos_peso_semanas.append(None)

    # if len(hembras_peso_semanas) <7:
    #         for i in range(1, 8 -len(hembras_peso_semanas)):
    #             hembras_peso_semanas.append(None)

    # if len(mixto_peso_semanas) <7:
    #         for i in range(1, 8 -len(mixto_peso_semanas)):
    #             mixto_peso_semanas.append(None)

    machos_peso_inicial = int(
        ciclos_filtro_usuario.filter(ciclo=ultimo_ciclo_alimento, sexo="Macho")
        .first()
        .peso_inicial_gramos
    )
    try:
        hembras_peso_inicial = int(
            ciclos_filtro_usuario.filter(ciclo=ultimo_ciclo_alimento, sexo="Hembra")
            .first()
            .peso_inicial_gramos
        )
    except:
        hembras_peso_inicial = 0
    mixto_peso_inicial = (
        (machos_peso_inicial * machos_aves_inicial)
        + (hembras_peso_inicial * hembras_aves_inicial)
    ) / mixto_aves_inicial

    machos_CA_semanas = list(
        alimento_filto.filter(sexo="Macho")
        .order_by("semana")
        .values_list("c_a_acum", flat=True)
    )
    hembras_CA_semanas = list(
        alimento_filto.filter(sexo="Hembra")
        .order_by("semana")
        .values_list("c_a_acum", flat=True)
    )
    mixto_CA_semanas = []
    for row in alimento_filto.filter(sexo="Macho").order_by("semana"):
        for row2 in alimento_filto.filter(sexo="Macho").order_by("semana"):
            if row.semana == row2.semana:
                if (
                    mortalidad_filtro.filter(
                        semana=row.semana, sexo="Macho", ciclo=ultimo_ciclo_alimento
                    ).first()
                    != None
                ) & (
                    mortalidad_filtro.filter(
                        semana=row2.semana, sexo="Hembra", ciclo=ultimo_ciclo_alimento
                    ).first()
                    != None
                ):
                    # a = (((row.peso_ave*mortalidad_filtro.filter(semana = row.semana, sexo = 'Macho', ciclo = ultimo_ciclo_alimento).first().saldo_aves)+(row2.peso_ave*mortalidad_filtro.filter(semana = row2.semana, sexo = 'Hembra', ciclo = ultimo_ciclo_alimento).first().saldo_aves))/((mortalidad_filtro.filter(semana = row.semana, sexo = 'Macho', ciclo = ultimo_ciclo_alimento).first().saldo_aves)+(mortalidad_filtro.filter(semana = row2.semana, sexo = 'Hembra', ciclo = ultimo_ciclo_alimento).first().saldo_aves)))
                    b = (
                        row.peso_ave
                        * mortalidad_filtro.filter(
                            semana=row.semana, sexo="Macho", ciclo=ultimo_ciclo_alimento
                        )
                        .first()
                        .saldo_aves
                    ) + (
                        row2.peso_ave
                        * mortalidad_filtro.filter(
                            semana=row2.semana,
                            sexo="Hembra",
                            ciclo=ultimo_ciclo_alimento,
                        )
                        .first()
                        .saldo_aves
                    )
                    try:
                        mixto_CA_semanas.append(
                            (
                                (
                                    row.consumo_ave
                                    * mortalidad_filtro.filter(
                                        semana=row.semana,
                                        sexo="Macho",
                                        ciclo=ultimo_ciclo_alimento,
                                    )
                                    .first()
                                    .saldo_aves
                                )
                                + (
                                    row2.consumo_ave
                                    * mortalidad_filtro.filter(
                                        semana=row2.semana,
                                        sexo="Hembra",
                                        ciclo=ultimo_ciclo_alimento,
                                    )
                                    .first()
                                    .saldo_aves
                                )
                            )
                            / b
                        )
                    except:
                        mixto_CA_semanas.append(0)

    machos_CA_final = round(machos_CA_semanas[-1], 2)
    try:
        hembras_CA_final = round(hembras_CA_semanas[-1], 2)
    except:
        hembras_CA_final = 0
    if len(mixto_peso_semanas) > 0:
        mixto_CA_final = round(mixto_CA_semanas[-1], 2)
    else:
        mixto_CA_final = 0

    # completar informacion de 7 semanas
    # if len(machos_CA_semanas) <7:
    #         for i in range(1, 8 -len(machos_CA_semanas)):
    #             machos_CA_semanas.append(None)

    # if len(hembras_CA_semanas) <7:
    #         for i in range(1, 8 -len(hembras_CA_semanas)):
    #             hembras_CA_semanas.append(None)

    # if len(mixto_CA_semanas) <7:
    #         for i in range(1, 8 -len(mixto_CA_semanas)):
    #             mixto_CA_semanas.append(None)

    ciclos_posibles = []
    ip_ciclos_posibles_machos = []

    ip_ciclos_posibles_hembras = []

    ip_ciclos_posibles_mixtos = []

    ciclos_filtro_usuario_machos = ciclos_filtro_usuario.filter(sexo="Macho")

    ciclos_posibles = ciclos_filtro_usuario_machos.order_by("-ciclo").values_list(
        "ciclo", flat=True
    )
    ip_ciclos_posibles_machos = ciclos_filtro_usuario_machos.order_by(
        "-ciclo"
    ).values_list("indice_productividad", flat=True)

    ciclos_filtro_usuario_hembras = ciclos_filtro_usuario.filter(sexo="Hembra")

    ciclos_posibles2 = ciclos_filtro_usuario_hembras.order_by("-ciclo").values_list(
        "ciclo", flat=True
    )
    ip_ciclos_posibles_hembras = ciclos_filtro_usuario_hembras.order_by(
        "-ciclo"
    ).values_list("indice_productividad", flat=True)

    consumo_final_ciclos_mixto = []
    ca_final_ciclos_mixto = []
    safcm = []
    for i in range(0, (len(ciclos_posibles))):
        # ip_ciclos_posibles_machos.append(ciclos_filtro_usuario_machos.filter(ciclo = ciclos_posibles[i]).first().indice_productividad)
        # ip_ciclos_posibles_hembras.append(ciclos_filtro_usuario_hembras.filter(ciclo = ciclos_posibles[i]).values_list('indice_productividad', flat = True))
        try:  # if ciclos_filtro_usuario_machos.filter(ciclo = i).values_list('aves_finales', flat=True)[0] !=None and ciclos_filtro_usuario_hembras.filter(ciclo = i).values_list('aves_finales', flat=True)[0] !=None:
            saldo_aves_final_ciclos_mixto = (
                ciclos_filtro_usuario_machos.filter(
                    ciclo=ciclos_posibles[i]
                ).values_list("aves_finales", flat=True)[0]
            ) + (
                ciclos_filtro_usuario_hembras.filter(
                    ciclo=ciclos_posibles[i]
                ).values_list("aves_finales", flat=True)[0]
            )
            peso = (
                ciclos_filtro_usuario_machos.filter(
                    ciclo=ciclos_posibles[i]
                ).values_list("peso_final_gramos", flat=True)[0]
                * ciclos_filtro_usuario_machos.filter(
                    ciclo=ciclos_posibles[i]
                ).values_list("aves_finales", flat=True)[0]
            ) + (
                ciclos_filtro_usuario_hembras.filter(
                    ciclo=ciclos_posibles[i]
                ).values_list("peso_final_gramos", flat=True)[0]
                * ciclos_filtro_usuario_hembras.filter(
                    ciclo=ciclos_posibles[i]
                ).values_list("aves_finales", flat=True)[0]
            )
            peso_final_ciclos_mixto = peso / saldo_aves_final_ciclos_mixto
            consumo_final_ciclos_mixto = (
                (
                    ciclos_filtro_usuario_machos.filter(
                        ciclo=ciclos_posibles[i]
                    ).values_list("consumo_total_ave_kilogramos", flat=True)[0]
                    * ciclos_filtro_usuario_machos.filter(
                        ciclo=ciclos_posibles[i]
                    ).values_list("aves_finales", flat=True)[0]
                )
                + (
                    ciclos_filtro_usuario_hembras.filter(
                        ciclo=ciclos_posibles[i]
                    ).values_list("consumo_total_ave_kilogramos", flat=True)[0]
                    * ciclos_filtro_usuario_hembras.filter(
                        ciclo=ciclos_posibles[i]
                    ).values_list("aves_finales", flat=True)[0]
                )
            ) / (saldo_aves_final_ciclos_mixto)
            ca_final_ciclos_mixto = consumo_final_ciclos_mixto / peso_final_ciclos_mixto
            ip_ciclos_posibles_mixtos.append(
                (
                    ((peso_final_ciclos_mixto) / (ca_final_ciclos_mixto))
                    / ca_final_ciclos_mixto
                )
                / 10
            )
            safcm.append(round(ip_ciclos_posibles_mixtos[-1], 2))
            # safcm.append((ciclos_filtro_usuario_machos.filter(ciclo = ciclos_posibles[i]).values_list('aves_finales', flat=True)[0]))
            # safcm.append((ciclos_filtro_usuario_hembras.filter(ciclo = ciclos_posibles[i]).values_list('aves_finales', flat=True)[0]))
        except:
            saldo_aves_final_ciclos_mixto = (
                ciclos_filtro_usuario_machos.filter(
                    ciclo=ciclos_posibles[i]
                ).values_list("aves_finales", flat=True)[0]
            ) + (0)
            peso = (
                ciclos_filtro_usuario_machos.filter(
                    ciclo=ciclos_posibles[i]
                ).values_list("peso_final_gramos", flat=True)[0]
                * ciclos_filtro_usuario_machos.filter(
                    ciclo=ciclos_posibles[i]
                ).values_list("aves_finales", flat=True)[0]
            ) + (0 * 0)
            peso_final_ciclos_mixto = peso / saldo_aves_final_ciclos_mixto
            consumo_final_ciclos_mixto = (
                (
                    ciclos_filtro_usuario_machos.filter(
                        ciclo=ciclos_posibles[i]
                    ).values_list("consumo_total_ave_kilogramos", flat=True)[0]
                    * ciclos_filtro_usuario_machos.filter(
                        ciclo=ciclos_posibles[i]
                    ).values_list("aves_finales", flat=True)[0]
                )
                + (0 * 0)
            ) / (saldo_aves_final_ciclos_mixto)
            ca_final_ciclos_mixto = consumo_final_ciclos_mixto / peso_final_ciclos_mixto
            ip_ciclos_posibles_mixtos.append(
                (
                    ((peso_final_ciclos_mixto) / (ca_final_ciclos_mixto))
                    / ca_final_ciclos_mixto
                )
                / 10
            )
            safcm.append(round(ip_ciclos_posibles_mixtos[-1], 2))

        # else:
        #    peso = 1

    if len(ciclos_posibles) > 6:
        for i in range(0, len(ciclos_posibles)):
            del ciclos_posibles[6 + i]
            del ip_ciclos_posibles_machos[6 + i]

    # for i in range(0,7):
    #     if len(list(ciclos_filtro_usuario.order_by('-ciclo').values_list('ciclo', flat = True))) >i:
    #         ciclos_posibles.append(ciclos_filtro_usuario.order_by('-ciclo')[i].ciclo)
    #         ip_ciclos_posibles_machos.append(round(ciclos_filtro_usuario.order_by('-ciclo')[i].indice_productividad,2))
    bodega = Cicloproduccion.objects.filter(
        sexo="Macho", ciclo=ultimo_ciclo_ciclos_produccion,user=request.user
    ).order_by("-indice_productividad").first().bodega
    ciclos_productores_filtro_ultimo_ciclo = Cicloproduccion.objects.filter(
        sexo="Macho", ciclo=ultimo_ciclo_ciclos_produccion, bodega =bodega
    ).order_by("-indice_productividad")
    productores_machos = list(
        ciclos_productores_filtro_ultimo_ciclo.values_list("productor", flat=True)
    )
    ip_productores_machos = list(
        ciclos_productores_filtro_ultimo_ciclo.values_list(
            "indice_productividad", flat=True
        )
    )
    ciclos_productores_filtro_ultimo_ciclo_hembras = Cicloproduccion.objects.filter(
        sexo="Hembra", ciclo=ultimo_ciclo_ciclos_produccion,bodega =bodega
    ).order_by("-indice_productividad")
    productores_hembras = list(
        ciclos_productores_filtro_ultimo_ciclo_hembras.values_list(
            "productor", flat=True
        )
    )
    ip_productores_hembras = list(
        ciclos_productores_filtro_ultimo_ciclo_hembras.values_list(
            "indice_productividad", flat=True
        )
    )
    ip_productores_mixtos = []

    objetos_filtro_ultimo_ciclo = Cicloproduccion.objects.filter(
        ciclo=ultimo_ciclo_ciclos_produccion, bodega = bodega
    )
    productores_mixto = list(
        objetos_filtro_ultimo_ciclo.values_list("productor", flat=True).distinct()
    )

    for i in range(0, (len(productores_mixto))):
        try:
            saldo_aves_final_productor = (
                objetos_filtro_ultimo_ciclo.filter(
                    sexo="Macho", productor=productores_mixto[i]
                )
                .first()
                .aves_finales
                + objetos_filtro_ultimo_ciclo.filter(
                    sexo="Hembra", productor=productores_mixto[i]
                )
                .first()
                .aves_finales
            )
            peso_machos = (
                objetos_filtro_ultimo_ciclo.filter(
                    sexo="Macho", productor=productores_mixto[i]
                )
                .first()
                .peso_final_gramos
                * objetos_filtro_ultimo_ciclo.filter(
                    sexo="Macho", productor=productores_mixto[i]
                )
                .first()
                .aves_finales
            )
            peso_hembras = (
                objetos_filtro_ultimo_ciclo.filter(
                    sexo="Hembra", productor=productores_mixto[i]
                )
                .first()
                .peso_final_gramos
                * objetos_filtro_ultimo_ciclo.filter(
                    sexo="Hembra", productor=productores_mixto[i]
                )
                .first()
                .aves_finales
            )
            peso_final = (peso_machos + peso_hembras) / saldo_aves_final_productor
            consumo_machos = (
                objetos_filtro_ultimo_ciclo.filter(
                    sexo="Macho", productor=productores_mixto[i]
                )
                .first()
                .consumo_total_ave_kilogramos
                * objetos_filtro_ultimo_ciclo.filter(
                    sexo="Macho", productor=productores_mixto[i]
                )
                .first()
                .aves_finales
            )
            consumo_hembras = (
                objetos_filtro_ultimo_ciclo.filter(
                    sexo="Hembra", productor=productores_mixto[i]
                )
                .first()
                .consumo_total_ave_kilogramos
                * objetos_filtro_ultimo_ciclo.filter(
                    sexo="Hembra", productor=productores_mixto[i]
                )
                .first()
                .aves_finales
            )
            consumo_final = (
                consumo_machos + consumo_hembras
            ) / saldo_aves_final_productor
            ca_final = consumo_final / peso_final
            ip_productores_mixtos.append(((peso_final / ca_final) / ca_final) / 10)
        except:
            saldo_aves_final_productor = (
                objetos_filtro_ultimo_ciclo.filter(
                    sexo="Macho", productor=productores_mixto[i]
                )
                .first()
                .aves_finales
            )
            peso_machos = (
                objetos_filtro_ultimo_ciclo.filter(
                    sexo="Macho", productor=productores_mixto[i]
                )
                .first()
                .peso_final_gramos
                * objetos_filtro_ultimo_ciclo.filter(
                    sexo="Macho", productor=productores_mixto[i]
                )
                .first()
                .aves_finales
            )
            peso_final = (peso_machos) / saldo_aves_final_productor
            consumo_machos = (
                objetos_filtro_ultimo_ciclo.filter(
                    sexo="Macho", productor=productores_mixto[i]
                )
                .first()
                .consumo_total_ave_kilogramos
                * objetos_filtro_ultimo_ciclo.filter(
                    sexo="Macho", productor=productores_mixto[i]
                )
                .first()
                .aves_finales
            )
            consumo_final = (consumo_machos) / saldo_aves_final_productor
            ca_final = consumo_final / peso_final
            ip_productores_mixtos.append(((peso_final / ca_final) / ca_final) / 10)

    original = ip_productores_mixtos.copy()
    ip_productores_mixtos.sort(reverse=True)
    productores_mixto_sorted = []
    a = len(ip_productores_mixtos)

    for i in range(0, a):
        for j in range(0, (len(original))):
            if original[j] == ip_productores_mixtos[i]:
                productores_mixto_sorted.append(productores_mixto[j])
                del productores_mixto[j]
                del original[j]
                break
            else:
                continue

    productores_mixto = productores_mixto_sorted

    # for i in range(0, (len(productores_machos))):
    #     #ip_ciclos_posibles_machos.append(ciclos_filtro_usuario_machos.filter(ciclo = ciclos_posibles[i]).first().indice_productividad)
    #     #ip_ciclos_posibles_hembras.append(ciclos_filtro_usuario_hembras.filter(ciclo = ciclos_posibles[i]).values_list('indice_productividad', flat = True))
    #     try:#if ciclos_filtro_usuario_machos.filter(ciclo = i).values_list('aves_finales', flat=True)[0] !=None and ciclos_filtro_usuario_hembras.filter(ciclo = i).values_list('aves_finales', flat=True)[0] !=None:
    #         saldo_aves_final_ciclos_mixto = (Cicloproduccion.objects.filter(sexo = 'Macho', ciclo = ultimo_ciclo_ciclos_produccion).order_by('-indice_productividad').filter(productor = productores_machos[i]).values_list('aves_finales', flat=True)[0])+(Cicloproduccion.objects.filter(sexo = 'Hembra', ciclo = ultimo_ciclo_ciclos_produccion).order_by('-indice_productividad').filter(productor = productores_machos[i]).values_list('aves_finales', flat=True)[0])
    #         peso = ((Cicloproduccion.objects.filter(sexo = 'Macho', ciclo = ultimo_ciclo_ciclos_produccion).order_by('-indice_productividad').filter(productor = productores_machos[i]).values_list('peso_final_gramos', flat=True)[0] * Cicloproduccion.objects.filter(sexo = 'Macho', ciclo = ultimo_ciclo_ciclos_produccion).order_by('-indice_productividad').filter(productor = productores_machos[i]).values_list('aves_finales', flat=True)[0]) + (Cicloproduccion.objects.filter(sexo = 'Hembra', ciclo = ultimo_ciclo_ciclos_produccion).order_by('-indice_productividad').filter(productor = productores_machos[i]).values_list('peso_final_gramos', flat=True)[0] * Cicloproduccion.objects.filter(sexo = 'hembra', ciclo = ultimo_ciclo_ciclos_produccion).order_by('-indice_productividad').filter(productor = productores_machos[i]).values_list('aves_finales', flat=True)[0]))
    #         peso_final_ciclos_mixto = peso / saldo_aves_final_ciclos_mixto
    #         consumo_final_ciclos_mixto = ((Cicloproduccion.objects.filter(sexo = 'Macho', ciclo = ultimo_ciclo_ciclos_produccion).order_by('-indice_productividad').filter(productor = productores_machos[i]).values_list('consumo_total_ave_kilogramos', flat=True)[0] * Cicloproduccion.objects.filter(sexo = 'Macho', ciclo = ultimo_ciclo_ciclos_produccion).order_by('-indice_productividad').filter(productor = productores_machos[i]).values_list('aves_finales', flat=True)[0]) + (Cicloproduccion.objects.filter(sexo = 'Hembra', ciclo = ultimo_ciclo_ciclos_produccion).order_by('-indice_productividad').filter(productor = productores_machos[i]).values_list('consumo_total_ave_kilogramos', flat=True)[0] * Cicloproduccion.objects.filter(sexo = 'Hembra', ciclo = ultimo_ciclo_ciclos_produccion).order_by('-indice_productividad').filter(productor = productores_machos[i]).values_list('aves_finales', flat=True)[0]) )/ (saldo_aves_final_ciclos_mixto)
    #         ca_final_ciclos_mixto = consumo_final_ciclos_mixto/peso_final_ciclos_mixto
    #         ip_productores_mixtos.append((((peso_final_ciclos_mixto)/(ca_final_ciclos_mixto))/ca_final_ciclos_mixto)/10)
    #         #safcm.append(round(ip_ciclos_posibles_mixtos[-1],2))
    #         #safcm.append((ciclos_filtro_usuario_machos.filter(productor = productores_machos[i]).values_list('aves_finales', flat=True)[0]))
    #         #safcm.append((ciclos_filtro_usuario_hembras.filter(productor = productores_machos[i]).values_list('aves_finales', flat=True)[0]))
    #     except:
    #         saldo_aves_final_ciclos_mixto = (Cicloproduccion.objects.filter(sexo = 'Macho', ciclo = ultimo_ciclo_ciclos_produccion).order_by('-indice_productividad').filter(productor = productores_machos[i]).values_list('aves_finales', flat=True)[0])+(0)
    #         peso = ((Cicloproduccion.objects.filter(sexo = 'Macho', ciclo = ultimo_ciclo_ciclos_produccion).order_by('-indice_productividad').filter(productor = productores_machos[i]).values_list('peso_final_gramos', flat=True)[0] * Cicloproduccion.objects.filter(sexo = 'Macho', ciclo = ultimo_ciclo_ciclos_produccion).order_by('-indice_productividad').filter(productor = productores_machos[i]).values_list('aves_finales', flat=True)[0]) + (0 * 0))
    #         peso_final_ciclos_mixto = peso / saldo_aves_final_ciclos_mixto
    #         consumo_final_ciclos_mixto = ((Cicloproduccion.objects.filter(sexo = 'Macho', ciclo = ultimo_ciclo_ciclos_produccion).order_by('-indice_productividad').filter(productor = productores_machos[i]).values_list('consumo_total_ave_kilogramos', flat=True)[0] * Cicloproduccion.objects.filter(sexo = 'Macho', ciclo = ultimo_ciclo_ciclos_produccion).order_by('-indice_productividad').filter(productor = productores_machos[i]).values_list('aves_finales', flat=True)[0]) + (0 * 0) )/ (saldo_aves_final_ciclos_mixto)
    #         ca_final_ciclos_mixto = consumo_final_ciclos_mixto/peso_final_ciclos_mixto
    #         ip_productores_mixtos.append((((peso_final_ciclos_mixto)/(ca_final_ciclos_mixto))/ca_final_ciclos_mixto)/10)
    #         #safcm.append(round(ip_ciclos_posibles_mixtos[-1],2))

    safcm.reverse()
    ip_ciclos_posibles_mixtos.reverse()

    #para visual de ganancia de pesos
    ganancia_machos= []
    ganancia_hembras = []
    ganancia_mixto = []

    #try:
    ganancia_machos.append(round(((machos_peso_semanas[0]-machos_peso_inicial)/7),2))
    ganancia_hembras.append(round(((hembras_peso_semanas[0]-hembras_peso_inicial)/7),2))
    ganancia_mixto.append(round(((float(mixto_peso_semanas[0])-mixto_peso_inicial)/7),2))
    for i in range(1,(len(machos_peso_semanas))):
        if i!= 5 :
            ganancia_machos.append(round(((machos_peso_semanas[i]-machos_peso_semanas[i-1])/7),2))
        else:
            ganancia_machos.append(round(((machos_peso_semanas[i]-machos_peso_semanas[i-1])/(dias_ultimo_ciclo-35)),2))
    for i in range(1,(len(hembras_peso_semanas))):
        if i!= 5 :
            ganancia_hembras.append(round(((hembras_peso_semanas[i]-hembras_peso_semanas[i-1])/7),2))
        else:
            ganancia_hembras.append(round(((hembras_peso_semanas[i]-hembras_peso_semanas[i-1])/(dias_ultimo_ciclo-35)),2))
    for i in range(1,(len(mixto_peso_semanas))):
        if i!= 5 :
            ganancia_mixto.append(round(((mixto_peso_semanas[i]-mixto_peso_semanas[i-1])/7),2))
        else:
            ganancia_mixto.append(round(((mixto_peso_semanas[i]-mixto_peso_semanas[i-1])/(dias_ultimo_ciclo-35)),2))
    # except:
    #     ganancia_machos= [0,0,0,0,0,0]
    #     ganancia_hembras = [0,0,0,0,0,0]
    #     ganancia_mixto = [0,0,0,0,0,0]


    diccionario_ciclos_IP = {
        "ciclos_posibles": ciclos_posibles.reverse,
        "ciclos_posibles_hembras": ciclos_posibles2.reverse,
        "ip_ciclos_posibles_machos": ip_ciclos_posibles_machos.reverse,
        "ip_ciclos_posibles_hembras": ip_ciclos_posibles_hembras.reverse,
        "ip_ciclos_posibles_mixto": ip_ciclos_posibles_mixtos,
        "productores_machos": productores_machos,
        "ip_productores_machos": ip_productores_machos,
        "productores_hembras": productores_hembras,
        "ip_productores_hembras": ip_productores_hembras,
        "productores_mixto": productores_mixto,
        "ip_productores_mixtos": ip_productores_mixtos,
        "ultimo_ciclo_ciclos_produccion": ultimo_ciclo_ciclos_produccion,
        "ultimo_ip_usuario_machos": round(ip_ciclos_posibles_machos[0], 2),
        "ultimo_ip_usuario_hembras": round(ip_ciclos_posibles_hembras[0], 2),
        "ultimo_ip_usuario_mixto": round(safcm[-1], 2),
        "safcm": safcm,
        "productor": productor,
        "datos_metas_ip": datos_metas_ip,
    }

    diccionario_mortalidad = {
        "ultimo_ciclo_mortalidad": ultimo_ciclo_mortalidad,
        "ultima_semana_ciclo_mortalidad": ultima_semana_ciclo_mortalidad,
        "semanas_posibles": semanas_posibles,
        "machos_acumulados_porcentaje": machos_acumulados_porcentaje,
        "hembras_acumulados_porcentaje": hembras_acumulados_porcentaje,
        "mixto_acumulados_porcentaje": mixto_acumulados_porcentaje,
        "objetivo_mortalidad": objetivo_mortalidad,
        "objetivo_aves_semana_mixto": objetivo_aves_semana_mixto,
        "objetivo_aves_semana_machos": objetivo_aves_semana_machos,
        "objetivo_aves_semana_hembras": objetivo_aves_semana_hembras,
        "objetivo_aves_final_mixto": round(objetivo_aves_semana_mixto[-1]),
        "objetivo_aves_final_machos": round(objetivo_aves_semana_machos[-1]),
        "objetivo_aves_final_hembras": round(objetivo_aves_semana_hembras[-1]),
        "objetivo_aves_actual_mixto": round(
            objetivo_aves_semana_mixto[ultima_semana_ciclo_mortalidad - 1]
        ),
        "objetivo_aves_actual_machos": round(
            objetivo_aves_semana_machos[ultima_semana_ciclo_mortalidad - 1]
        ),
        "objetivo_aves_actual_hembras": round(
            objetivo_aves_semana_hembras[ultima_semana_ciclo_mortalidad - 1]
        ),
        "machos_aves_inicial": machos_aves_inicial,
        "hembras_aves_inicial": hembras_aves_inicial,
        "mixto_aves_inicial": mixto_aves_inicial,
        "machos_aves_final": machos_aves_final,
        "hembras_aves_final": hembras_aves_final,
        "mixto_aves_final": mixto_aves_final,
    }

    diccionario_pesos_CA = {
        "ultimo_ciclo_alimento": ultimo_ciclo_alimento,
        "ultima_semana_ciclo_alimento": ultima_semana_ciclo_alimento,
        "semanas_posibles": semanas_posibles,
        "machos_peso_inicial": machos_peso_inicial,
        "hembras_peso_inicial": hembras_peso_inicial,
        "mixto_peso_inicial": mixto_peso_inicial,
        "machos_peso_final": machos_peso_final,
        "hembras_peso_final": hembras_peso_final,
        "mixto_peso_final": mixto_peso_final,
        "machos_peso_semanas": machos_peso_semanas,
        "hembras_peso_semanas": hembras_peso_semanas,
        "mixto_peso_semanas": mixto_peso_semanas,
        "objetivo_peso_mixto": objetivo_peso_mixto,
        "objetivo_peso_machos": objetivo_peso_machos,
        "objetivo_peso_hembras": objetivo_peso_hembras,
        "objetivo_conversion_alimento_mixto": objetivo_conversion_alimento_mixto,
        "objetivo_peso_final_mixto": objetivo_peso_mixto[-1],
        "objetivo_peso_actual_mixto": objetivo_peso_mixto[
            ultima_semana_ciclo_alimento - 1
        ],
        "objetivo_conversion_actual_mixto": objetivo_conversion_alimento_mixto[
            ultima_semana_ciclo_alimento - 1
        ],
        "objetivo_conversion_final_mixto": objetivo_conversion_alimento_mixto[-1],
        "objetivo_conversion_alimento_machos": objetivo_conversion_alimento_machos,
        "objetivo_peso_final_machos": objetivo_peso_machos[-1],
        "objetivo_peso_actual_machos": objetivo_peso_machos[
            ultima_semana_ciclo_alimento - 1
        ],
        "objetivo_conversion_actual_machos": objetivo_conversion_alimento_machos[
            ultima_semana_ciclo_alimento - 1
        ],
        "objetivo_conversion_final_machos": objetivo_conversion_alimento_machos[-1],
        "objetivo_conversion_alimento_hembras": objetivo_conversion_alimento_hembras,
        "objetivo_peso_final_hembras": objetivo_peso_hembras[-1],
        "objetivo_peso_actual_hembras": objetivo_peso_hembras[
            ultima_semana_ciclo_alimento - 1
        ],
        "objetivo_conversion_actual_hembras": objetivo_conversion_alimento_hembras[
            ultima_semana_ciclo_alimento - 1
        ],
        "objetivo_conversion_final_hembras": objetivo_conversion_alimento_hembras[-1],
        "objetivo_ganancia_actual_machos": objetivo_ganancia_machos[ultima_semana_ciclo_alimento - 1],
        'objetivo_ganancia_final_machos' : objetivo_ganancia_machos[-1],
        "objetivo_ganancia_actual_hembras": objetivo_ganancia_hembras[ultima_semana_ciclo_alimento - 1],
        'objetivo_ganancia_final_hembras' : objetivo_ganancia_hembras[-1],
        "objetivo_ganancia_actual_mixto": objetivo_ganancia_mixto[ultima_semana_ciclo_alimento - 1],
        'objetivo_ganancia_final_mixto' : objetivo_ganancia_mixto[-1],
        'ganancia_final_machos': ganancia_machos[-1],
        'ganancia_final_hembras' : ganancia_hembras[-1],
        'ganancia_final_mixto': ganancia_mixto[-1],
        "machos_CA_semanas": machos_CA_semanas,
        "hembras_CA_semanas": hembras_CA_semanas,
        "mixto_CA_semanas": mixto_CA_semanas,
        "machos_CA_final": machos_CA_final,
        "hembras_CA_final": hembras_CA_final,
        "mixto_CA_final": mixto_CA_final,
        "raza_ultimo_ciclo": raza_ultimo_ciclo,
        "dias_ultimo_ciclo": dias_ultimo_ciclo,
        'ganancia_machos': ganancia_machos,
        'ganancia_hembras': ganancia_hembras,
        'ganancia_mixto': ganancia_mixto,
        'objetivo_ganancia_machos' : objetivo_ganancia_machos,
        'objetivo_ganancia_hembras': objetivo_ganancia_hembras, 
        'objetivo_ganancia_mixto': objetivo_ganancia_mixto,
    }

    return {
        "diccionario_mortalidad": diccionario_mortalidad,
        "diccionario_pesos_CA": diccionario_pesos_CA,
        "diccionario_ciclos_IP": diccionario_ciclos_IP,
    }
