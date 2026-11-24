from django.db import models


class Categoria(models.Model):
    """
    Modelo que representa una categoría o etiqueta para clasificar tareas.
    """
    nombre = models.CharField(
        max_length=50,
        unique=True,
        verbose_name="Nombre de la categoría"
    )
    color = models.CharField(
        max_length=7,
        default="#3b82f6",
        verbose_name="Color hexadecimal",
        help_text="Código hexadecimal para identificación visual (ej. #3b82f6)"
    )

    class Meta:
        verbose_name = "Categoría"
        verbose_name_plural = "Categorías"
        ordering = ["nombre"]

    def __str__(self):
        return self.nombre


class Tarea(models.Model):
    """
    Modelo representativo de una tarea dentro del gestor.
    Aplica principios de POO y desacoplamiento relacional.
    """
    class Prioridad(models.TextChoices):
        BAJA = "Baja", "Baja"
        MEDIA = "Media", "Media"
        ALTA = "Alta", "Alta"

    titulo = models.CharField(
        max_length=200,
        verbose_name="Título"
    )
    descripcion = models.TextField(
        blank=True,
        null=True,
        verbose_name="Descripción"
    )
    completada = models.BooleanField(
        default=False,
        verbose_name="¿Completada?"
    )
    prioridad = models.CharField(
        max_length=10,
        choices=Prioridad.choices,
        default=Prioridad.MEDIA,
        verbose_name="Prioridad"
    )
    fecha_limite = models.DateField(
        blank=True,
        null=True,
        verbose_name="Fecha límite"
    )
    creada_en = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Fecha de creación"
    )
    categoria = models.ForeignKey(
        Categoria,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="tareas",
        verbose_name="Categoría"
    )

    class Meta:
        verbose_name = "Tarea"
        verbose_name_plural = "Tareas"
        # Ordenación: pendientes primero (False < True) y fecha límite próxima
        ordering = ["completada", "fecha_limite", "-creada_en"]

    def __str__(self):
        estado = "✓" if self.completada else "✗"
        return f"[{estado}] {self.titulo} ({self.prioridad})"
