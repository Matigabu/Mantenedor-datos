from django.shortcuts import render, redirect
from .forms import EventoForm


def registrar_evento(request):
    if request.method == "POST":
        form = EventoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("dashboard:dashboard") 
    else:
        form = EventoForm()

    return render(request, "eventos/registrar_evento.html", {"form": form})


def lista_eventos(request):
    return redirect("dashboard:dashboard")