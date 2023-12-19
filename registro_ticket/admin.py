from django.contrib import admin
from .models import Ticket, Trabajador, Atencion

# Register your models here.

admin.site.register(Ticket)
admin.site.register(Trabajador)
admin.site.register(Atencion)