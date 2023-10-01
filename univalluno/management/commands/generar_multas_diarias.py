# generar_multas_diarias.py (dentro de la carpeta commands de tu aplicación)

from django.core.management.base import BaseCommand
from tu_app.models import Prestamo, Multa
from tu_app.utils import calcular_multa_diaria

class Command(BaseCommand):
    help = 'Aplica multas diarias por retraso en la entrega'

    def handle(self, *args, **kwargs):
        # Obtén todos los préstamos vencidos sin multa
        prestamos_vencidos = Prestamo.objects.filter(
            fecha_hora_vencimiento__lt=datetime.now(),
            fecha_hora_entrega__isnull=True,
            multa__isnull=True
        )

        for prestamo in prestamos_vencidos:
            # Calcula la multa diaria para el préstamo
            multa_total = calcular_multa_diaria(prestamo)
            
            # Crea un registro de multa asociado al préstamo
            Multa.objects.create(prestamo=prestamo, monto=multa_total)
