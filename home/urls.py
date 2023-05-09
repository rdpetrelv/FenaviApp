from django.urls import path
from . import views 
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('crearusuario/', views.crearusuario, name = 'crearusuario'),
    path('desconexion/', views.desconexion, name = 'desconexion'),
]
urlpatterns += static(settings.MEDIA_URL,
document_root=settings.MEDIA_ROOT)