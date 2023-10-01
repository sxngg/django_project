from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.exceptions import ValidationError
from datetime import datetime, timedelta

class Univalluno(models.Model):
    nombres = models.CharField(max_length=255)
    apellidos = models.CharField(max_length=255)
    tipo_univalluno = models.CharField(max_length=50, choices=[('Estudiante', 'Estudiante'), ('Funcionario', 'Funcionario')])
    tipo_documento = models.CharField(max_length=50) 
    numero_documento = models.CharField(max_length=50, unique=True)
    codigo_estudiante = models.CharField(max_length=50, blank=True, null=True)
    correo_electronico = models.EmailField()

    #Muestra el nombre del modelo en el admin
    def __str__(self):
        return self.nombres 

class ArticuloDeportivo(models.Model):
    nombres = models.CharField(max_length=255)
    deporte = models.CharField(max_length=255)
    descrpcion = models.CharField(max_length=255)
    valorArticulo = models.DecimalField(max_digits=10, decimal_places=2)
    disponible = models.BooleanField(default=True)  

    def __str__(self):
        return self.nombres 

class Prestamo(models.Model):
    univalluno = models.ForeignKey('Univalluno', on_delete=models.CASCADE)
    articulo_deportivo = models.ForeignKey('ArticuloDeportivo', on_delete=models.CASCADE)
    fecha_hora_prestamo = models.DateTimeField(auto_now_add=True)
    fecha_hora_vencimiento = models.DateTimeField()

    def save(self, *args, **kwargs):
        # Verificar si el artículo deportivo está disponible
        if not self.articulo_deportivo.disponible:
            raise ValidationError("El artículo deportivo no está disponible para préstamo.")
        
        super().save(*args, **kwargs)  # Llama al método save predeterminado para crear el préstamo
        
        # Marcar el artículo como no disponible
        self.articulo_deportivo.disponible = False
        self.articulo_deportivo.save()

def calcular_multa_diaria(prestamo):
    # Obtén la fecha actual
    fecha_actual = datetime.now()
    
    # Calcula los días de retraso
    dias_de_retraso = (fecha_actual - prestamo.fecha_hora_vencimiento).days
    
    # Calcula la multa diaria (15% del valor del artículo)
    valor_articulo = prestamo.articulo_deportivo.valorArticulo
    multa_diaria = valor_articulo * 0.15
    
    # Multiplica la multa por los días de retraso
    multa_total = multa_diaria * dias_de_retraso
    
    return multa_total

class Multa(models.Model):
    prestamo = models.ForeignKey('Prestamo', on_delete=models.CASCADE)
    fecha_hora_pago = models.DateTimeField(blank=True, null=True)
    pagada = models.BooleanField(default=False)