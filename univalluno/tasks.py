2# tasks.py

import time
import schedule
from datetime import datetime, time as dt_time
from django.core.management.base import BaseCommand
from .models import Prestamo, Multa

def generar_multas():
    now = datetime.now().time()
    target_time = dt_time(20, 10)  # 8:10 PM

    if now < target_time:
        return  # No hagas nada si no es aún la hora programada

    # Obtén los préstamos que aún no se han entregado
    prestamos_pendientes = Prestamo.objects.filter(
        fecha_hora_vencimiento__lt=now,
        fecha_hora_entrega__isnull=True
    )

    for prestamo in prestamos_pendientes:
        # Crea una multa para cada préstamo pendiente
        Multa.objects.create(prestamo=prestamo)

def schedule_tarea():
    # Programa la tarea para ejecutarse a las 8:10 PM todos los días
    schedule.every().day.at("20:10").do(generar_multas)

if __name__ == '__main__':
    schedule_tarea()

    while True:
        schedule.run_pending()
        time.sleep(1)
