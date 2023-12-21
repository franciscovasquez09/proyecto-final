from django.urls import path
from .views import index,add_residente,update_residente,delete_residente,residentes,exportar_pdf_residente,vehiculos,add_vehiculo,update_vehiculo,delete_vehiculo,registro_acceso, trabajadores, add_trabajador, update_trabajador, delete_trabajador, exportar_pdf_vehiculo, buscar_residente
from .views_login import login_view
from django.contrib.auth import logout
from .views import salir, procesar_imagen, vista_camara, bienvenido_safestay


urlpatterns = [
  path('', login_view, name='login_view'),
  path('residentes', residentes, name='residentes'),
  path('bienvenido_safestay/', bienvenido_safestay, name='bienvenido_safestay'),
  path('salir', salir, name='salir'),
  
  #residente paths
  path('add_residente',add_residente,name='add_residente'),
  path('update_residente/<str:rut>',update_residente,name='update_residente'),
  path('delete_residente/<str:rut>',delete_residente,name='delete_residente'),
  path('exportar_pdf_residente', exportar_pdf_residente, name='exportar_pdf_residente'),
  path('residentes/', buscar_residente, name='residentes'),


  #vehiculo paths
  path('vehiculos',vehiculos,name='vehiculos'),
  path('add_vehiculo',add_vehiculo,name='add_vehiculo'),
  path('update_vehiculo/<int:id>',update_vehiculo,name='update_vehiculo'),
  path('delete_vehiculo/<int:id>',delete_vehiculo,name='delete_vehiculo'),
  path('exportar_pdf_vehiculo', exportar_pdf_vehiculo, name='exportar_pdf_vehiculo'),
  path('buscar_residente/', buscar_residente, name='buscar_residente'),
  

  path('trabajadores', trabajadores, name='trabajadores'),
  path('add_trabajador', add_trabajador, name='add_trabajador'),
  path('update_trabajador/<int:id>', update_trabajador, name='update_trabajador'),
  path('delete_trabajador/<int:id>',delete_trabajador,name='delete_trabajador'),

  path('registro_acceso', registro_acceso, name='registro_acceso'),
  path('procesar_imagen/', procesar_imagen, name='procesar_imagen'),
  path('camara/', vista_camara, name='vista_camara'),
]