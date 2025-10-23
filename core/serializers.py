from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Estudiante, Curso, Seccion, Nota

class EstudianteSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()

    class Meta:
        model = Estudiante
        fields = ['id', 'codigo', 'nombre', 'apellido', 'email', 'user',
                  'full_name', 'creado', 'actualizado']

    def get_full_name(self, obj):
        return f"{obj.apellido}, {obj.nombre}"


class CursoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Curso
        fields = ['id', 'codigo', 'nombre', 'creado', 'actualizado']


class SeccionSerializer(serializers.ModelSerializer):
    # <<< estos dos campos sirven para que el front pinte 'FS - A'
    curso_codigo = serializers.CharField(source='curso.codigo', read_only=True)
    curso_nombre = serializers.CharField(source='curso.nombre', read_only=True)

    class Meta:
        model = Seccion
        fields = ['id', 'nombre', 'curso', 'curso_codigo', 'curso_nombre',
                  'creado', 'actualizado']


class NotaSerializer(serializers.ModelSerializer):
    # campos de solo lectura para pintar la tabla de manera amigable
    estudiante_codigo = serializers.CharField(source='estudiante.codigo', read_only=True)
    estudiante_nombre = serializers.SerializerMethodField()
    seccion_nombre = serializers.CharField(source='seccion.nombre', read_only=True)
    curso_codigo = serializers.CharField(source='seccion.curso.codigo', read_only=True)

    class Meta:
        model = Nota
        fields = [
            'id',
            'avance1', 'avance2', 'avance3',
            'participacion', 'proyecto_final', 'nota_final',
            'estudiante', 'seccion',
            # solo lectura
            'estudiante_codigo', 'estudiante_nombre',
            'seccion_nombre', 'curso_codigo',
            'creado', 'actualizado'
        ]

    def get_estudiante_nombre(self, obj):
        return f"{obj.estudiante.apellido}, {obj.estudiante.nombre}"


# -------- Registro de DOCENTE (para /api/auth/register/) --------
class RegisterDocenteSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True, min_length=6)
    email = serializers.EmailField(required=False, allow_blank=True, allow_null=True)
    nombre = serializers.CharField()
    apellido = serializers.CharField()

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("El usuario ya existe.")
        return value
