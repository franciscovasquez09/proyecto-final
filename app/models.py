from django.db import models

class Ciudad(models.Model):
  nombre = models.CharField(max_length=100)

  class Meta:
    db_table = "ciudades"

  def __str__(self):
    return self.nombre

class Persona(models.Model):
  rut = models.CharField(max_length=12, primary_key=True)
  nombre = models.CharField(max_length=100)
  apellidos = models.CharField(max_length=100)
  correo = models.CharField(max_length=100)
  telefono = models.CharField(max_length=12)
  direccion = models.CharField(max_length=100)
  ciudad = models.ForeignKey(Ciudad, on_delete=models.CASCADE, null=True)

  class Meta:
    abstract = True

  def __str__(self):
    return self.nombre
  
class TipoTrabajador(models.Model):
  nombre = models.CharField(max_length=100)

  class Meta:
    db_table = "tipo_trabajador"

  def __str__(self):
    return self.nombre

class Trabajador(Persona):
  tipo_trabajador = models.ForeignKey(TipoTrabajador, on_delete=models.CASCADE, null=True) 
  nombre_usuario = models.CharField(max_length=100)
  password = models.CharField(max_length=100)

  class Meta:
    db_table = "trabajadores"

  def __str__(self):
    return self.nombre

class Residente(Persona):
  numero_casa = models.PositiveIntegerField()

  class Meta:
    db_table = "residentes"

  def __str__(self):
    return str(self.nombre + ' - ' + self.rut)
  
class TipoVehiculo(models.Model):
  nombre = models.CharField(max_length=100)

  class Meta:
    db_table = "tipo_vehiculos"

  def __str__(self):
    return self.nombre
  

class ModeloVehiculo(models.Model):
  nombre = models.CharField(max_length=100)
  class Meta:
    db_table = "modelo_vehiculos"

  def __str__(self):
    return self.nombre
  
class MarcaVehiculo(models.Model):
  nombre = models.CharField(max_length=100)
  class Meta:
    db_table = "marca_vehiculos"

  def __str__(self):
    return self.nombre
  
class ColorVehiculo(models.Model):
  nombre = models.CharField(max_length=100)
  class Meta:
    db_table = "color_vehiculos"

  def __str__(self):
    return self.nombre

class Vehiculo(models.Model):
  patente = models.CharField(max_length=10)
  residente = models.ForeignKey(Residente, to_field='rut', on_delete=models.CASCADE)
  tipo_vehiculo = models.ForeignKey(TipoVehiculo, on_delete=models.CASCADE)
  marca = models.ForeignKey(MarcaVehiculo, on_delete=models.CASCADE)
  modelo = models.ForeignKey(ModeloVehiculo, on_delete=models.CASCADE)
  color = models.ForeignKey(ColorVehiculo, on_delete=models.CASCADE)
    
  class Meta:
      db_table = "vehiculos"
    
  def __str__(self):
      return str(self.patente)
    
class PatenteAutorizada(models.Model):
  vehiculo = models.ForeignKey(Vehiculo, on_delete=models.CASCADE)
  fecha_inicio = models.DateField()
  fecha_termino = models.DateField()
    
  class Meta:
    db_table = "patentes_autorizadas"
    
  def __str__(self):
    return self.vehiculo.patente

class RegistroAcceso(models.Model):
  fecha_hora_ingreso = models.DateTimeField()
  fecha_hora_salida = models.DateTimeField()
  residente = models.ForeignKey(Residente, on_delete=models.CASCADE)
  trabajador = models.ForeignKey(Trabajador, on_delete=models.CASCADE)
  vehiculo = models.ManyToManyField(Vehiculo)
    
  class Meta:
    db_table = "registros_accesos"
    
    def __str__(self):
        return self.residente.nombre

class Informe(models.Model):
    residente = models.ForeignKey(Residente, on_delete=models.CASCADE)
    registros_acceso = models.ForeignKey(RegistroAcceso, on_delete=models.CASCADE)
    vehiculo = models.ForeignKey(Vehiculo, on_delete=models.CASCADE)
    
    fecha = models.DateField()
    descripcion = models.TextField()
    # Otros campos del informe

    def __str__(self):
        return f"Informe {self.id} - Residente: {self.residente}"

    class Meta:
        verbose_name_plural = "Informes"