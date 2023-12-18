from django import forms
from django.contrib.admin.widgets import AutocompleteSelect
from django.contrib import admin
from .models import Residente,Vehiculo,PatenteAutorizada, RegistroAcceso, Trabajador, TipoTrabajador
import re

class ResidenteForm(forms.ModelForm):
    RUT_REGEX = r'^\d{1,2}\.\d{3}\.\d{3}[-][0-9kK]{1}$'
    EMAIL_REGEX = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    PHONE_REGEX = r'^(\+?56)?(\s?)(0?9)(\s?)[98765432]\d{7}$'

    class Meta:
        model = Residente
        fields = '__all__'
        labels = {
            
            'numero_casa': 'Número de Casa',
            'telefono': 'Número Telefónico',
        }
        widgets = {
            'ciudad': AutocompleteSelect(Residente._meta.get_field('ciudad').remote_field, admin.site, attrs={'placeholder': 'seleccionar'}),
        }

    def clean_rut(self):
        rut = self.cleaned_data.get('rut')
        if not re.match(self.RUT_REGEX, rut):
            raise forms.ValidationError('El Rut no es válido.')
        return rut
    
    def clean_nombre(self):
        nombre = self.cleaned_data.get('nombre')
        if not nombre.isalpha():
            raise forms.ValidationError('El nombre no es válido.')
        return nombre

    def clean_apellidos(self):
        apellidos = self.cleaned_data.get('apellidos')
        if not apellidos.isalpha():
            raise forms.ValidationError('Los apellidos no son válidos.')
        return apellidos
    
    def clean_correo(self):
        correo = self.cleaned_data.get('correo')
        if not re.match(self.EMAIL_REGEX, correo):
            raise forms.ValidationError('El correo no es válido.')
        return correo

    def clean_telefono(self):
        telefono = self.cleaned_data.get('telefono')
        if not re.match(self.PHONE_REGEX, telefono):
            raise forms.ValidationError('El número telefónico no es válido.')
        return telefono
    
    def clean_numero_casa(self):
        numero_casa = self.cleaned_data.get('numero_casa')
        if numero_casa < 0 or numero_casa > 9999:
            raise forms.ValidationError('El número de casa no es válido.')
        return numero_casa


class VehiculoForm(forms.ModelForm):
    PATENTE_REGEX = r'^[A-Za-z]{4}\d{2}$'

    class Meta:
        model = Vehiculo
        fields = '__all__'
        labels = {
            'residente': 'Residente',
            'patente': 'Patente',
            'tipo_vehiculo': 'Tipo de Vehículo',
        }
        widgets = {
            'residente': AutocompleteSelect(Vehiculo._meta.get_field('residente').remote_field, admin.site, attrs={'placeholder': 'seleccionar'})   
        }

    def clean_patente(self):
        patente = self.cleaned_data.get('patente')
        if not re.match(self.PATENTE_REGEX, patente):
            raise forms.ValidationError('La patente no es válida.')
        return patente
    

class RegistroAccesoForm(forms.ModelForm):
     class Meta:
        model = RegistroAcceso
        fields = ['fecha_hora_ingreso', 'fecha_hora_salida']


class TrabajadorForm(forms.ModelForm):
    RUT_REGEX = r'^\d{1,2}\.\d{3}\.\d{3}[-][0-9kK]{1}$'
    EMAIL_REGEX = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    PHONE_REGEX = r'^(\+?56)?(\s?)(0?9)(\s?)[98765432]\d{7}$'

    tipo_trabajador = forms.ModelChoiceField(queryset=TipoTrabajador.objects.all())

    class Meta:
        model = Trabajador
        fields = '__all__'
        labels = {
            'nombre_usuario': 'Nombre de Usuario',
            'password': 'Contraseña',
            'tipo_trabajador': 'Tipo de Trabajador',
        }
        widgets = {
            'ciudad': AutocompleteSelect(Trabajador._meta.get_field('ciudad').remote_field, admin.site, attrs={'placeholder': 'seleccionar'}),
            'tipo_trabajador': forms.Select(),  # No es necesario asignar el widget aquí
        }

    def clean_rut(self):
        rut = self.cleaned_data.get('rut')
        if not re.match(self.RUT_REGEX, rut):
            raise forms.ValidationError('El Rut no es válido.')
        return rut
    
    def clean_nombre(self):
        nombre = self.cleaned_data.get('nombre')
        if not nombre.isalpha():
            raise forms.ValidationError('El nombre no es válido.')
        return nombre

    def clean_apellidos(self):
        apellidos = self.cleaned_data.get('apellidos')
        if not apellidos.isalpha():
            raise forms.ValidationError('Los apellidos no son válidos.')
        return apellidos



















#     def __init__(self, *args, **kwargs):
#         super(self.__class__, self).__init__(*args, **kwargs)
#         # asi vuelves tus campos no requeridos
#         self.fields['amount'].required = False
#         self.fields['discount'].required = False
#         self.fields['comments'].required = False
#         self.fields['message'].required = False

#     def clean(self):
#         cleaned_data = super().clean()
#         start_date = cleaned_data.get("start_date")
#         end_date = cleaned_data.get("end_date")
#         if end_date < start_date:
#             raise forms.ValidationError("Las fechas no concuerdan.")
