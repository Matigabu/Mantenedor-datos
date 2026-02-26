from django import forms
from .models import Evento


def usuario_puede_asignar_turno(user):
    return bool(
        user
        and user.is_authenticated
        and (
            user.is_superuser
            or user.is_staff
            or user.groups.filter(name="supervisores").exists()
        )
    )


def obtener_turno_usuario(user):
    """
    Para técnicos:
    el turno se obtiene desde el username (T1, T2, T3, T4, T5),
    siempre que el usuario pertenezca al grupo 'tecnicos'.
    """
    if not user or not user.is_authenticated:
        return None

    if not user.groups.filter(name="tecnicos").exists():
        return None

    username = (user.username or "").strip().upper()
    turnos_validos = {codigo for codigo, _ in Evento.TURNOS}

    if username in turnos_validos:
        return username

    return None


class EventoForm(forms.ModelForm):
    class Meta:
        model = Evento
        fields = "__all__"

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)

        self.user = user
        self.puede_asignar_turno = usuario_puede_asignar_turno(user)
        self.turno_usuario = obtener_turno_usuario(user)

        # Mantener clase Bootstrap / AdminLTE
        for f in self.fields.values():
            widget_name = f.widget.__class__.__name__
            if widget_name == "CheckboxInput":
                css = "form-check-input"
            else:
                css = "form-control"

            actual = f.widget.attrs.get("class", "")
            if css not in actual:
                f.widget.attrs["class"] = f"{actual} {css}".strip()

        # Reemplazar "---------" por textos guía
        placeholders = {
            "canal": "Seleccione canal",
            "solicitante": "Seleccione solicitante",
            "torre": "Seleccione torre",
            "piso": "Seleccione piso",
            "servicio": "Seleccione servicio",
            "tipo_trabajo": "Seleccione tipo de trabajo",
            "estado": "Seleccione estado",
            "turno": "Seleccione técnico / turno",
            "tipo_luminaria": "Seleccione tipo de luminaria",
        }

        for name, text in placeholders.items():
            if name not in self.fields:
                continue

            field = self.fields[name]

            if isinstance(field, forms.ModelChoiceField):
                field.empty_label = text
            elif isinstance(field.widget, forms.Select):
                choices = list(field.choices)

                if choices:
                    if choices[0][0] == "":
                        choices[0] = ("", text)
                    else:
                        choices.insert(0, ("", text))
                else:
                    choices = [("", text)]

                field.choices = choices

        # Control del campo turno
        if "turno" in self.fields:
            field_turno = self.fields["turno"]

            if self.puede_asignar_turno:
                field_turno.disabled = False
                field_turno.widget.attrs.pop("disabled", None)
            else:
                field_turno.disabled = True
                field_turno.widget.attrs["disabled"] = "disabled"

                # Mostrar visualmente el turno correcto en el dropdown bloqueado
                if self.turno_usuario:
                    field_turno.initial = self.turno_usuario
                    self.initial["turno"] = self.turno_usuario

    def clean(self):
        cleaned = super().clean()

        # Blindaje backend: si no puede elegir turno, se fuerza desde el login
        if not self.puede_asignar_turno:
            if self.turno_usuario:
                cleaned["turno"] = self.turno_usuario
            else:
                raise forms.ValidationError(
                    "Tu usuario no tiene un turno válido asignado. Debe pertenecer a 'tecnicos' y llamarse T1, T2, T3, T4 o T5."
                )

        return cleaned