from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from .forms import EventoForm, usuario_puede_asignar_turno, obtener_turno_usuario


@login_required
def registrar_evento(request):
    puede_asignar_turno = usuario_puede_asignar_turno(request.user)

    if request.method == "POST":
        form = EventoForm(request.POST, user=request.user)
        if form.is_valid():
            evento = form.save(commit=False)

            # Registrar quién creó el evento
            evento.creado_por = request.user

            # Blindaje backend: si no puede elegir, se fuerza su turno
            if not puede_asignar_turno:
                evento.turno = obtener_turno_usuario(request.user)

            evento.save()
            return redirect("dashboard:dashboard")
    else:
        form = EventoForm(user=request.user)

    return render(request, "eventos/registrar_evento.html", {
        "form": form,
        "puede_asignar_turno": puede_asignar_turno,
    })