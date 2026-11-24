from django.urls import path
from . import views

app_name = "tasks"

urlpatterns = [
    path("", views.lista_tareas, name="lista_tareas"),
    path("crear/", views.crear_tarea, name="crear_tarea"),
    path("<int:pk>/editar/", views.editar_tarea, name="editar_tarea"),
    path("<int:pk>/eliminar/", views.eliminar_tarea, name="eliminar_tarea"),
    path("<int:pk>/toggle/", views.toggle_tarea, name="toggle_tarea"),
]
