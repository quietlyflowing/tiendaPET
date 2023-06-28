from django import forms

class DonarForm(forms.Form):
    cantidad = forms.IntegerField(
        min_value=1000,
        max_value=1000000,
        label='Cantidad',
        required=True
    )
    nombre = forms.CharField(
        min_length=3,
        max_length=15,
        label='Nombre',
        required=True,
        widget=forms.TextInput(attrs={'pattern': '[A-Za-zñÑáéíóúÁÉÍÓÚ\s]+', 'title': 'El Nombre debe tener entre 3 a 15 caracteres'})
    )
    apellido = forms.CharField(
        min_length=3,
        max_length=15,
        label='Apellido',
        required=True,
        widget=forms.TextInput(attrs={'pattern': '[A-Za-zñÑáéíóúÁÉÍÓÚ\s]+', 'title': 'Ingresa solo letras y espacios'})
    )
    rut = forms.CharField(
        max_length=12,
        label='RUT',
        required=True,
        widget=forms.TextInput(attrs={'pattern': r'\d{7,8}-[0-9kK]{1}', 'title': 'Ingresa un RUT válido'})
    )
    correo = forms.EmailField(
        max_length=35,
        label='Correo Electrónico',
        required=True
    )
    celular = forms.CharField(
        max_length=11,
        label='Celular',
        required=True,
        widget=forms.TextInput(attrs={'pattern': '(56|9)(\d{8}|\d{9})', 'title': 'Ingresa un número de celular válido'})
    )
    METODO_PAGO_CHOICES = [
        ('option1', 'Crédito'),
        ('option2', 'Débito')
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
        widget=forms.TextInput(attrs={'pattern': r'^[a-zA-ZÀ-ÖØ-öø-ÿ\s.\'-]{1,40}$'}),
        required=True,
        label='Titular de la tarjeta',
        error_messages={'required': 'Debe ingresar un nombre válido'}
    )
    numero = forms.CharField(
        min_length=16,
        max_length=19,
        widget=forms.TextInput(attrs={'pattern': r'[0-9]{4}?[0-9]{4}?[0-9]{4}?[0-9]{4}'}),
        required=True,
        label='Número de la tarjeta',
        error_messages={'required': 'El número de tarjeta no es válido'}
    )
    codigo = forms.CharField(
        min_length=3,
        max_length=3,
        widget=forms.TextInput(attrs={'pattern': r'^[0-9]{3}$'}),
        required=True,
        label='Código de seguridad',
        error_messages={'required': 'Debe ingresar un código válido de 3 dígitos'}
    )
    fecha = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'month', 'min': '2024-01', 'max': '2045-12'}),
        required=True,
        label='Fecha de caducidad',
        error_messages={'required': 'Debe ingresar una fecha válida entre 2024 y 2045'}
    )

class ContactoForm(forms.Form):
    nombre = forms.CharField(label='Nombre completo', max_length=100)
    email = forms.EmailField(label='Correo Electrónico')
    razon = forms.ChoiceField(label='Motivo de contacto', choices=(
        ('', 'Seleccione un motivo'),
        ('1', 'Duda'),
        ('2', 'Sugerencia'),
        ('3', 'Reclamo'),
    ))
    comentario = forms.CharField(label='Su mensaje', widget=forms.Textarea(attrs={'rows': 8, 'cols': 7, 'maxlength': 700}))
    agree = forms.BooleanField(label='He leído y acepto los términos y condiciones.')