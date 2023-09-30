from django.contrib import admin
from django.forms import ModelForm
from django.core.exceptions import ValidationError
from .models import Univalluno
from .models import ArticuloDeportivo
from .models import Prestamo
from .models import Multa


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

class UnivallunoAdmin(admin.ModelAdmin):
    form = UnivallunoForm


admin.site.register(Univalluno, UnivallunoAdmin)
admin.site.register(ArticuloDeportivo)
admin.site.register(Prestamo)
admin.site.register(Multa)

# Register your models here.
