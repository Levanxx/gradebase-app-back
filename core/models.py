from django.db import models
from django.contrib.auth.models import User


class TimeStampedModel(models.Model):
    """Base con marcas de tiempo."""
    creado = models.DateTimeField(auto_now_add=True)
    actualizado = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Estudiante(TimeStampedModel):
    """
    Estudiante de la institución.
    Si el alumno inicia sesión, se puede enlazar con un usuario de Django.
    """
    user = models.ForeignKey(
        User, null=True, blank=True, on_delete=models.SET_NULL, related_name="estudiantes"
    )
    codigo = models.CharField(max_length=20, unique=True)
    nombre = models.CharField(max_length=150)
    apellido = models.CharField(max_length=150)
    email = models.EmailField(unique=True, null=True, blank=True)

    class Meta:
        ordering = ["apellido", "nombre", "codigo"]

    def __str__(self) -> str:
        return f"{self.codigo} - {self.apellido}, {self.nombre}"


class Curso(TimeStampedModel):
    """Catálogo de cursos."""
    codigo = models.CharField(max_length=20, unique=True)  # p.ej. FS, BIGD, IA, ...
    nombre = models.CharField(max_length=200)

    class Meta:
        ordering = ["codigo"]

    def __str__(self) -> str:
        return f"{self.codigo} - {self.nombre}"


class Seccion(TimeStampedModel):
    """
    Sección de un curso (A, B, 01, etc.) dictada por un profesor (usuario Django).
    """
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE, related_name="secciones")
    nombre = models.CharField(max_length=50)  # p.ej. "A"
    profesor = models.ForeignKey(
        User, null=True, blank=True, on_delete=models.SET_NULL, related_name="secciones_dictadas"
    )

    class Meta:
        ordering = ["curso__codigo", "nombre"]
        unique_together = ("curso", "nombre")  # una sección por curso

    def __str__(self) -> str:
        prof = f" - {self.profesor.username}" if self.profesor_id else ""
        return f"{self.curso.codigo} - {self.nombre}{prof}"


class Nota(TimeStampedModel):
    """
    Registro de notas por estudiante y sección.
    Los campos numéricos tienen default=0 para evitar NULL en BD
    (así el frontend siempre ve números y no celdas vacías).
    """
    estudiante = models.ForeignKey(Estudiante, on_delete=models.CASCADE, related_name="notas")
    seccion = models.ForeignKey(Seccion, on_delete=models.CASCADE, related_name="notas")

    avance1 = models.FloatField(default=0, null=False, blank=True)
    avance2 = models.FloatField(default=0, null=False, blank=True)
    avance3 = models.FloatField(default=0, null=False, blank=True)
    participacion = models.FloatField(default=0, null=False, blank=True)
    proyecto_final = models.FloatField(default=0, null=False, blank=True)
    nota_final = models.FloatField(default=0, null=False, blank=True)

    class Meta:
        ordering = ["seccion__curso__codigo", "seccion__nombre", "estudiante__apellido", "estudiante__nombre"]
        unique_together = ("estudiante", "seccion")  # una fila por alumno en la sección
        indexes = [
            models.Index(fields=["seccion"]),
            models.Index(fields=["estudiante"]),
        ]

    def __str__(self) -> str:
        return f"Nota({self.estudiante.codigo} @ {self.seccion.curso.codigo}-{self.seccion.nombre})"

    @property
    def curso_codigo(self) -> str:
        return self.seccion.curso.codigo

    @property
    def seccion_nombre(self) -> str:
        return self.seccion.nombre
