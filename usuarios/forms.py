from django import forms
from django.contrib.auth.models import User

TURNOS = ["T1", "T2", "T3", "T4", "T5"]


class UsuarioCreateForm(forms.ModelForm):
    username = forms.CharField(
        label="Nombre de usuario",
        help_text="Máximo 150 caracteres. Letras, números y @/./+/-/_ solamente.",
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Ingrese el nombre de usuario",
                "autocomplete": "off",
            }
        ),
    )
    first_name = forms.CharField(
        label="Nombre",
        required=False,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Ingrese el nombre",
            }
        ),
    )
    last_name = forms.CharField(
        label="Apellido",
        required=False,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Ingrese el apellido",
            }
        ),
    )
    email = forms.EmailField(
        label="Correo electrónico",
        required=False,
        widget=forms.EmailInput(
            attrs={
                "class": "form-control",
                "placeholder": "Ingrese el correo",
            }
        ),
    )
    password1 = forms.CharField(
        label="Contraseña",
        help_text=(
            "<ul class='mb-0 ps-3'>"
            "<li>La contraseña no debe ser demasiado parecida a tu información personal.</li>"
            "<li>Debe contener al menos 8 caracteres.</li>"
            "<li>No debe ser una contraseña demasiado común.</li>"
            "<li>No puede estar compuesta solo por números.</li>"
            "</ul>"
        ),
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": "Ingrese la contraseña",
                "autocomplete": "new-password",
            }
        ),
    )
    password2 = forms.CharField(
        label="Confirmar contraseña",
        help_text="Ingrese nuevamente la contraseña para validarla.",
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": "Repita la contraseña",
                "autocomplete": "new-password",
            }
        ),
    )

    class Meta:
        model = User
        fields = ["username", "first_name", "last_name", "email", "is_active", "is_staff"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["is_active"].label = "Usuario activo"
        self.fields["is_staff"].label = "Es staff"
        self.fields["is_active"].widget.attrs.update({"class": "form-check-input"})
        self.fields["is_staff"].widget.attrs.update({"class": "form-check-input"})

    def clean_username(self):
        return self.cleaned_data["username"].strip()

    def clean(self):
        cleaned = super().clean()
        p1 = cleaned.get("password1")
        p2 = cleaned.get("password2")
        if p1 and p2 and p1 != p2:
            self.add_error("password2", "Las contraseñas no coinciden.")
        return cleaned

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UsuarioEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "email", "is_active", "is_staff"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["first_name"].label = "Nombre"
        self.fields["last_name"].label = "Apellido"
        self.fields["email"].label = "Correo electrónico"
        self.fields["is_active"].label = "Usuario activo"
        self.fields["is_staff"].label = "Es staff"

        for f in self.fields.values():
            css = "form-control"
            if f.widget.__class__.__name__ == "CheckboxInput":
                css = "form-check-input"
            f.widget.attrs.update({"class": css})


class PasswordChangeSimpleForm(forms.Form):
    password1 = forms.CharField(
        label="Nueva contraseña",
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": "Ingrese la nueva contraseña",
                "autocomplete": "new-password",
            }
        ),
    )
    password2 = forms.CharField(
        label="Confirmar nueva contraseña",
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": "Repita la nueva contraseña",
                "autocomplete": "new-password",
            }
        ),
    )

    def clean(self):
        cleaned = super().clean()
        if cleaned.get("password1") != cleaned.get("password2"):
            self.add_error("password2", "Las contraseñas no coinciden.")
        return cleaned