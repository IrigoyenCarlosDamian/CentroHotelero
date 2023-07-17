from django.core.mail import message
from django.forms import *
from django import forms
from Apps.Core.models import Persona,Rol
from django.forms import ValidationError
from django.core.validators import RegexValidator
import re

class PersonaForm(ModelForm):
    class Meta:
        model = Persona
        fields = '__all__'
        widgets = {
            'tipo_documento': forms.Select(attrs={
                'class': 'form-control col-md-7 col-xs-12',
                'required': 'required',
                'autofocus': False
            }),
            'documento': forms.TextInput(attrs={
                'class': 'form-control col-md-7 col-xs-12',
                'required': 'required',
                'autofocus': False
            }),
            'nombre': forms.TextInput(attrs={
                'class': 'form-control col-md-7 col-xs-12',
                'required': 'required',
                'autofocus': False
            }),
            'apellido': forms.TextInput(attrs={
                'class': 'form-control col-md-7 col-xs-12',
                'required': 'required',
                'autofocus': False
            }),
        }
        error_messages = {'documento':{ 'max_length': ("Documento demasiado extenso")}}

    def clean_nombre(self, *args, **kwargs):
        # Validación de Nombre
        # Solo permite caracteres
        nombre = self.cleaned_data.get("nombre")
        if not nombre.isalpha():
            raise forms.ValidationError('Nombre Incorrecto: No puede contener numeros')
        return nombre

    def clean_apellido(self, *args, **kwargs):
        # Validación de Apellido
        # Especificamos que validaremos Letras Mayusculas, Minúsculas y espacio en blanco
        # Esperamos como mínimo 2 caracteres y un máximo de 20
        clean_apellido = re.compile(r'^[A-Z|a-z| ]{2,20}$')

        apellido = self.cleaned_data.get("apellido")
        if not clean_apellido.search(apellido):
            raise forms.ValidationError('Apellido Incorrecto: No puede contener numeros')

        return apellido

    def clean_documento(self):
        #validacion de Documento
        #solo permite numeros
        documento = self.cleaned_data.get("documento")
        if not documento.isnumeric():
            raise ValidationError("Documento Invalido: Solo puede contener numeros")
        if Persona.objects.filter(documento = documento).exists():
            raise ValidationError("Ya existe el documento")
        return documento

def get_roles_vendedor():
    roles = Rol.TIPOS
    roles_vendedor = []
    for r in roles:
        if r[0] == 2:
            roles_vendedor.append(r)

    return roles_vendedor

def get_roles_encargado():
    roles = Rol.TIPOS
    roles_encargado = []
    for r in roles:
        if r[0] == 1:
            roles_encargado.append(r)

    return roles_encargado

def get_roles_cliente():
    roles = Rol.TIPOS
    roles_cliente = []
    for r in roles:
        if r[0] == 3:
            roles_cliente.append(r)

    return roles_cliente



def get_rol_class(tipo_rol):
    rol = None
    for klass in Rol.__subclasses__():
        if klass.TIPO == tipo_rol:
            rol = klass
    return rol


class VendedorForm(PersonaForm):
    email = forms.CharField(widget=forms.EmailInput(attrs={
        'class': 'form-control col-md-7 col-xs-12',
        'required': 'required',
        'autofocus': False
    }))
    usuario = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control col-md-7 col-xs-12',
        'required': 'required',
        'autofocus': False
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control col-md-7 col-xs-12',
        'required': 'required',
        'autofocus': False
    }))

    def save(self, commit=True):
        persona = super().save(commit=commit)
        usuario = self.cleaned_data['usuario']
        email = self.cleaned_data['email']
        password = self.cleaned_data['password']
        return persona.hacer_vendedor(usuario, email, password)


class EncargadoForm(PersonaForm):
    email = forms.CharField(widget=forms.EmailInput(attrs={
        'class': 'form-control col-md-7 col-xs-12',
        'required': 'required',
        'autofocus': False
    }))

    usuario = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control col-md-7 col-xs-12',
        'required': 'required',
        'autofocus': False
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control col-md-7 col-xs-12',
        'required': 'required',
        'autofocus': False
    }))
    def save(self, commit=True):
        persona = super().save(commit=commit)
        usuario = self.cleaned_data['usuario']
        email = self.cleaned_data['email']
        password = self.cleaned_data['password']
        return persona.hacer_encargado(usuario, email, password)


class ClienteForm(PersonaForm):
    email = forms.CharField(widget=forms.EmailInput(attrs={
        'class': 'form-control col-md-7 col-xs-12',
        'required': 'required',
        'autofocus': False
    }))
    def save(self, commit=True):
        persona = super().save(commit=commit)
        return persona.hacer_cliente()
