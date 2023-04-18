from django.contrib import admin
import tablib
from .models import Cicloproduccion, Alimento, Mortalidad, Ciclo_produccion_Form, Alimento_Form, Mortalidad_Form
from import_export.admin import ImportExportModelAdmin
from import_export import resources

# Register your models here.

#class CicloproduccionResource(resources.ModelResource):

    #class Meta:
     #   model = Cicloproduccion 

class CicloproduccionAdmin(ImportExportModelAdmin):
    pass

class AlimentoAdmin(ImportExportModelAdmin):
    pass

class MortalidadAdmin(ImportExportModelAdmin):
    pass    

admin.site.register(Cicloproduccion, CicloproduccionAdmin)
#admin.site.register(Ciclo_produccion_Form)
admin.site.register(Alimento, AlimentoAdmin)
#admin.site.register(Alimento_Form)
admin.site.register(Mortalidad, MortalidadAdmin)
#admin.site.register(Mortalidad_Form)