from django import forms
from django.contrib.auth.forms import AuthenticationForm

class AutenticacionForm(AuthenticationForm):
    email = forms.EmailField(widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'usuario@correo.cl'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control'}))


class DonarForm(forms.Form):
    # def __init__(self, *args, **kwargs):
    #     super(DonarForm, self).__init__(*args, **kwargs)
    #     for visible in self.visible_fields():
    #         if isinstance(visible.field.widget, forms.widgets.RadioSelect):
    #             visible.field.widget.attrs['class'] = 'form-check-input'
    #         elif isinstance(visible.fields.widget, forms.widget.):
    #             visible.field.widget.attrs['class'] = 'form-control'
    #         else:
    #             visible.field.widget.attrs['class']

    cantidad = forms.IntegerField(
        min_value=1000,
        max_value=1000000,
        label='Cantidad',
        required=True,
        widget=forms.TextInput(attrs={'class':'form-control'})
    )
    nombre = forms.CharField(
        min_length=3,
        max_length=40,
        label='Nombre',
        required=True,
        widget=forms.TextInput(attrs={'title': 'El Nombre debe tener entre 3 a 15 caracteres', 'class': 'form-control'})
    )
    apellido = forms.CharField(
        min_length=3,
        max_length=40,
        label='Apellido',
        required=True,
        widget=forms.TextInput(attrs={'title': 'Ingresa solo letras y espacios', 'class': 'form-control'})
    )
    rut = forms.CharField(
        max_length=12,
        label='RUT',
        required=True,
        widget=forms.TextInput(attrs={ 'title': 'Ingresa un RUT válido', 'class': 'form-control'})
    )
    correo = forms.EmailField(
        max_length=50,
        label='Correo Electrónico',
        required=True,
        widget=forms.TextInput(attrs={'class':'form-control'})
    )
    celular = forms.CharField(
        max_length=11,
        label='Celular',
        required=True,
        widget=forms.TextInput(attrs={'title': 'Ingresa un número de celular válido', 'class': 'form-control'})
    )
    METODO_PAGO_CHOICES = [
        ('Crédito', 'Crédito'),
        ('Débito', 'Débito')
    ]

    optradio = forms.ChoiceField(
        choices=METODO_PAGO_CHOICES,
        widget=forms.RadioSelect(attrs={'required': 'required'}),
        required=True,
        label='Método de Pago',
        error_messages={'required': 'Debe seleccionar un método de pago'}
    )
    titular = forms.CharField(
        max_length=40,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        required=True,
        label='Titular de la tarjeta',
        error_messages={'required': 'Debe ingresar un nombre válido'}
    )
    numero = forms.CharField(
        min_length=16,
        max_length=19,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        required=True,
        label='Número de la tarjeta',
        error_messages={'required': 'El número de tarjeta no es válido'}
    )
    codigo = forms.CharField(
        min_length=3,
        max_length=3,
        widget=forms.TextInput(attrs={ 'class': 'form-control'}),
        required=True,
        label='Código de seguridad',
        error_messages={'required': 'Debe ingresar un código válido de 3 dígitos'}
    )
    fecha = forms.CharField(
        widget=forms.DateInput(attrs={'type': 'month', 'min': '2024-01', 'max': '2045-12', 'class': 'form-control'}),
        required=True,
        label='Fecha de caducidad',
        error_messages={'required': 'Debe ingresar una fecha válida entre 2024 y 2045'}
    )

class ContactoForm(forms.Form):
    nombre = forms.CharField(label='Nombre completo', max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(label='Correo Electrónico', widget=forms.TextInput(attrs={'class': 'form-control'}))
    razon = forms.ChoiceField(label='Motivo de contacto', choices=(
        ('', 'Seleccione un motivo'),
        ('1', 'Duda'),
        ('2', 'Sugerencia'),
        ('3', 'Reclamo'),
    ), widget=forms.Select(attrs={'class': 'form-select'}))
    comentario = forms.CharField(label='Su mensaje', widget=forms.Textarea(attrs={'rows': 8, 'cols': 7, 'maxlength': 700, 'class': 'form-control'}))
    agree = forms.BooleanField(
    label='He leído y acepto los términos y condiciones.', 
    error_messages= {'required': 'Debe aceptar nuestros términos y condiciones.'}, 
    widget=forms.CheckboxInput(attrs={'class': 'form-check'}))

class RegistroForm(forms.Form):

    correo = forms.EmailField(
        max_length=35,
        label='Correo Electrónico',
        required=True,
        widget=forms.TextInput(attrs={ 'class': 'form-control'})
    )
    password = forms.CharField(
        label='Contraseña',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'id': 'password'}),
        min_length=8,
    ) 
    confirm_password = forms.CharField(
        label='Confirmar Contraseña',
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        min_length=8
    )
    primer_nombre = forms.CharField(
        min_length=3,
        max_length=15,
        label='Primer Nombre',
        required=True,
        widget=forms.TextInput(attrs={'pattern': '[A-Za-zñÑáéíóúÁÉÍÓÚ\s]+', 'class': 'form-control'})
    )
    segundo_nombre = forms.CharField(
        min_length=3,
        max_length=15,
        label='Segundo Nombre',
        widget=forms.TextInput(attrs={'pattern': '[A-Za-zñÑáéíóúÁÉÍÓÚ\s]+', 'class': 'form-control', 'default':' '})
    )
    primer_apellido = forms.CharField(
        min_length=3,
        max_length=15,
        label='Primer Apellido',
        required=True,
        widget=forms.TextInput(attrs={'pattern': '[A-Za-zñÑáéíóúÁÉÍÓÚ\s]+', 'class': 'form-control'})
    )
    segundo_apellido = forms.CharField(
        min_length=3,
        max_length=15,
        label='Segundo Apellido',
        widget=forms.TextInput(attrs={'pattern': '[A-Za-zñÑáéíóúÁÉÍÓÚ\s]+', 'class': 'form-control', 'default':' '})
    )
    direccion = forms.CharField(
        min_length=10,
        max_length=150,
        label='Dirección',
        required=True,
        widget=forms.TextInput(attrs={'pattern': '[A-Za-zñÑáéíóúÁÉÍÓÚ0-9\s]+','class': 'form-control'})
    ) 
    rut = forms.CharField(
        min_length=9,
        max_length=10,
        label='RUT',
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )