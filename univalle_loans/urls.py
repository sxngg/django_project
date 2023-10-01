
from django.contrib import admin
from django.urls import include, path
from django.contrib.auth.models import User
from rest_framework import routers, serializers, viewsets
from univalluno.views import GenerarMultaView, grafico_prestamos_por_deporte

urlpatterns = [
    path("reporte/", include("univalluno.urls")),
    path('admin/', admin.site.urls),
    path('generar_multa/', GenerarMultaView.as_view(), name='generar_multa'),
    path('', grafico_prestamos_por_deporte)
]
