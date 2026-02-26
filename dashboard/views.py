from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from eventos.models import Evento


@login_required
def home(request):
    qs = Evento.objects.all().order_by("-fecha_creacion")

    canal = request.GET.get("canal", "").strip()
    solicitante = request.GET.get("solicitante", "").strip()
    torre = request.GET.get("torre", "").strip()
    piso = request.GET.get("piso", "").strip()
    servicio = request.GET.get("servicio", "").strip()
    tipo_trabajo = request.GET.get("tipo_trabajo", "").strip()
    estado = request.GET.get("estado", "").strip()
    turno = request.GET.get("turno", "").strip()

    q = request.GET.get("q", "").strip()
    desde = request.GET.get("desde", "").strip()
    hasta = request.GET.get("hasta", "").strip()

    if canal:
        qs = qs.filter(canal=canal)
    if solicitante:
        qs = qs.filter(solicitante=solicitante)
    if torre:
        qs = qs.filter(torre=torre)
    if piso:
        qs = qs.filter(piso=piso)
    if servicio:
        qs = qs.filter(servicio=servicio)
    if tipo_trabajo:
        qs = qs.filter(tipo_trabajo=tipo_trabajo)
    if estado:
        qs = qs.filter(estado=estado)
    if turno:
        qs = qs.filter(turno=turno)

    if desde:
        qs = qs.filter(fecha_creacion__date__gte=desde)
    if hasta:
        qs = qs.filter(fecha_creacion__date__lte=hasta)

    if q:
        qs = qs.filter(
            Q(numero_orden__icontains=q) |
            Q(habitacion_box__icontains=q) |
            Q(numero_circuito__icontains=q) |
            Q(descripcion__icontains=q)
        )

    page_sizes = [10, 25, 50, 100]
    page_size = request.GET.get("page_size", "25")
    if not str(page_size).isdigit():
        page_size = 25
    page_size = int(page_size)
    if page_size not in page_sizes:
        page_size = 25

    paginator = Paginator(qs, page_size)
    page_obj = paginator.get_page(request.GET.get("page", 1))

    base_qs = request.GET.copy()
    base_qs.pop("page", None)
    base_qs = base_qs.urlencode()

    return render(request, "dashboard/home.html", {
        "page_obj": page_obj,
        "base_qs": base_qs,
        "page_sizes": page_sizes,
        "f": {
            "canal": canal,
            "solicitante": solicitante,
            "torre": torre,
            "piso": piso,
            "servicio": servicio,
            "tipo_trabajo": tipo_trabajo,
            "estado": estado,
            "turno": turno,
            "q": q,
            "desde": desde,
            "hasta": hasta,
            "page_size": str(page_size),
        },
        "choices": {
            "canal": Evento.CANAL_CHOICES,
            "solicitante": Evento.SOLICITANTE_CHOICES,
            "torre": Evento.TORRE_CHOICES,
            "piso": Evento.PISO_CHOICES,
            "servicio": Evento.SERVICIO_CHOICES,
            "tipo_trabajo": Evento.TIPO_TRABAJO_CHOICES,
            "estado": Evento.ESTADO_CHOICES,
            "turno": Evento.TURNOS,
        }
    })