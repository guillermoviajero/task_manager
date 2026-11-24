from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.views.decorators.http import require_POST
from .models import Tarea, Categoria
from .forms import TareaForm


def lista_tareas(request):
    """
    Lista las tareas optimizando la consulta a la base de datos con select_related('categoria')
    para evitar el problema de N+1 queries. Permite filtros por estado, prioridad y categoría.
    """
    # Consulta base optimizada con INNER/LEFT JOIN a Categoria
    tareas = Tarea.objects.select_related("categoria").all()

    # Filtros recibidos por GET
    estado = request.GET.get("estado", "todas").strip()
    prioridad = request.GET.get("prioridad", "").strip()
    categoria_id = request.GET.get("categoria", "").strip()

    # Aplicar filtro por estado de completada
    if estado == "pendientes":
        tareas = tareas.filter(completada=False)
    elif estado == "completadas":
        tareas = tareas.filter(completada=True)

    # Aplicar filtro por prioridad
    if prioridad in [choice[0] for choice in Tarea.Prioridad.choices]:
        tareas = tareas.filter(prioridad=prioridad)

    # Aplicar filtro por categoría
    if categoria_id.isdigit():
        tareas = tareas.filter(categoria_id=int(categoria_id))

    # Obtener todas las categorías para el selector de filtro
    categorias = Categoria.objects.all()

    # Contadores rápidos para métricas
    total_tareas = Tarea.objects.count()
    total_pendientes = Tarea.objects.filter(completada=False).count()
    total_completadas = Tarea.objects.filter(completada=True).count()

    contexto = {
        "tareas": tareas,
        "categorias": categorias,
        "estado_actual": estado,
        "prioridad_actual": prioridad,
        "categoria_actual": categoria_id,
        "prioridades": Tarea.Prioridad.choices,
        "total_tareas": total_tareas,
        "total_pendientes": total_pendientes,
        "total_completadas": total_completadas,
    }
    return render(request, "tasks/lista_tareas.html", contexto)


def crear_tarea(request):
    """
    Crea una nueva tarea utilizando TareaForm.
    """
    if request.method == "POST":
        form = TareaForm(request.POST)
        if form.is_valid():
            tarea = form.save()
            messages.success(request, f"¡Tarea '{tarea.titulo}' creada con éxito!")
            return redirect("tasks:lista_tareas")
        else:
            messages.error(request, "Por favor corrige los errores indicados en el formulario.")
    else:
        form = TareaForm()

    return render(request, "tasks/form_tarea.html", {
        "form": form,
        "titulo_pagina": "Crear Nueva Tarea",
        "accion": "Crear Tarea",
    })


def editar_tarea(request, pk):
    """
    Edita una tarea existente identificada por su clave primaria (pk).
    """
    tarea = get_object_or_404(Tarea, pk=pk)

    if request.method == "POST":
        form = TareaForm(request.POST, instance=tarea)
        if form.is_valid():
            form.save()
            messages.success(request, f"¡Tarea '{tarea.titulo}' actualizada correctamente!")
            return redirect("tasks:lista_tareas")
        else:
            messages.error(request, "Por favor corrige los errores del formulario.")
    else:
        form = TareaForm(instance=tarea)

    return render(request, "tasks/form_tarea.html", {
        "form": form,
        "tarea": tarea,
        "titulo_pagina": f"Editar: {tarea.titulo}",
        "accion": "Guardar Cambios",
    })


def eliminar_tarea(request, pk):
    """
    Elimina una tarea existente tras confirmación mediante POST o vista modal.
    """
    tarea = get_object_or_404(Tarea, pk=pk)
    if request.method == "POST":
        titulo = tarea.titulo
        tarea.delete()
        messages.warning(request, f"La tarea '{titulo}' ha sido eliminada.")
        return redirect("tasks:lista_tareas")

    return render(request, "tasks/confirmar_eliminar.html", {"tarea": tarea})


@require_POST
def toggle_tarea(request, pk):
    """
    Vista rápida para alternar el estado 'completada' de una tarea con un solo clic.
    Redirige al listado preservando una experiencia fluida.
    """
    tarea = get_object_or_404(Tarea, pk=pk)
    tarea.completada = not tarea.completada
    tarea.save(update_fields=["completada"])

    if tarea.completada:
        messages.success(request, f"¡Completada: '{tarea.titulo}'!")
    else:
        messages.info(request, f"Marcada como pendiente: '{tarea.titulo}'.")

    # Si hay referer en la petición, vuelve a la misma página/filtros
    referer = request.META.get("HTTP_REFERER")
    if referer:
        return redirect(referer)
    return redirect("tasks:lista_tareas")
