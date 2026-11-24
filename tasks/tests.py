from datetime import date
from django.test import TestCase, Client
from django.urls import reverse
from .models import Categoria, Tarea
from .forms import TareaForm


class TareaModelAndFormTests(TestCase):
    """
    Pruebas unitarias de modelos y formularios siguiendo buenas prácticas de POO.
    """
    def setUp(self):
        self.categoria = Categoria.objects.create(nombre="Desarrollo", color="#6366f1")

    def test_creacion_categoria_y_str(self):
        self.assertEqual(str(self.categoria), "Desarrollo")
        self.assertEqual(self.categoria.color, "#6366f1")

    def test_creacion_tarea_con_valores_por_defecto(self):
        tarea = Tarea.objects.create(
            titulo="Aprender Django ORM",
            categoria=self.categoria
        )
        self.assertFalse(tarea.completada)
        self.assertEqual(tarea.prioridad, Tarea.Prioridad.MEDIA)
        self.assertEqual(str(tarea), "[✗] Aprender Django ORM (Media)")

    def test_validacion_formulario_titulo_minimo_3_caracteres(self):
        # Título inválido (menos de 3 caracteres)
        form_invalido = TareaForm(data={
            "titulo": "ab",
            "prioridad": Tarea.Prioridad.MEDIA,
        })
        self.assertFalse(form_invalido.is_valid())
        self.assertIn("titulo", form_invalido.errors)

        # Título válido
        form_valido = TareaForm(data={
            "titulo": "Crear proyecto Django",
            "prioridad": Tarea.Prioridad.ALTA,
        })
        self.assertTrue(form_valido.is_valid())


class TareaViewsAndFilterTests(TestCase):
    """
    Pruebas unitarias para verificar el filtrado por estado, prioridad y optimización.
    """
    def setUp(self):
        self.client = Client()
        self.cat_backend = Categoria.objects.create(nombre="Backend", color="#10b981")
        self.cat_frontend = Categoria.objects.create(nombre="Frontend", color="#3b82f6")

        # Crear tareas con diferentes estados y prioridades
        self.tarea_pendiente_1 = Tarea.objects.create(
            titulo="Configurar Base de Datos SQLite",
            completada=False,
            prioridad=Tarea.Prioridad.ALTA,
            categoria=self.cat_backend,
            fecha_limite=date.today()
        )
        self.tarea_pendiente_2 = Tarea.objects.create(
            titulo="Escribir componentes Tailwind",
            completada=False,
            prioridad=Tarea.Prioridad.BAJA,
            categoria=self.cat_frontend
        )
        self.tarea_completada = Tarea.objects.create(
            titulo="Instalar dependencias",
            completada=True,
            prioridad=Tarea.Prioridad.MEDIA,
            categoria=self.cat_backend
        )

    def test_vista_lista_todas_las_tareas(self):
        response = self.client.get(reverse("tasks:lista_tareas"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "tasks/lista_tareas.html")
        self.assertEqual(len(response.context["tareas"]), 3)

    def test_filtrado_por_estado_pendientes(self):
        response = self.client.get(reverse("tasks:lista_tareas") + "?estado=pendientes")
        self.assertEqual(response.status_code, 200)
        tareas = list(response.context["tareas"])
        self.assertEqual(len(tareas), 2)
        for t in tareas:
            self.assertFalse(t.completada)

    def test_filtrado_por_estado_completadas(self):
        response = self.client.get(reverse("tasks:lista_tareas") + "?estado=completadas")
        self.assertEqual(response.status_code, 200)
        tareas = list(response.context["tareas"])
        self.assertEqual(len(tareas), 1)
        self.assertTrue(tareas[0].completada)
        self.assertEqual(tareas[0].titulo, "Instalar dependencias")

    def test_filtrado_por_prioridad(self):
        response = self.client.get(reverse("tasks:lista_tareas") + "?prioridad=Alta")
        self.assertEqual(response.status_code, 200)
        tareas = list(response.context["tareas"])
        self.assertEqual(len(tareas), 1)
        self.assertEqual(tareas[0].prioridad, Tarea.Prioridad.ALTA)

    def test_filtrado_por_categoria(self):
        response = self.client.get(reverse("tasks:lista_tareas") + f"?categoria={self.cat_frontend.id}")
        self.assertEqual(response.status_code, 200)
        tareas = list(response.context["tareas"])
        self.assertEqual(len(tareas), 1)
        self.assertEqual(tareas[0].categoria, self.cat_frontend)


class TareaToggleAndCRUDTests(TestCase):
    """
    Pruebas unitarias para alternar estado (toggle) y operaciones CRUD.
    """
    def setUp(self):
        self.client = Client()
        self.tarea = Tarea.objects.create(
            titulo="Tarea de prueba para toggle",
            completada=False,
            prioridad=Tarea.Prioridad.MEDIA
        )

    def test_toggle_de_pendiente_a_completada_y_viceversa(self):
        # 1. Cambiar de pendiente (False) a completada (True)
        url = reverse("tasks:toggle_tarea", kwargs={"pk": self.tarea.pk})
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)  # Redirección esperada
        self.tarea.refresh_from_db()
        self.assertTrue(self.tarea.completada)

        # 2. Cambiar de completada (True) a pendiente (False)
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)
        self.tarea.refresh_from_db()
        self.assertFalse(self.tarea.completada)

    def test_toggle_rechaza_metodo_get(self):
        url = reverse("tasks:toggle_tarea", kwargs={"pk": self.tarea.pk})
        response = self.client.get(url)
        # @require_POST debe retornar 405 Method Not Allowed ante peticiones GET
        self.assertEqual(response.status_code, 405)

    def test_crear_tarea_via_post(self):
        url = reverse("tasks:crear_tarea")
        response = self.client.post(url, {
            "titulo": "Nueva tarea desde formulario",
            "descripcion": "Descripción detallada",
            "prioridad": Tarea.Prioridad.ALTA,
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Tarea.objects.filter(titulo="Nueva tarea desde formulario").exists())

    def test_eliminar_tarea_via_post(self):
        url = reverse("tasks:eliminar_tarea", kwargs={"pk": self.tarea.pk})
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Tarea.objects.filter(pk=self.tarea.pk).exists())
