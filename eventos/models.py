from django.db import models
from django.conf import settings


class Evento(models.Model):

    creado_por = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="eventos_creados",
        verbose_name="Registrado por"
    )

    # ----------- ORIGEN -----------#
    CANAL_CHOICES = [
        ("RONDA", "Ronda programada"),
        ("WSP", "Whatsapp"),
        ("CALL", "Llamado"),
        ("TPROG", "Trabajo programado"),
        ("FRACTTAL", "Fracttal"),
        ("RADIO", "Radio"),
        ("MAIL", "Correo electrónico"),
    ]

    SOLICITANTE_CHOICES = [
        ("HOTELERIA", "Hotelería"),
        ("SERV_CLINICA", "Servicios clínica"),
        ("EXP_PACIENTE", "Experiencia de pacientes"),
        ("SUP_CLINICA", "Supervisión clínica"),
        ("CLIMA", "Climatización"),
        ("TPROG", "Trabajo programado"),
        ("EQ_MED", "Equipos médicos"),
    ]

    canal = models.CharField(max_length=20, choices=CANAL_CHOICES, db_index=True)
    numero_orden = models.CharField(max_length=100, blank=True, null=True)
    solicitante = models.CharField(max_length=50, choices=SOLICITANTE_CHOICES)

    # --------------UBICACIÓN ----------#
    TORRE_CHOICES = [
        ("A", "A"), ("B", "B"), ("C", "C"), ("CDA", "CDA"),
        ("D", "D"), ("E", "E"), ("F", "F"), ("G", "G"),
        ("H", "H"), ("I", "I"), ("J", "J"),
        ("SUBESTACIONES", "Subestaciones"),
        ("UPS", "UPS"),
        ("Z_CRITICAS", "Zonas críticas"),
    ]

    PISO_CHOICES = [
        ("1", "1"), ("2", "2"), ("3", "3"), ("4", "4"),
        ("5", "5"), ("6", "6"), ("7", "7"),
        ("1SUB", "1° sub"), ("2SUB", "2° sub"),
        ("3SUB", "3° sub"), ("4SUB", "4° sub"),
        ("5SUB", "5° sub"),
        ("AZOTEA", "Azotea"),
    ]

    torre = models.CharField(max_length=20, choices=TORRE_CHOICES, db_index=True)
    piso = models.CharField(max_length=20, choices=PISO_CHOICES, blank=True, null=True)

    SERVICIO_CHOICES = [
        ("BANCO_SANGRE", "Banco de sangre"),
        ("BANO_VEST", "Baño / vestidores"),
        ("BODEGA", "Bodega"),
        ("CAFETERIA", "Cafetería"),
        ("CALL_CENTER", "Call center"),
        ("CASINO", "Casino"),
        ("CIC", "Centro integral del cáncer"),
        ("CLIMA_AZOTEA", "Clima azotea"),
        ("CMA", "CMA"),
        ("CONSULTA_MED", "Consulta médica"),
        ("COR_INTENSIVA", "Coronaria intensiva"),
        ("DIALISIS", "Diálisis"),
        ("ESTACIONAMIENTO", "Estacionamiento"),
        ("ESTERILIZACION", "Esterilización"),
        ("FARMACIA", "Farmacia"),
        ("FLEISCHMANN", "Fleischmann"),
        ("GERENCIA", "Gerencia"),
        ("GIM_KINE", "Gimnasio / kinesiología"),
        ("HALL_ASC", "Hall de ascensores"),
        ("IMAGENES", "Imágenes"),
        ("LABORATORIO", "Laboratorio"),
        ("MED_PREVENTIVA", "Medicina preventiva"),
        ("MQ", "MQ"),
        ("NEONATOLOGIA", "Neonatología"),
        ("NEUROLOGIA", "Neurología"),
        ("OF_ADM", "Oficina administrativa"),
        ("PABELLON", "Pabellón"),
        ("PARKING", "Párking"),
        ("PASILLO", "Pasillo general"),
        ("REAS", "REAS"),
        ("RESIDENCIA", "Residencia"),
        ("SALA_ESPERA", "Sala de espera"),
        ("SEDILE", "Sedile"),
        ("SHAFT_TISAL", "Shaft TISAL"),
        ("SUBGERENCIA", "Subgerencia"),
        ("UCI", "UCI"),
        ("UPC_PED", "UPC pediátrico"),
        ("UPS", "UPS"),
        ("URGENCIA", "Urgencia"),
        ("UTI", "Uti"),
        ("VITAMINA", "Vitamina"),
    ]

    servicio = models.CharField(max_length=30, choices=SERVICIO_CHOICES, db_index=True)

    habitacion_box = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        verbose_name="N° habitación / Box"
    )

    # ------------------ DETALLE TÉCNICO ---------------#
    TIPO_TRABAJO_CHOICES = [
        ("ACCESO", "Acceso"),
        ("CABECERA", "Cabecera"),
        ("CIRCUITOS", "Circuitos"),
        ("CLAVE_ROJA", "Clave roja (humo/fuego)"),
        ("CORTE_COMP", "Corte compañía"),
        ("ARTEFACTO", "Artefacto"),
        ("LEVANTAMIENTO", "Levantamiento / identificación"),
        ("LUMINARIA", "Luminaria"),
        ("MANTENCION", "Mantención"),
        ("PROTOCOLOS", "Protocolos"),
        ("PRUEBA_VACIO", "Prueba en vacío"),
        ("REVISION", "Revisión / medición"),
        ("RONDA", "Ronda"),
        ("TABLEROS", "Tableros"),
        ("TIMBRE", "Timbre"),
    ]

    TIPO_LUMINARIA_CHOICES = [
        ("18W", "18W"),
        ("60X60", "60x60"),
        ("AMPOLLETA", "Ampolleta"),
        ("DICROICO", "Dicroicos"),
        ("CPI", "Foco CPI"),
        ("TUBO_LED", "Tubo LED"),
    ]

    tipo_trabajo = models.CharField(max_length=30, choices=TIPO_TRABAJO_CHOICES, db_index=True)

    numero_circuito = models.CharField(max_length=50, blank=True, null=True, verbose_name="N° circuito")
    cantidad_luminaria = models.IntegerField(blank=True, null=True)

    tipo_luminaria = models.CharField(
        max_length=50,
        choices=TIPO_LUMINARIA_CHOICES,
        blank=True,
        null=True
    )

    descripcion = models.TextField()

    # ---------------- ESTADO ---------------#
    ESTADO_CHOICES = [
        ("REALIZADO", "Realizado"),
        ("PENDIENTE", "Pendiente"),
    ]

    TURNOS = [
        ("T1", "T1"),
        ("T2", "T2"),
        ("T3", "T3"),
        ("T4", "T4"),
        ("T5", "T5"),
    ]

    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, db_index=True)

    # turno opcional para permitir supervisor y evitar errores
    turno = models.CharField(
        max_length=2,
        choices=TURNOS,
        db_index=True,
        blank=True,
        null=True
    )

    # ------------------ CONTROL --------------#
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-fecha_creacion"]
        indexes = [
            models.Index(fields=["fecha_creacion"]),
            models.Index(fields=["tipo_trabajo"]),
            models.Index(fields=["torre"]),
            models.Index(fields=["servicio"]),
            models.Index(fields=["estado"]),
            models.Index(fields=["turno"]),
        ]

    def __str__(self):
        return f"{self.fecha_creacion.date()} - {self.get_tipo_trabajo_display()} - {self.get_torre_display()}"


class SeguimientoFracttal(models.Model):
    evento = models.ForeignKey(
        Evento,
        on_delete=models.CASCADE,
        related_name="seguimientos_fracttal",
        verbose_name="Evento asociado",
    )
    restriccion = models.CharField("Restricción", max_length=255)
    encargado_area = models.CharField("Encargado del área", max_length=120, blank=True)
    detalle = models.TextField("Detalle", blank=True)

    creado_por = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="seguimientos_fracttal_creados",
        verbose_name="Registrado por",
    )

    fecha_creacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Seguimiento Fracttal"
        verbose_name_plural = "Seguimientos Fracttal"
        ordering = ["-fecha_creacion"]
        indexes = [
            models.Index(fields=["fecha_creacion"]),
        ]

    def __str__(self):
        numero = self.evento.numero_orden or "Sin OT"
        return f"{numero} - {self.fecha_creacion:%d/%m/%Y %H:%M}"