from django.db import models

class Univalluno(models.Model):
    nombres = models.CharField(max_length=255)
    apellidos = models.CharField(max_length=255)
    tipo_univalluno = models.CharField(max_length=50, choices=[('Estudiante', 'Estudiante'), ('Funcionario', 'Funcionario')])
    tipo_documento = models.CharField(max_length=50) 
    numero_documento = models.CharField(max_length=50, unique=True)
    codigo_estudiante = models.CharField(max_length=50, blank=True, null=True)
    correo_electronico = models.EmailField()

class ArticuloDeportivo(models.Model):
    nombres = models.CharField(max_length=255)
    deporte = models.CharField(max_length=255)
    descrpcion = models.CharField(max_length=255)
    valorArticulo = models.DecimalField(max_digits=10, decimal_places=2)

class Prestamo(models.Model):
    univalluno = models.ForeignKey('Univalluno', on_delete=models.CASCADE)
    articulo_deportivo = models.ForeignKey('ArticuloDeportivo', on_delete=models.CASCADE)
    fecha_hora_prestamo = models.DateTimeField(auto_now_add=True)
    fecha_hora_vencimiento = models.DateTimeField()

class Multa(models.Model):
    prestamo = models.ForeignKey('Prestamo', on_delete=models.CASCADE)
    fecha_hora_pago = models.DateTimeField(blank=True, null=True)
    pagada = models.BooleanField(default=False)
