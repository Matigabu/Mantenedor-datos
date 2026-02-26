from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, redirect, render

from .forms import UsuarioCreateForm, PasswordChangeSimpleForm


def es_supervisor(user):
    return user.is_authenticated and (
        user.is_superuser or user.groups.filter(name="supervisores").exists()
    )


solo_supervisor = user_passes_test(es_supervisor)


def objetivo_es_superuser_protegido(request_user, user_obj):
    return user_obj.is_superuser and not request_user.is_superuser


@solo_supervisor
def lista_usuarios(request):
    q = (request.GET.get("q") or "").strip()

    qs = User.objects.all().order_by("username")
    if q:
        qs = qs.filter(username__icontains=q)

    return render(request, "usuarios/lista_usuarios.html", {"usuarios": qs, "q": q})


@solo_supervisor
def crear_usuario(request):
    if request.method == "POST":
        form = UsuarioCreateForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Usuario creado correctamente.")
            return redirect("usuarios:lista")
    else:
        form = UsuarioCreateForm()

    return render(request, "usuarios/form.html", {"form": form, "titulo": "Crear usuario"})


@solo_supervisor
def editar_usuario(request, pk):
    user_obj = get_object_or_404(User, pk=pk)

    if objetivo_es_superuser_protegido(request.user, user_obj):
        messages.error(request, "No tienes permiso para modificar un superusuario.")
        return redirect("usuarios:lista")

    if request.method == "POST":
        nuevo_activo = bool(request.POST.get("is_active"))
        nuevo_staff = bool(request.POST.get("is_staff"))

        if user_obj == request.user and not nuevo_activo:
            messages.warning(request, "No puedes desactivar tu propio usuario.")
            return redirect("usuarios:editar", pk=pk)

        user_obj.first_name = (request.POST.get("first_name") or "").strip()
        user_obj.last_name = (request.POST.get("last_name") or "").strip()
        user_obj.email = (request.POST.get("email") or "").strip()
        user_obj.is_active = nuevo_activo
        user_obj.is_staff = nuevo_staff
        user_obj.save()

        messages.success(request, "Usuario actualizado.")
        return redirect("usuarios:lista")

    return render(request, "usuarios/editar.html", {"u": user_obj})


@solo_supervisor
def cambiar_password(request, pk):
    user_obj = get_object_or_404(User, pk=pk)

    if objetivo_es_superuser_protegido(request.user, user_obj):
        messages.error(request, "No tienes permiso para cambiar la contraseña de un superusuario.")
        return redirect("usuarios:lista")

    if request.method == "POST":
        form = PasswordChangeSimpleForm(request.POST)
        if form.is_valid():
            user_obj.set_password(form.cleaned_data["password1"])
            user_obj.save()
            messages.success(request, "Contraseña actualizada.")
            return redirect("usuarios:lista")
    else:
        form = PasswordChangeSimpleForm()

    return render(request, "usuarios/password.html", {"form": form, "u": user_obj})


@solo_supervisor
def toggle_activo(request, pk):
    user_obj = get_object_or_404(User, pk=pk)

    if objetivo_es_superuser_protegido(request.user, user_obj):
        messages.error(request, "No tienes permiso para activar o desactivar un superusuario.")
        return redirect("usuarios:lista")

    if user_obj == request.user:
        messages.warning(request, "No puedes desactivar tu propio usuario.")
        return redirect("usuarios:lista")

    user_obj.is_active = not user_obj.is_active
    user_obj.save()
    messages.success(request, "Estado actualizado.")
    return redirect("usuarios:lista")