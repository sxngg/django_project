
from django.contrib import admin
from django.urls import include, path
from univalluno.views import GenerarMultaView, grafico_prestamos_por_deporte, grafico_prestamos_por_dia

urlpatterns = [
    path("reporte/", include("univalluno.urls")),
    path('', admin.site.urls),
    path('admin/', admin.site.urls),
    path('generar_multa/', GenerarMultaView.as_view(), name='generar_multa'),
    path('grafico_prestamo_por_deporte', grafico_prestamos_por_deporte),
    path('grafico_prestamo_por_dia', grafico_prestamos_por_dia),
]
