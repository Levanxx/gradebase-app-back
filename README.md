# 🎓 Implementación de una Plataforma Web para la Gestión Académica — **GradeBase**

![Python](https://img.shields.io/badge/python-3776AB.svg?style=for-the-badge&logo=python&logoColor=white)
![Django](https://img.shields.io/badge/django-092E20.svg?style=for-the-badge&logo=django&logoColor=white)
![DRF](https://img.shields.io/badge/Django%20REST%20Framework-FF1709?style=for-the-badge&logo=django&logoColor=white)
![SQLite](https://img.shields.io/badge/sqlite-003B57.svg?style=for-the-badge&logo=sqlite&logoColor=white)
![Swagger](https://img.shields.io/badge/Swagger-85EA2D.svg?style=for-the-badge&logo=swagger&logoColor=black)
![Pandas](https://img.shields.io/badge/pandas-150458.svg?style=for-the-badge&logo=pandas&logoColor=white)
![NumPy](https://img.shields.io/badge/numpy-013243.svg?style=for-the-badge&logo=numpy&logoColor=white)
![Angular](https://img.shields.io/badge/angular-DD0031.svg?style=for-the-badge&logo=angular&logoColor=white)

---

##  Descripción general del proyecto  

**GradeBase** es un sistema web académico que permite **gestionar cursos, secciones, estudiantes y notas** de forma eficiente y automatizada.  
Está construido sobre **Django REST Framework**, y utiliza **Machine Learning** para proyectar el rendimiento académico de los estudiantes y detectar el riesgo de desaprobación.  

El proyecto busca **modernizar la gestión educativa**, optimizar la carga de notas y ofrecer herramientas inteligentes a docentes y alumnos.  
Incluye exportaciones en **CSV, XLSX y PDF**, junto con documentación API dinámica mediante **Swagger/OpenAPI**. 🚀  

---

## :mag_right: Tecnologías Usadas  

### **Backend**
- Django 5  
- Django REST Framework  
- SimpleJWT (autenticación por tokens)  
- drf-spectacular (OpenAPI Docs)  
- Pandas / NumPy / scikit-learn (Machine Learning)
- django-filter / CORS Headers  

### **Frontend**
- Angular (proyecto complementario para el consumo del API)

### **Base de Datos**
- SQLite (modo desarrollo)  
- PostgreSQL (planeado para producción)

---

##  Instalación del proyecto  

> [!NOTE]
> ###  Instalación Local  
>  
> 1. Clona este repositorio:  
>    ```bash
>    git clone https://github.com/Levanxx/gradebase-app-back.git
>    cd gradebase-app-back
>    ```
>  
> 2. Crea y activa un entorno virtual:  
>    ```bash
>    python -m venv venv
>    source venv/Scripts/activate  # (Windows)
>    source venv/bin/activate      # (Linux/macOS)
>    ```
>  
> 3. Instala dependencias:  
>    ```bash
>    pip install -r requirements.txt
>    ```
>  
> 4. Ejecuta migraciones:  
>    ```bash
>    python manage.py migrate
>    ```
>  
> 5. Crea un superusuario:  
>    ```bash
>    python manage.py createsuperuser
>    ```
>  
> 6. Inicia el servidor:  
>    ```bash
>    python manage.py runserver
>    ```
>  
> 7. Accede al sistema:  
>    👉 [http://127.0.0.1:8000](http://127.0.0.1:8000)  
>    📘 Documentación: [http://127.0.0.1:8000/api/schema/swagger-ui/](http://127.0.0.1:8000/api/schema/swagger-ui/)

---

##  Arquitectura General  

**Estructura del proyecto GradeBase Backend:**

GradeBase Backend  
│  
├── **config/** → Configuración global de Django  
│ ├── settings.py  
│ └── urls.py  
│  
├── **core/** → Aplicación principal  
│ ├── models.py → Modelos de datos  
│ ├── serializers.py → Serialización de datos  
│ ├── views.py → Lógica de la API  
│ ├── permissions.py → Roles y permisos  
│ ├── ml.py → Algoritmos ML (regresión y clasificación)  
│ ├── admin.py → Registro en el panel admin  
│ ├── **management/** → Comandos personalizados  
│ │ ├── cargar_demo_prueba.py  
│ │ ├── importar_estudiantes_excel.py  
│ │ └── proyectar_notas.py  
│ └── **migrations/** → Migraciones de base de datos  
│  
├── **templates/reports/** → Plantillas HTML para reportes PDF  
├── **requirements.txt** → Dependencias del proyecto  
└── **README.md** → Este archivo   

---

## 👥 Roles y Responsabilidades del Equipo  

| ID  | Rol | Integrante | Responsabilidades |
|-----|-----|-------------|-------------------|
| R1  | **Backend Developer / ML Engineer** | **Levanxx** | Arquitectura, lógica de negocio, modelos ML y configuración de API. |
| R2  | **API Developer / Documentation Lead** | **JhoanAronith** | Endpoints DRF, exportaciones, documentación Swagger y testing de endpoints. |

---

## 📋 Requerimientos Funcionales  

| ID | Descripción |
|----|--------------|
| RF01 | CRUD de estudiantes, cursos, secciones y notas. |
| RF02 | Autenticación y permisos por rol (admin, docente, estudiante). |
| RF03 | Visualización de notas y exportación a PDF/XLSX/CSV. |
| RF04 | API REST documentada con OpenAPI/Swagger. |
| RF05 | Proyección de notas con regresión lineal. |
| RF06 | Detección de riesgo académico con clasificación. |

---

## ⚙️ Requerimientos No Funcionales  

| ID | Descripción |
|----|--------------|
| RNF01 | Interfaz limpia y responsive (Angular). |
| RNF02 | API escalable, segura y modular. |
| RNF03 | Cumplimiento de convenciones RESTful. |
| RNF04 | Validaciones robustas y mensajes de error claros. |
| RNF05 | Código documentado y estructurado bajo buenas prácticas. |

---

## 📈 Flujo de trabajo en Git  

> [!TIP]
> ### 🔹 Flujo de commits atómicos y colaborativos
>  
> 1. Crear branch por funcionalidad:  
>    ```bash
>    git checkout -b feat/ml-module
>    ```
>  
> 2. Commits atómicos (Conventional Commits):  
>    ```bash
>    git commit -m "feat(api): agregar endpoint de proyección de nota"
>    git commit -m "fix(export): corregir error en PDF"
>    ```
>  
> 3. Push al remoto:  
>    ```bash
>    git push origin feat/ml-module
>    ```
>  
> 4. Merge por PR en GitHub (revisión mutua Levanxx ⇄ JhoanAronith).

---

## 📊 Endpoints principales  

| Método | Endpoint | Descripción |
|---------|-----------|-------------|
| POST | `/api/login/` | Autenticación JWT |
| GET | `/api/estudiantes/` | Lista de estudiantes |
| GET | `/api/notas/export/pdf/` | Exporta notas a PDF |
| POST | `/api/notas/ml/proyeccion/` | Predice nota final |
| POST | `/api/notas/ml/riesgo/` | Determina riesgo académico |

---

## 🧪 Machine Learning Integrado  

| Modelo | Tipo | Descripción |
|---------|------|-------------|
| Regresión lineal | `LinearRegression` | Predice nota final del estudiante |
| Clasificación | `RandomForestClassifier` | Detecta riesgo de desaprobar |

> 🔬 Los modelos se entrenan con datos históricos de notas, ponderaciones y métricas de rendimiento académico.

---

## 🏆 Commits y Convenciones  

| Tipo | Significado |
|------|--------------|
| `feat:` | Nueva funcionalidad |
| `fix:` | Corrección de errores |
| `docs:` | Documentación |
| `chore:` | Mantenimiento y configuración |
| `refactor:` | Mejora del código sin alterar la lógica |

> Cada commit cuenta una parte de la historia de **GradeBase**: limpio, descriptivo y profesional. 💪

---

## 💡 Próximas Mejoras  

- [ ] Migración a PostgreSQL  
- [ ] Dashboard docente con visualización estadística  
- [ ] Despliegue en Railway/Render  
- [ ] Sistema de alertas automáticas para riesgo alto  

---

## 🛡️ Licencia  

Este proyecto se distribuye bajo **MIT License** — libre para aprender, adaptar y mejorar.

---

> _“Educar con datos, aprender con inteligencia.  
> GradeBase: tu base para crecer.”_ 📘
