# core/management/commands/riesgo_desaprobacion.py
from __future__ import annotations

from django.core.management.base import BaseCommand, CommandError
from core.models import Seccion
from core.ml import predict_risk_for_seccion


class Command(BaseCommand):
    help = (
        "Calcula el riesgo de desaprobar para todos los estudiantes de una sección.\n\n"
        "Uso:\n"
        "  python manage.py riesgo_desaprobacion --seccion_id 12\n"
        "  python manage.py riesgo_desaprobacion --curso FS --seccion A\n"
    )

    def add_arguments(self, parser):
        # Permite identificar la sección por ID o por (curso, seccion)
        parser.add_argument(
            "--seccion_id",
            type=int,
            help="ID de la sección (alternativa a --curso y --seccion).",
        )
        parser.add_argument(
            "--curso",
            type=str,
            help="Código del curso (p.ej. FS, IA, BIGD). Requiere --seccion si no usas --seccion_id.",
        )
        parser.add_argument(
            "--seccion",
            type=str,
            help="Nombre de la sección (p.ej. A, B, 01). Requiere --curso si no usas --seccion_id.",
        )

    # ------------------------------- Helpers -------------------------------

    def _resolve_seccion(self, seccion_id: int | None, curso: str | None, seccion_nombre: str | None) -> Seccion:
        """
        Obtiene la Seccion ya sea por ID o por (curso.codigo, nombre).
        Lanza CommandError si no se encuentra o si faltan parámetros.
        """
        if seccion_id:
            try:
                return (
                    Seccion.objects.select_related("curso", "profesor")
                    .get(pk=seccion_id)
                )
            except Seccion.DoesNotExist:
                raise CommandError(f"Sección con id={seccion_id} no encontrada.")

        if curso and seccion_nombre:
            try:
                return (
                    Seccion.objects.select_related("curso", "profesor")
                    .get(curso__codigo=curso, nombre=seccion_nombre)
                )
            except Seccion.DoesNotExist:
                raise CommandError(
                    f"No se encontró la sección '{seccion_nombre}' del curso '{curso}'."
                )

        raise CommandError(
            "Debes especificar --seccion_id o el par --curso y --seccion."
        )

    # -------------------------------- Main ---------------------------------

    def handle(self, *args, **options):
        seccion_id = options.get("seccion_id")
        curso = options.get("curso")
        seccion_nombre = options.get("seccion")

        # Resolver la sección
        seccion = self._resolve_seccion(seccion_id, curso, seccion_nombre)

        # Ejecutar cálculo de riesgo
        try:
            out = predict_risk_for_seccion(seccion)
        except ValueError as e:
            # Errores típicos: no hay suficientes filas con nota_final > 0, o no hay diversidad de clases
            raise CommandError(str(e))
        except KeyError as e:
            raise CommandError(f"Salida inesperada del predictor. Falta clave: {e!s}")
        except Exception as e:
            raise CommandError(f"Error no controlado al calcular riesgo: {e}")

        metrics = out.get("metrics", {})
        n_train = metrics.get("n_train", 0)
        acc = metrics.get("accuracy", 0.0)
        version = metrics.get("version", "v1")

        header = (
            f"[{version}] Riesgo de desaprobación "
            f"para {seccion.curso.codigo} - {seccion.nombre} "
            f"(profesor: {seccion.profesor.username if seccion.profesor_id else '—'})"
        )
        self.stdout.write(self.style.MIGRATE_HEADING(header))

        self.stdout.write(
            self.style.SUCCESS(
                f"Entrenado con {n_train} filas válidas (nota_final > 0). "
                f"Accuracy={acc:.3f}"
            )
        )

        preds = out.get("predictions", [])
        if not preds:
            self.stdout.write("No hay predicciones para imprimir.")
            return

        # Imprimir tabla simple
        self.stdout.write("\nCódigo\t\tProb_Riesgo\tClase\tUmbral")
        self.stdout.write("-" * 56)
        for p in preds:
            codigo = p.get("codigo", "-")
            prob = p.get("risk_prob", 0.0)
            clase = p.get("clase", "-")
            umbral = p.get("umbral", 0.6)
            self.stdout.write(f"{codigo}\t\t{prob:.2f}\t\t{clase}\t{umbral:.2f}")

        self.stdout.write("")  # línea en blanco final
