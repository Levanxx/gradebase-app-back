from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    EstudianteViewSet,
    CursoViewSet,
    SeccionViewSet,
    NotaViewSet,
    register_user,   # <- endpoint público de registro DOCENTE
)

router = DefaultRouter()
router.register(r"estudiantes", EstudianteViewSet, basename="estudiante")
router.register(r"cursos", CursoViewSet, basename="curso")
router.register(r"secciones", SeccionViewSet, basename="seccion")
router.register(r"notas", NotaViewSet, basename="nota")

urlpatterns = [
    path("", include(router.urls)),
    path("auth/register/", register_user, name="auth_register"),
]
