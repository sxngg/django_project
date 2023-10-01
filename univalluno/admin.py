from django.contrib import admin
from django.forms import ModelForm
from django.utils import timezone
from django.core.exceptions import ValidationError
from .models import Univalluno
from .models import ArticuloDeportivo
from .models import Prestamo
from .models import Multa

# Se construye un formulario personalizdo para validar el modelo Univalluno
class UnivallunoForm(ModelForm):
    def clean(self):
        print(self.instance)
        print(self.cleaned_data)
        if len(self.cleaned_data.get("apellidos")) <= 4:
            raise ValidationError("Holaaaaaa")
        return super().clean()

    class Meta:
        model = Univalluno
        fields = "__all__"

# Se construye un formulario personalizdo para validar el modelo Prestamo agregando la condición
# de que una vez prestado un articulo no se pueda prestar a otro Univalluno
class PrestamoAdminForm(ModelForm):
    class Meta:
        model = Prestamo
        fields = '__all__'
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Filtrar los artículos deportivos disponibles
        self.fields['articulo_deportivo'].queryset = self.fields['articulo_deportivo'].queryset.filter(disponible=True)

        # Filtrar los Univalluno disponibles que no tienen préstamo activo
        univalluno_queryset = Univalluno.objects.exclude(
            prestamo__fecha_hora_vencimiento__gt=timezone.now()
        ).distinct()
        
        self.fields['univalluno'].queryset = univalluno_queryset


#Se registran los formularios personalizados para sobreescribir los formularios default de Admin
@admin.register(Univalluno)
class UnivallunoAdmin(admin.ModelAdmin):
    form = UnivallunoForm

@admin.register(Prestamo)
class PrestamoAdmin(admin.ModelAdmin):
    form = PrestamoAdminForm

#En este modelo el único cambio en el formulario es que no se muestre el campo de disponible
#Pues nos sirve para un borrado lógico, pero no debemos mostrarlo al usuario
@admin.register(ArticuloDeportivo)
class ArticuloDeportivoAdmin(admin.ModelAdmin):
    exclude = ('disponible',) 

admin.site.register(Multa)

# Register your models here.
