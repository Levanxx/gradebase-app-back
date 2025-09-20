from django.core.management.base import BaseCommand
from django.contrib.auth.models import User, Group
from core.models import Curso, Seccion, Estudiante, Nota


class Command(BaseCommand):
    help = "Crea datos mínimos de prueba: 1 curso, 1 sección, 1 docente, 5 estudiantes y 1 nota por estudiante."

    def handle(self, *args, **kwargs):
        # --- Grupos ---
        g_doc, _ = Group.objects.get_or_create(name="DOCENTE")
        g_est, _ = Group.objects.get_or_create(name="ESTUDIANTE")

        # --- Docente ---
        docente, created = User.objects.get_or_create(
            username="profe1", defaults={"email": "profe1@x.com"}
        )
        if created:
            docente.set_password("profe1")
            docente.save()
        docente.groups.add(g_doc)

        # --- Curso ---
        curso, _ = Curso.objects.get_or_create(
            codigo="CS101", defaults={"nombre": "Algoritmos"}
        )

        # --- Sección (lookup solo por curso+nombre; profesor en defaults) ---
        seccion, created_sec = Seccion.objects.get_or_create(
            curso=curso,
            nombre="A",
            defaults={"profesor": docente},
        )
        # Si existía con otro profesor, lo ajustamos para la demo
        if not created_sec and seccion.profesor_id != docente.id:
            seccion.profesor = docente
            seccion.save(update_fields=["profesor"])

        # --- Estudiantes (5) ---
        estudiantes = []
        for i in range(1, 6):
            u, u_created = User.objects.get_or_create(
                username=f"alumno{i}", defaults={"email": f"alumno{i}@x.com"}
            )
            if u_created:
                u.set_password(f"alumno{i}")
                u.save()
            u.groups.add(g_est)

            e, _ = Estudiante.objects.get_or_create(
                user=u,
                defaults={
                    "codigo": f"STU10{i}",
                    "nombre": f"Nombre{i}",
                    "apellido": f"Apellido{i}",
                    "email": u.email,
                },
            )
            estudiantes.append(e)

        # --- 1 Nota por estudiante (update_or_create para poder re-ejecutar el comando) ---
        created_count = 0
        updated_count = 0
        for idx, e in enumerate(estudiantes, start=1):
            # valores simples y reproducibles
            av1 = 11 + (idx % 3)  # 12..14
            av2 = 12 + (idx % 3)  # 13..15
            av3 = 13 + (idx % 3)  # 14..16
            part = 15
            proj = 16
            final = round((av1 + av2 + av3 + part + proj) / 5)

            nota, created = Nota.objects.update_or_create(
                estudiante=e,
                seccion=seccion,
                defaults={
                    "avance1": av1,
                    "avance2": av2,
                    "avance3": av3,
                    "participacion": part,
                    "proyecto_final": proj,
                    "nota_final": final,
                },
            )
            if created:
                created_count += 1
            else:
                updated_count += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"OK: CS101/A con docente=profe1/profe1. Estudiantes: {len(estudiantes)}. "
                f"Notas creadas: {created_count}, actualizadas: {updated_count}."
            )
        )
