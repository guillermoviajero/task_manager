from datetime import date, timedelta
from django.core.management.base import BaseCommand
from tasks.models import Categoria, Tarea


class Command(BaseCommand):
    help = "Puebla la base de datos SQLite con categorías y tareas de ejemplo para pruebas de interfaz."

    def handle(self, *args, **options):
        self.stdout.write(self.style.NOTICE("Iniciando inserción de datos semilla en SQLite..."))

        # 1. Crear 3 Categorías
        cat_trabajo, _ = Categoria.objects.get_or_create(
            nombre="Trabajo",
            defaults={"color": "#ef4444"}
        )
        cat_estudio, _ = Categoria.objects.get_or_create(
            nombre="Estudio",
            defaults={"color": "#3b82f6"}
        )
        cat_personal, _ = Categoria.objects.get_or_create(
            nombre="Personal",
            defaults={"color": "#10b981"}
        )

        self.stdout.write(self.style.SUCCESS("✓ 3 Categorías creadas/verificadas: Trabajo, Estudio, Personal"))

        # Fechas de referencia relativas
        hoy = date.today()

        # 2. Definir 8 Tareas de ejemplo
        tareas_data = [
            {
                "titulo": "Configurar entorno Django con SQLite y python-dotenv",
                "descripcion": "Estructurar variables de entorno y excluir db.sqlite3 y .env en gitignore.",
                "categoria": cat_estudio,
                "prioridad": Tarea.Prioridad.ALTA,
                "completada": True,
                "fecha_limite": hoy - timedelta(days=2),
            },
            {
                "titulo": "Diseñar modelos de datos Categoria y Tarea con POO",
                "descripcion": "Establecer claves foráneas con on_delete=SET_NULL, Meta con ordenación y métodos __str__.",
                "categoria": cat_estudio,
                "prioridad": Tarea.Prioridad.ALTA,
                "completada": True,
                "fecha_limite": hoy - timedelta(days=1),
            },
            {
                "titulo": "Optimizar consulta de tareas con select_related",
                "descripcion": "Evitar el problema de N+1 queries al renderizar las categorías asociadas en la plantilla.",
                "categoria": cat_trabajo,
                "prioridad": Tarea.Prioridad.ALTA,
                "completada": False,
                "fecha_limite": hoy + timedelta(days=1),
            },
            {
                "titulo": "Revisar logs y depuración del endpoint de toggle de estado",
                "descripcion": "Comprobar que el marcado rápido mediante POST responda ágilmente con mensajes flash.",
                "categoria": cat_trabajo,
                "prioridad": Tarea.Prioridad.MEDIA,
                "completada": False,
                "fecha_limite": hoy + timedelta(days=3),
            },
            {
                "titulo": "Preparar presentación de sprint sobre Vibe Coding y Django",
                "descripcion": "Elaborar diapositivas resumiendo la evolución del proyecto y buenas prácticas de desarrollo.",
                "categoria": cat_trabajo,
                "prioridad": Tarea.Prioridad.MEDIA,
                "completada": False,
                "fecha_limite": hoy + timedelta(days=5),
            },
            {
                "titulo": "Comprar libro de patrones de diseño en Python",
                "descripcion": "Revisar edición actualizada sobre patrones creacionales y estructurales.",
                "categoria": cat_personal,
                "prioridad": Tarea.Prioridad.BAJA,
                "completada": False,
                "fecha_limite": hoy + timedelta(days=7),
            },
            {
                "titulo": "Completar sesión de entrenamiento funcional",
                "descripcion": "45 minutos de ejercicios de fuerza y movilidad articular.",
                "categoria": cat_personal,
                "prioridad": Tarea.Prioridad.MEDIA,
                "completada": True,
                "fecha_limite": hoy,
            },
            {
                "titulo": "Planificar itinerario de viaje de senderismo",
                "descripcion": "Revisar rutas de montaña, mapa topográfico y previsión meteorológica.",
                "categoria": cat_personal,
                "prioridad": Tarea.Prioridad.BAJA,
                "completada": False,
                "fecha_limite": hoy + timedelta(days=14),
            },
        ]

        creadas_count = 0
        for data in tareas_data:
            tarea, creada = Tarea.objects.get_or_create(
                titulo=data["titulo"],
                defaults={
                    "descripcion": data["descripcion"],
                    "categoria": data["categoria"],
                    "prioridad": data["prioridad"],
                    "completada": data["completada"],
                    "fecha_limite": data["fecha_limite"],
                }
            )
            if creada:
                creadas_count += 1

        self.stdout.write(self.style.SUCCESS(f"✓ {creadas_count} tareas nuevas insertadas ({len(tareas_data)} totales en catálogo)."))
        self.stdout.write(self.style.SUCCESS("Población de datos finalizada con éxito en SQLite."))
