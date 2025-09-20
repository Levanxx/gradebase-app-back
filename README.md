Documentación del Proyecto GradeBase
1. Descripción General

GradeBase es un sistema de gestión de cursos, secciones, estudiantes y notas, con funcionalidades de exportación (CSV/XLSX/PDF) y Machine Learning (proyección de notas y predicción de riesgo de desaprobación).

Arquitectura:

Backend: Django + Django REST Framework (DRF).

Base de Datos: SQLite (en desarrollo).

Autenticación: JWT (SimpleJWT).

Frontend: Angular 16+ (standalone API, zone.js).

2. Funcionalidades Implementadas
 Backend (Django + DRF)

Modelos:

Estudiante: vinculado a User, con código único, nombre, apellido, email.

Curso: código y nombre.

Seccion: pertenece a un curso, tiene nombre y profesor (usuario docente).

Nota: pertenece a un estudiante y sección; almacena notas parciales y finales.

Restricciones: unique_together para estudiante+sección (no duplicados).

Timestamps: created_at, updated_at.

Admin:

Modelos registrados (Estudiante, Curso, Sección, Nota).

Superusuario creado.

Grupos: docente, estudiante.

API REST:

CRUD para Estudiante, Curso, Sección y Nota.

Autenticación JWT (/api/token/, /api/token/refresh/).

Permisos:

Estudiante: solo puede ver sus propias notas.

Docente: puede editar notas de sus secciones.

Admin: acceso total.

Exportaciones:

CSV → /api/notas/export/csv/

XLSX → /api/notas/export/xlsx/

PDF → /api/notas/export/pdf/

Filtros por curso, sección y estudiante.

Filtros y paginación:

Integrado django-filter.

Paginación: 20 resultados por página.

Machine Learning (ML):

Endpoint /api/notas/ml/proyeccion: predice nota final (regresión).

Endpoint /api/notas/ml/riesgo: calcula probabilidad de desaprobar (clasificación).

Implementado con scikit-learn.

Comandos de gestión:

cargar_demo_prueba: crea curso demo (CS101), sección A, 1 docente (profe1), 5 alumnos (alumno1..5) y notas de prueba.

limpiar_demo_prueba: elimina los datos anteriores (sin tocar grupos ni otros cursos).

 Sirve para reiniciar el entorno de demo rápido.


3. Requisitos Técnicos

Backend:

Python 3.12+

Django 5.2.5

DRF 3.16.1

SimpleJWT

Pandas, Numpy, Scikit-learn, OpenPyXL

Frontend:

Node.js 20+

Angular 16+

zone.js

Standalone components (sin NgModules).

4. Flujo de Uso (Demo)

Backend:

Levantar:

cd GradeBase
.\venv\Scripts\activate
python manage.py runserver


Cargar datos demo:

python manage.py cargar_demo_prueba
