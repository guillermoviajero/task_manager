from django.contrib import admin
from .models import Categoria, Tarea


@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ("nombre", "color")
    search_fields = ("nombre",)
    ordering = ("nombre",)


@admin.register(Tarea)
class TareaAdmin(admin.ModelAdmin):
    list_display = ("titulo", "categoria", "prioridad", "completada", "fecha_limite", "creada_en")
    list_filter = ("completada", "prioridad", "categoria", "fecha_limite")
    search_fields = ("titulo", "descripcion")
    list_editable = ("completada",)
    date_hierarchy = "fecha_limite"
    ordering = ("completada", "fecha_limite")
