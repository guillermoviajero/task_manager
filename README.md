# 📋 Django Task Manager

Aplicación web para la gestión eficiente de tareas y proyectos desarrollada con **Django 5** y **SQLite**, aplicando buenas prácticas de desarrollo web, arquitectura Modelo-Vista-Template (MVT) y principios de Clean Code.

---

## ✨ Características Principales

- **Gestión Integral de Tareas (CRUD)**: Creación, lectura, actualización y eliminación de tareas con confirmación interactiva.
- **Categorización y Etiquetas Visuales**: Clasificación por categorías con códigos de color personalizables.
- **Priorización y Estados**: Clasificación por prioridad (*Baja*, *Media*, *Alta*) y marcado rápido de estado (*Pendiente* / *Completada*).
- **Filtrado Avanzado**: Filtrado instantáneo por estado de completitud, prioridad y categoría asignada.
- **Consultas Optimizadas**: Implementación de `select_related` para evitar el problema de consultas $N+1$ en base de datos.
- **Comando de Población de Datos**: Incluye el comando personalizado `python manage.py poblar_tareas` para generar datos de prueba realistas.
- **Seguridad y Variables de Entorno**: Configuración desacoplada con `python-dotenv` y plantilla `.env.example`.

---

## 🛠️ Tecnologías y Librerías

- **Python 3.10+**
- **Django 5.x**
- **python-dotenv**
- **SQLite**
- **HTML5 & CSS / Componentes visuales**

---

## 🚀 Puesta en Marcha en Local

### 1. Clonar el repositorio
```bash
git clone https://github.com/guillermoviajero/task_manager.git
cd task_manager
```

### 2. Crear y activar el entorno virtual
```bash
# Windows
python -m venv .venv
.venv\Scripts\activate

# Linux / macOS
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 4. Configurar variables de entorno
Copia el archivo de ejemplo `.env.example` y renómbralo a `.env`:
```bash
cp .env.example .env
```
*(En Windows PowerShell: `Copy-Item .env.example .env`)*

### 5. Aplicar migraciones
```bash
python manage.py migrate
```

### 6. (Opcional) Cargar datos de prueba iniciales
```bash
python manage.py poblar_tareas
```

### 7. Iniciar el servidor de desarrollo
```bash
python manage.py runserver
```
Abre tu navegador en [http://127.0.0.1:8000/](http://127.0.0.1:8000/) para explorar la aplicación.

---

## 📁 Estructura del Proyecto

```text
task_manager/
│
├── manage.py                   # Script de gestión de Django
├── requirements.txt            # Dependencias del proyecto
├── .env.example                # Plantilla de variables de entorno
├── .gitignore                  # Exclusión de archivos sensibles y temporales
├── README.md                   # Documentación del proyecto
│
├── task_manager/               # Configuración central del proyecto Django
│   ├── settings.py             # Configuración con soporte para .env
│   ├── urls.py                 # Enrutamiento raíz
│   ├── asgi.py
│   └── wsgi.py
│
└── tasks/                      # Aplicación principal de gestión de tareas
    ├── models.py               # Modelos Categoria y Tarea
    ├── views.py                # Lógica de controladores y filtros
    ├── forms.py                # Formularios Django
    ├── urls.py                 # Enrutamiento de la app tasks
    ├── admin.py                # Registro en panel de administración
    ├── templates/tasks/        # Plantillas HTML (MVT)
    └── management/commands/    # Comandos personalizados (poblar_tareas)
```

---

## 📄 Licencia

Este proyecto está bajo la Licencia MIT.
