from django import forms
from .models import Evento


class EventoForm(forms.ModelForm):

    class Meta:
        model = Evento
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

      
        for field in self.fields.values():
            css_class = 'form-control'
            if isinstance(field.widget, forms.CheckboxInput):
                css_class = 'form-check-input'
            field.widget.attrs.update({'class': css_class})

        
        # Placeholders inputs
        
        if 'numero_orden' in self.fields:
            self.fields['numero_orden'].widget.attrs.update({
                'placeholder': 'Ingrese N° de orden si corresponde'
            })

        if 'numero_circuito' in self.fields:
            self.fields['numero_circuito'].widget.attrs.update({
                'placeholder': 'Ej: C-12'
            })

        if 'descripcion' in self.fields:
            self.fields['descripcion'].widget.attrs.update({
                'placeholder': 'Describa la falla o intervención realizada'
            })

        
        for fname in ('numero_orden', 'cantidad_luminaria', 'tipo_luminaria'):
            if fname in self.fields:
                self.fields[fname].required = False

        
        dropdown_placeholders = {
            # Origen
            'canal': 'Seleccione canal…',
            'solicitante': 'Seleccione solicitante…',

            # Ubicación
            'torre': 'Seleccione torre…',
            'piso': 'Seleccione piso…',
            'servicio': 'Seleccione servicio…',

            # Detalle
            'tipo_trabajo': 'Seleccione tipo de trabajo…',
            'tipo_luminaria': 'Seleccione tipo de luminaria…',

            # Estado
            'estado': 'Seleccione estado…',
            'turno': 'Seleccione turno…',
        }

        for fname, text in dropdown_placeholders.items():
            if fname in self.fields and hasattr(self.fields[fname], 'choices'):
                choices = list(self.fields[fname].choices)
                
                if choices and choices[0][0] == '':
                    choices[0] = ('', text)
                    self.fields[fname].choices = choices

    
    # Validaciones 
    
    def clean(self):
        cleaned_data = super().clean()

        canal = cleaned_data.get('canal')
        tipo_trabajo = cleaned_data.get('tipo_trabajo')

        numero_orden = cleaned_data.get('numero_orden')
        cantidad = cleaned_data.get('cantidad_luminaria')
        tipo_lum = cleaned_data.get('tipo_luminaria')

        
        if canal == "FRACTTAL":
            if not numero_orden:
                self.add_error(
                    'numero_orden',
                    'Debe ingresar el N° de orden cuando el canal es Fracttal.'
                )
        else:
            cleaned_data['numero_orden'] = None

        
        if tipo_trabajo == "LUMINARIA":
            if not cantidad:
                self.add_error(
                    'cantidad_luminaria',
                    'Debe indicar la cantidad de luminarias.'
                )
            if not tipo_lum:
                self.add_error(
                    'tipo_luminaria',
                    'Debe indicar el tipo de luminaria.'
                )
        else:
            cleaned_data['cantidad_luminaria'] = None
            cleaned_data['tipo_luminaria'] = None

        return cleaned_data