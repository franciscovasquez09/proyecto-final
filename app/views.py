from django.shortcuts import render,redirect
from django.shortcuts import get_object_or_404
import requests
from .models import Residente,Vehiculo, Trabajador, TipoTrabajador
from .forms import ResidenteForm, VehiculoForm, RegistroAccesoForm, TrabajadorForm
from django.db.models import ProtectedError
from django.contrib import messages
from django.contrib.auth import logout
from django.http import JsonResponse
from .models import PatenteAutorizada
import pytesseract
from PIL import Image
import cv2
import numpy as np
import base64
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def index(request):
  return render(request,'residentes.html')

# Residentes Views
@login_required
def residentes(request):
  residentes = Residente.objects.all()
  return render (request,'residentes.html',{"residentes":residentes})

@login_required
def add_residente(request):
  actionMessage = "Registrar Residente"
  form = ResidenteForm()
  if request.method == "POST":
    form = ResidenteForm(request.POST)
    if form.is_valid():
      form.save() 
      return redirect(residentes)
  return render(request, 'components/crispyform.html', {"form": form,"title":actionMessage})

@login_required
def update_residente(request, rut):
    actionMessage = "Actualizar Residente"
    residente = get_object_or_404(Residente, rut=rut)
    form = ResidenteForm(instance=residente)
    if request.method == "POST":
        form = ResidenteForm(request.POST, instance=residente)
        if form.is_valid() and form.has_changed():
            form.save()
            return redirect(residentes)
    return render(request, 'components/crispyform.html', {"form": form, "title": actionMessage, "residenteId": id})

@login_required
def delete_residente(request, rut):
    residente = get_object_or_404(Residente, rut=rut)
    residente.delete()
    return redirect(residentes)

def exportar_pdf_residente(request, id=None):
    # Obtener todos los vehículos si no se proporciona un ID
    if id is None:
        residentes = Residente.objects.all()
    else:
        # Obtener el objeto residente con el id proporcionado
        residente = get_object_or_404(Residente, id=id)
        # Crear una lista con un solo vehículo para poder iterar en el template
        residentes = [residente]

    # Crear el contexto con los datos de los vehículos
    context = {'residentes': residentes}

    # Renderizar el template HTML como PDF
    template_path = 'pdf_residentes.html'  # Ruta al template HTML

    # Crear una instancia de HttpResponse con el tipo de contenido PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="residentes.pdf"'

    # Crear el PDF
    template = get_template(template_path)
    html = template.render(context)
    pisa_status = pisa.CreatePDF(html, dest=response)

    # Si el PDF se creó correctamente, devolver la respuesta
    if pisa_status.err:
        return HttpResponse('Error al generar el PDF', content_type='text/plain')
    return response

# Vehiculos Views
@login_required
def vehiculos(request):
  vehiculos = Vehiculo.objects.all()
  return render (request,'vehiculos.html',{"vehiculos":vehiculos})

@login_required
def add_vehiculo(request):
  actionMessage = "Registrar Vehiculo"
  form = VehiculoForm()
  if request.method == "POST":
    form = VehiculoForm(request.POST)
    if form.is_valid():
      form.save()
      return redirect(vehiculos)
  return render(request, 'components/crispyform.html', {"form": form,"title":actionMessage})

@login_required
def update_vehiculo(request,id):
  actionMessage = "Actualizar Vehiculo"
  vehiculo = Vehiculo.objects.get(id=id)
  form = VehiculoForm(instance=vehiculo)
  if request.method == "POST":
    form = VehiculoForm(request.POST,instance=vehiculo)
    if form.is_valid() and form.has_changed():
      form.save()
      return redirect(vehiculos)
  return render(request, 'components/crispyform.html', {"form": form,"title":actionMessage, "vehiculoId":id})

def delete_vehiculo(request,id):
  vehiculo = get_object_or_404(Vehiculo, id=id)
  vehiculo.delete()
  return redirect(vehiculos)

def registro_acceso(request):
    if request.method == 'POST':
        form = RegistroAccesoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('residentes')  # Redirige a la lista de registros de acceso
    else:
        form = RegistroAccesoForm()

    return render(request, 'registro_acceso.html', {'form': form})


def trabajadores(request):
    trabajadores = Trabajador.objects.all()
    return render(request, 'trabajadores.html', {"trabajadores": trabajadores})

