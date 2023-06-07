"""fenaviapp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from home import views as homeViews
from visuales import views as visualesviews
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', homeViews.home, name = 'home'),
    path('conversion/', visualesviews.visual_Conversion_Alimenticia2, name = 'conversion'),
    path('mortalidad/', visualesviews.visual_Mortalidad2, name = 'mortalidad'),
    path('peso/', visualesviews.visual_Evolucion_Peso2, name = 'peso'),
    path('gananciapeso/', visualesviews.visual_Ganancia_Peso2, name = 'ganancia'),
    #path('mortalidad/', visualesviews.Graficos2.as_view(), name = 'mortalidad'),
    #path('indiceproductividad/', visualesviews.indiceproductividad, name = 'indiceproductividad'),
    path('usuarios/', include('home.urls')),
    path('visuales/', include('visuales.urls')),
    path('indiceproductividad/', visualesviews.visual_Indice_productividad2,name='indiceproductividad'),
    path('Resumenciclo', visualesviews.visual_Resumen, name = 'resumen'),
    path('', include('pwa.urls')), 
]

urlpatterns += static(settings.MEDIA_URL,
document_root=settings.MEDIA_ROOT)
