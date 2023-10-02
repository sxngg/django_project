from rest_framework import generics
from .models import Multa, ArticuloDeportivo, Prestamo
from datetime import datetime
from .serializers import MultaSerializer
from django.shortcuts import render
from django.db.models import Count
from django.utils import timezone

class GenerarMultaView(generics.ListAPIView):
    queryset = Multa.objects.all() 
    serializer_class = MultaSerializer

def grafico_prestamos_por_deporte(request):
    fecha_inicio = timezone.make_aware(datetime(2023, 1, 1)) 
    fecha_fin = timezone.make_aware(datetime(2023, 12, 31))    

    prestamos_por_deporte = Prestamo.objects.filter(
        fecha_hora_prestamo__range=(fecha_inicio, fecha_fin)
    ).values('articulo_deportivo__deporte').annotate(
        total_prestamos=Count('id')
    )

    datos_grafico = [{
    'deporte': item['articulo_deportivo__deporte'],
    'total_prestamos': item['total_prestamos']
    } for item in prestamos_por_deporte]

    print(datos_grafico)
    return render(request, 'grafico-prestamo-por-deporte.html', {'datos_grafico': datos_grafico})

def grafico_prestamos_por_dia(request):
    fecha_inicio = timezone.make_aware(datetime(2023, 1, 1))
    fecha_fin = timezone.make_aware(datetime(2023, 12, 31))

    fecha_inicio_str = fecha_inicio.strftime('%Y-%m-%d')
    fecha_fin_str = fecha_fin.strftime('%Y-%m-%d')

    prestamos_por_dia = Prestamo.objects.filter(
        fecha_hora_prestamo__range=(fecha_inicio, fecha_fin)
    ).values('fecha_hora_prestamo__date').annotate(
        total_prestamos=Count('id')
    )

    datos_grafico = [{
        'fecha': item['fecha_hora_prestamo__date'].strftime('%Y-%m-%d'),
        'total_prestamos': item['total_prestamos']
    } for item in prestamos_por_dia]
    print(datos_grafico)
    return render(request, 'grafico-prestamo-por-dia.html', {'fecha_inicio': fecha_inicio_str, 'fecha_fin': fecha_fin_str, 'datos_grafico': datos_grafico})
