from django.shortcuts import render,redirect
from django.shortcuts import get_object_or_404
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
def residentes(request):
  residentes = Residente.objects.all()
  return render (request,'residentes.html',{"residentes":residentes})

def add_residente(request):
  actionMessage = "Registrar Residente"
  form = ResidenteForm()
  if request.method == "POST":
    form = ResidenteForm(request.POST)
    if form.is_valid():
      form.save() 
      return redirect(residentes)
  return render(request, 'components/crispyform.html', {"form": form,"title":actionMessage})

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

def delete_residente(request,id):
  reservation = Residente.objects.get(id=id)
  reservation.delete()
  return redirect(residentes)


# Vehiculos Views
def vehiculos(request):
  vehiculos = Vehiculo.objects.all()
  return render (request,'vehiculos.html',{"vehiculos":vehiculos})

def add_vehiculo(request):
  actionMessage = "Registrar Vehiculo"
  form = VehiculoForm()
  if request.method == "POST":
    form = VehiculoForm(request.POST)
    if form.is_valid():
      form.save()
      return redirect(vehiculos)
  return render(request, 'components/crispyform.html', {"form": form,"title":actionMessage})

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
  reservation = Vehiculo.objects.get(id=id)
  reservation.delete()
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

def procesar_imagen(request):
    if request.method == 'POST':
        # Obtén el archivo del formulario
        archivo = request.FILES.get('file', None)

        if archivo is None:
            return JsonResponse({'error': 'No se envió ningún archivo'}, status=400)

        # Lee el archivo en un array de bytes
        img_data = archivo.read()

        # Decodifica la matriz de bytes en una imagen de OpenCV
        nparr = np.frombuffer(img_data, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        # Procesamiento de la imagen (puedes ajustarlo según tus necesidades)
        img_grayscale = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # Aplica OCR para obtener el texto de la patente
        texto_patente = pytesseract.image_to_string(img_grayscale)
        print(texto_patente)
        if not texto_patente.strip():  # strip() elimina espacios en blanco al inicio y al final
          return JsonResponse({'error': 'no se encontro patente'}, status=404)
        # Consulta la base de datos para verificar si la patente existe
        patente_existe = PatenteAutorizada.objects.filter(vehiculo__patente=texto_patente).exists()

        # Devuelve la respuesta JSON
        return JsonResponse({'patente_existe': patente_existe})

    return JsonResponse({'error': 'Método no permitido'}, status=405)

def vista_camara(request):
    # Lógica de la vista de la cámara
    return render(request, 'camara.html')

@login_required
def bienvenido_safestay(request):
    return render(request, 'bienvenido_safestay.html')


def exportar_pdf_vehiculo(request, id):
    # Obtener el objeto Vehiculo con el id proporcionado
    vehiculo = get_object_or_404(Vehiculo, id=id)

    # Crear el contexto con los datos del vehículo
    context = {'vehiculo': vehiculo}

    # Renderizar el template HTML como PDF
    template_path = 'exportar_pdf.html'  # Ruta al template HTML

    # Crear una instancia de HttpResponse con el tipo de contenido PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="vehiculo_{id}.pdf"'

    # Crear el PDF
    template = get_template(template_path)
    html = template.render(context)
    pisa_status = pisa.CreatePDF(html, dest=response)

    # Si el PDF se creó correctamente, devolver la respuesta
    if pisa_status.err:
        return HttpResponse('Error al generar el PDF', content_type='text/plain')
    return response