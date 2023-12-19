from django.db import models
from django.utils import timezone

class Ticket(models.Model):
    id = models.AutoField(primary_key=True)
    nombre_usuario = models.CharField(max_length=100)
    area = models.CharField(max_length=50)
    descripcion = models.CharField(max_length=255)
    fecha = models.DateField(auto_now=True)
    estado = models.CharField(max_length=20)

class Trabajador(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    area = models.CharField(max_length=50)

class Atencion(models.Model):
    id_ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE)
    id_trabajador = models.ForeignKey(Trabajador, on_delete=models.CASCADE)
    solucion = models.CharField(max_length=255)
    estado = models.CharField(max_length=20)
    fecha = models.DateField(auto_now=True)

