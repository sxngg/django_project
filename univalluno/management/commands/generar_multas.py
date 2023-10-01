
# generar_multas.py (dentro de la carpeta commands de tu aplicación)

from django.core.management.base import BaseCommand
from univalluno.tasks import generar_multas

class Command(BaseCommand):
    help = 'Programa la tarea de generación de multas'

    def handle(self, *args, **kwargs):
        generar_multas()
