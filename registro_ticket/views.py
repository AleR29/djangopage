from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.db.models import Q
from .forms import  BusquedaForm, IngresoForm, ActualizarForm, AtencionFinalizados
from .models import Atencion, Ticket, Trabajador 
from datetime import datetime
from django.shortcuts import get_object_or_404

# Create your views here.

def busquedaAtencionFinalizado(request, ticket_id):
    tick = get_object_or_404(Atencion, id = ticket_id)
    return render(request, 'proceso_finalizado.html', {'ticket': tick})

def busquedaAtencion(request):
    form = BusquedaForm(request.POST or None)
    tickets = None
    pendientes = 0

    if request.method == 'POST':
        form = BusquedaForm(request.POST)
        if form.is_valid():
            #query = form.cleaned_data.get('query')
            fecha_inicial = form.cleaned_data.get('fecha_inicial')
            fecha_final = form.cleaned_data.get('fecha_final')
        
            tickets = Atencion.objects.filter(
                Q(estado__icontains="Por atender") | 
                Q(estado__icontains="En atención"),
                fecha__range=[fecha_inicial, fecha_final]
            )
            pendientes = tickets.count()

        else:
            tickets = Atencion.objects.none()
    else:
        tickets = Atencion.objects.filter(Q(estado__contains="Por atender") | Q(estado__contains="En atención"))
        pendientes = tickets.count()

    return render(request, 'proceso.html', {'form': form, 'tickets': tickets,'pendientes': pendientes}) 

def busquedaBD(request):
    form = BusquedaForm(request.POST or None)
    tickets = None
    atendidos = 0

    if request.method == 'POST':
        form = BusquedaForm(request.POST)
        if form.is_valid():
            #query = form.cleaned_data.get('query')
            fecha_inicial = form.cleaned_data.get('fecha_inicial')
            fecha_final = form.cleaned_data.get('fecha_final')
        
            tickets = Ticket.objects.filter(   
                    fecha__range=[fecha_inicial, fecha_final],
                    estado__icontains="Atendido"
                )
            atendidos = tickets.count()

        else:
            tickets = Ticket.objects.none()
    else:
        tickets = Ticket.objects.filter(estado__contains="Atendido")
        atendidos = tickets.count()

    return render(request, 'solucionados.html', {'form': form, 'tickets': tickets,'atendidos': atendidos}) 

def nuevo_ticket(request):
    if request.method == 'POST':
        form = IngresoForm(request.POST)
        if form.is_valid():
            nuevo_ticket = form.save(commit = False)
            nuevo_ticket.estado = 'Por atender'
            nuevo_ticket.save()
            area1 = form.cleaned_data['area']
            trabajador = Trabajador.objects.filter(area = area1).first()
            
            if trabajador:
                atencion = Atencion.objects.create(
                id_ticket = nuevo_ticket,
                id_trabajador = trabajador,
                solucion = '',
                estado = nuevo_ticket.estado
                )

            atencion.save()

            #tickets = Ticket.objects.all()
            #return render(request, 'agregar_ticket.html', {'form': IngresoForm(), 'tickets': tickets})

            return redirect(request.path)
    else:
        form = IngresoForm()

    #tickets = Ticket.objects.all()
    return render(request, 'agregar_ticket.html', {'form': form})

def actualizar_atencion(request, ticket_id):
    tick = get_object_or_404(Atencion, id = ticket_id)

    if request.method == 'POST':
        form = ActualizarForm(request.POST, instance = tick)
        if form.is_valid():
            atencion = form.save(commit=False)
            atencion.save()
            ticket = Atencion.objects.all()

            ticket_estado = atencion.id_ticket
            ticket_estado.estado = atencion.estado
            ticket_estado.save()
    
    else:
        form = ActualizarForm(instance = tick)
        ticket = Atencion.objects.all()
    
    return render(request, 'actualizar_ticket.html', {'form': form, 'tickets': tick, 'tck': ticket})