def add_trabajador(request):
    action_message = "Registrar Trabajador"
    form = TrabajadorForm()

    if request.method == "POST":
        form = TrabajadorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('trabajadores')

    return render(request, 'components/crispyform.html', {"form": form, "title": action_message})


def update_trabajador(request, trabajador):
    action_message = "Actualizar Trabajador"
    form = TrabajadorForm(instance=trabajador)

    if request.method == "POST":
        form = TrabajadorForm(request.POST, instance=trabajador)
        if form.is_valid() and form.has_changed():
            form.save()
            return redirect('trabajadores')

    return render(request, 'components/crispyform.html', {"form": form, "title": action_message, "trabajadorId": trabajador.id})

def delete_trabajador(request, trabajador):
    trabajador.delete()
    return redirect('trabajadores')


def salir(request):
    logout(request)
    messages.sucess(request, F"sesion cerrada exitosamente")
    # Redirecciona a la página que desees después de cerrar sesión
    return redirect('login_view')

def formatear_patente(patente):
    if len(patente) == 6:
        return f'{patente[:2]}-{patente[2:4]}*{patente[4:6]}'.upper()
    else:
        return patente

def procesar_imagen(request):
    if request.method == 'POST':
        archivo = request.FILES.get('file', None)
        if archivo is None:
            return JsonResponse({'error': 'No se envió ningún archivo'}, status=400)

        # Prepara los datos para enviar a Plate Recognizer
        files = {'upload': archivo}
        headers = {'Authorization': 'Token 3892c6ee8b698357efe7ff9664df6f98b6bb9c22'}

        # Realiza la solicitud a Plate Recognizer
        response = requests.post('https://api.platerecognizer.com/v1/plate-reader/', files=files, headers=headers)

        if response.status_code == 201:
            data = response.json()
            # Procesa los resultados como sea necesario
            # Ejemplo: extraer la primera patente reconocida
            patentes = [result['plate'] for result in data['results']]
            primera_patente = patentes[0] if patentes else None
           
            if primera_patente:
                primera_patente = formatear_patente(primera_patente)
                  # Consulta la base de datos para verificar si la patente existe
                patente_existe = PatenteAutorizada.objects.filter(vehiculo__patente=primera_patente).exists()
                return JsonResponse({'patente': primera_patente, 'patente_existe': patente_existe})  # Modifica según sea necesario
            else:
                return JsonResponse({'error': 'No se encontró patente'}, status=404)
        else:
            return JsonResponse({'error': 'Error en el servicio de Plate Recognizer'}, status=response.status_code)

    return JsonResponse({'error': 'Método no permitido'}, status=405)
    
def validar_formato_patente(texto):
    # Implementa la lógica para validar el formato de la patente
    # Por ejemplo, usar expresiones regulares para verificar el formato
    return texto  # Modifica esto según tu validación

def vista_camara(request):
    # Lógica de la vista de la cámara
    return render(request, 'camara.html')

@login_required
def bienvenido_safestay(request):
    return render(request, 'bienvenido_safestay.html')

def exportar_pdf_vehiculo(request, id=None):
    # Obtener todos los vehículos si no se proporciona un ID
    if id is None:
        vehiculos = Vehiculo.objects.all()
    else:
        # Obtener el objeto Vehiculo con el id proporcionado
        vehiculo = get_object_or_404(Vehiculo, id=id)
        # Crear una lista con un solo vehículo para poder iterar en el template
        vehiculos = [vehiculo]

    # Crear el contexto con los datos de los vehículos
    context = {'vehiculos': vehiculos}

    # Renderizar el template HTML como PDF
    template_path = 'pdf_vehiculos.html'  # Ruta al template HTML

    # Crear una instancia de HttpResponse con el tipo de contenido PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="vehiculos.pdf"'

    # Crear el PDF
    template = get_template(template_path)
    html = template.render(context)
    pisa_status = pisa.CreatePDF(html, dest=response)

    # Si el PDF se creó correctamente, devolver la respuesta
    if pisa_status.err:
        return HttpResponse('Error al generar el PDF', content_type='text/plain')
    return response

def buscar_residente(request):
    # Obtén la consulta desde los parámetros GET
    query = request.GET.get('query', '')

    # Filtra los residentes según la consulta en el campo Rut
    residentes = Residente.objects.filter(rut__startswith=query)

    # Renderiza la vista con los resultados
    return render(request, 'residentes.html', {'residentes': residentes, 'query': query})