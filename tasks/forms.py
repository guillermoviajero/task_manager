from django import forms
from .models import Tarea, Categoria


class TareaForm(forms.ModelForm):
    """
    Formulario vinculado al modelo Tarea con validaciones de POO y estilos de Tailwind CSS.
    """
    class Meta:
        model = Tarea
        fields = ["titulo", "descripcion", "prioridad", "fecha_limite", "categoria"]
        labels = {
            "titulo": "Título de la tarea",
            "descripcion": "Descripción detallada",
            "prioridad": "Nivel de prioridad",
            "fecha_limite": "Fecha límite",
            "categoria": "Categoría asociada",
        }
        widgets = {
            "titulo": forms.TextInput(attrs={
                "class": "w-full rounded-lg border border-slate-300 px-4 py-2.5 text-slate-800 shadow-sm focus:border-indigo-500 focus:ring-2 focus:ring-indigo-200 outline-none transition",
                "placeholder": "Ej: Implementar autenticación con JWT",
            }),
            "descripcion": forms.Textarea(attrs={
                "class": "w-full rounded-lg border border-slate-300 px-4 py-2.5 text-slate-800 shadow-sm focus:border-indigo-500 focus:ring-2 focus:ring-indigo-200 outline-none transition",
                "rows": 4,
                "placeholder": "Añade notas, contexto o especificaciones de la tarea...",
            }),
            "prioridad": forms.Select(attrs={
                "class": "w-full rounded-lg border border-slate-300 px-4 py-2.5 text-slate-800 shadow-sm focus:border-indigo-500 focus:ring-2 focus:ring-indigo-200 outline-none transition bg-white",
            }),
            "fecha_limite": forms.DateInput(attrs={
                "type": "date",
                "class": "w-full rounded-lg border border-slate-300 px-4 py-2.5 text-slate-800 shadow-sm focus:border-indigo-500 focus:ring-2 focus:ring-indigo-200 outline-none transition bg-white",
            }),
            "categoria": forms.Select(attrs={
                "class": "w-full rounded-lg border border-slate-300 px-4 py-2.5 text-slate-800 shadow-sm focus:border-indigo-500 focus:ring-2 focus:ring-indigo-200 outline-none transition bg-white",
            }),
        }

    def clean_titulo(self):
        """
        Valida que el título tenga al menos 3 caracteres tras eliminar espacios en blanco.
        """
        titulo = self.cleaned_data.get("titulo", "").strip()
        if len(titulo) < 3:
            raise forms.ValidationError("El título debe contener al menos 3 caracteres.")
        return titulo
