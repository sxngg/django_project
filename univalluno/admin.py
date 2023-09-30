from django.contrib import admin
from .models import Univalluno
from .models import ArticuloDeportivo
from .models import Prestamo
from .models import Multa

admin.site.register(Univalluno)
admin.site.register(ArticuloDeportivo)
admin.site.register(Prestamo)
admin.site.register(Multa)

# Register your models here.
