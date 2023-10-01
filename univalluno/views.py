from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions, generics
from .models import Multa, ArticuloDeportivo, Prestamo # Importa tu modelo Multa y otros modelos necesarios
from datetime import datetime, timedelta
from .serializers import MultaSerializer
from django.shortcuts import render
from django.db.models import Count
from django.utils import timezone  # Importa timezone
from django.http import JsonResponse

class GenerarMultaView(generics.ListAPIView):
    queryset = Multa.objects.all()  # Establece el queryset apropiado
    serializer_class = MultaSerializer

def grafico_prestamos_por_deporte(request):
   # Obtén las fechas de inicio y fin del rango
    fecha_inicio = timezone.make_aware(datetime(2023, 1, 1))  # Convierte a un objeto datetime con zona horaria
    fecha_fin = timezone.make_aware(datetime(2023, 12, 31))    

    # Realiza la consulta para contar los préstamos por deporte
    prestamos_por_deporte = Prestamo.objects.filter(
        fecha_hora_prestamo__range=(fecha_inicio, fecha_fin)
    ).values('articulo_deportivo__deporte').annotate(
        total_prestamos=Count('id')
    )

    # Convierte los resultados en una lista de tuplas (deporte, total_prestamos)
    datos_grafico = [(item['articulo_deportivo__deporte'], item['total_prestamos']) for item in prestamos_por_deporte]
    print(datos_grafico)
    return render(request, 'index.html', {'datos_grafico': datos_grafico})
    #return JsonResponse(datos_grafico, safe=False)