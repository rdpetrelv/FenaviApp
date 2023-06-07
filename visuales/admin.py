from django.contrib import admin
import tablib
from .models import (
    Cicloproduccion,
    Alimento,
    Mortalidad,
    imagenes_calificacion,
    metasIP,
)

# from .models import Ciclo_produccion_Form, Alimento_Form, Mortalidad_Form
from import_export.admin import ImportExportModelAdmin, ExportMixin
from import_export import resources
from django.contrib.auth.models import User


# Register your models here.

# class CicloproduccionResource(resources.ModelResource):

# class Meta:
#   model = Cicloproduccion


class CicloproduccionAdmin(ImportExportModelAdmin):
    pass


class AlimentoAdmin(ImportExportModelAdmin):
    pass


class MortalidadAdmin(ImportExportModelAdmin):
    pass


class UserResource(resources.ModelResource):
    class Meta:
        model = User
        fields = ("id", "username", "first_name", "last_name", "email")


class UserAdmin(ImportExportModelAdmin):
    list_display = ("id", "username", "first_name", "last_name", "email")
    resource_class = UserResource
    pass


admin.site.register(Cicloproduccion, CicloproduccionAdmin)
# admin.site.register(Ciclo_produccion_Form)
admin.site.register(Alimento, AlimentoAdmin)
# admin.site.register(Alimento_Form)
admin.site.register(Mortalidad, MortalidadAdmin)
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(imagenes_calificacion)
admin.site.register(metasIP)
# admin.site.register(Mortalidad_Form)
