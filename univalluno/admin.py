from django.contrib import admin
from django.forms import ModelForm
from django.utils import timezone
from django.core.exceptions import ValidationError
from .models import Univalluno, ArticuloDeportivo, Prestamo, Multa
from django import forms

# Se construye un formulario personalizdo para validar el modelo Univalluno
class UnivallunoForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        instance = kwargs.get('instance')
        if instance:
            self.fields['tipo_documento'].widget.attrs['readonly'] = True
            self.fields['numero_documento'].widget.attrs['readonly'] = True

    def clean(self):
        cleaned_data = super().clean()
        tipo_univalluno = cleaned_data.get("tipo_univalluno")
        codigo_estudiante = cleaned_data.get("codigo_estudiante")

        if tipo_univalluno == "Funcionario" and codigo_estudiante:
            raise ValidationError("El campo 'Código de estudiante' no debe estar lleno para Funcionarios.")

    class Meta:
        model = Univalluno
        fields = "__all__"
        unique_together = ('tipo_documento', 'numero_documento')

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
        
    def clean(self):
        cleaned_data = super().clean()
        univalluno = cleaned_data.get('univalluno')
        articulo_deportivo = cleaned_data.get('articulo_deportivo')

        # Verificar si el univalluno ya tiene un artículo deportivo en préstamo
        prestamos_existentes = Prestamo.objects.filter(univalluno=univalluno)
        for prestamo_existente in prestamos_existentes:
            if prestamo_existente != self.instance and prestamo_existente.articulo_deportivo == articulo_deportivo:
                raise ValidationError("Este univalluno ya tiene un artículo deportivo en préstamo.")

        return cleaned_data


#Se registran los formularios personalizados para sobreescribir los formularios default de Admin
@admin.register(Univalluno)
class UnivallunoAdmin(admin.ModelAdmin):
    form = UnivallunoForm
    list_display = ['nombres', 'apellidos', 'tipo_univalluno', 'correo_electronico']

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
