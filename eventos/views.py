from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, Http404
from django.shortcuts import get_object_or_404, redirect, render

from .forms import EventoForm, usuario_puede_asignar_turno, obtener_turno_usuario
from .models import Evento, SeguimientoFracttal


@login_required
def registrar_evento(request):
    puede_asignar_turno = usuario_puede_asignar_turno(request.user)

    if request.method == "POST":
        form = EventoForm(request.POST, user=request.user)

        if form.is_valid():
            evento = form.save(commit=False)

            # Registrar quién creó el intento actual
            evento.creado_por = request.user

            # Blindaje backend: si no puede elegir, se fuerza su turno
            if not puede_asignar_turno:
                evento.turno = obtener_turno_usuario(request.user)

            # Datos extra del bloque dinámico
            cierre_ot_fracttal = (request.POST.get("cierre_ot_fracttal") or "").strip()
            restriccion_fracttal = (request.POST.get("restriccion_fracttal") or "").strip()
            encargado_area_fracttal = (request.POST.get("encargado_area_fracttal") or "").strip()
            detalle_seguimiento_fracttal = (request.POST.get("detalle_seguimiento_fracttal") or "").strip()

            # ============================
            # FLUJO ESPECIAL SOLO FRACTTAL
            # ============================
            if evento.canal == "FRACTTAL" and evento.numero_orden:
                evento_existente = (
                    Evento.objects
                    .filter(canal="FRACTTAL", numero_orden=evento.numero_orden)
                    .order_by("fecha_creacion")
                    .first()
                )

                # Validación: para FRACTTAL se debe indicar si se pudo cerrar
                if cierre_ot_fracttal not in ["SI", "NO"]:
                    form.add_error(
                        None,
                        "Debes indicar si se pudo cerrar esta OT."
                    )

                # Si la OT ya existe, NO crear otro evento:
                # solo agregar un seguimiento al historial
                elif evento_existente:
                    if not restriccion_fracttal:
                        form.add_error(
                            None,
                            "Debes indicar la restricción para registrar un seguimiento de una OT existente."
                        )
                    else:
                        detalle_final = (
                            detalle_seguimiento_fracttal
                            or evento.descripcion
                            or "Se registra un nuevo intento de atención."
                        )

                        SeguimientoFracttal.objects.create(
                            evento=evento_existente,
                            restriccion=restriccion_fracttal,
                            encargado_area=encargado_area_fracttal,
                            detalle=detalle_final,
                            creado_por=request.user,
                        )

                        return redirect("dashboard:dashboard")

                # Si la OT NO existe y no se pudo cerrar,
                # también debe venir con restricción
                elif cierre_ot_fracttal == "NO" and not restriccion_fracttal:
                    form.add_error(
                        None,
                        "Debes indicar la restricción porque la OT no se pudo cerrar."
                    )

            # ============================
            # FLUJO NORMAL
            # ============================
            if not form.non_field_errors():
                evento.save()

                # Si es FRACTTAL, crear seguimiento inicial según el resultado
                if evento.canal == "FRACTTAL" and evento.numero_orden:
                    if cierre_ot_fracttal == "NO":
                        SeguimientoFracttal.objects.create(
                            evento=evento,
                            restriccion=restriccion_fracttal,
                            encargado_area=encargado_area_fracttal,
                            detalle=(
                                detalle_seguimiento_fracttal
                                or evento.descripcion
                                or "La OT no se pudo cerrar en el primer intento."
                            ),
                            creado_por=request.user,
                        )
                    else:
                        SeguimientoFracttal.objects.create(
                            evento=evento,
                            restriccion="OT cerrada",
                            encargado_area=encargado_area_fracttal,
                            detalle=(
                                detalle_seguimiento_fracttal
                                or evento.descripcion
                                or "La OT fue atendida y cerrada."
                            ),
                            creado_por=request.user,
                        )

                return redirect("dashboard:dashboard")
    else:
        form = EventoForm(user=request.user)

    return render(
        request,
        "eventos/registrar_evento.html",
        {
            "form": form,
            "puede_asignar_turno": puede_asignar_turno,
        },
    )


@login_required
def validar_ot_fracttal(request):
    numero_orden = (request.GET.get("numero_orden") or "").strip()

    existe = False
    if numero_orden:
        existe = Evento.objects.filter(
            canal="FRACTTAL",
            numero_orden=numero_orden
        ).exists()

    return JsonResponse({"existe": existe})


@login_required
def ver_seguimiento_fracttal(request, pk):
    evento = get_object_or_404(Evento, pk=pk)

    if evento.canal != "FRACTTAL" or not evento.numero_orden:
        raise Http404("Este evento no tiene seguimiento Fracttal.")

    seguimientos = evento.seguimientos_fracttal.all().order_by("-fecha_creacion")

    return render(
        request,
        "eventos/seguimiento_fracttal.html",
        {
            "evento": evento,
            "seguimientos": seguimientos,
        },
    )