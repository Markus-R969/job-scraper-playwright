# src/etl/clean.py
"""Limpieza y normalización de datos extraídos"""
import re
from datetime import datetime, timedelta

def clean_job_data(job: dict) -> dict:
    """Limpia y normaliza un registro de empleo"""
    # Limpiar campos de texto (espacios múltiples, saltos de línea)
    for key in ["title", "company", "location", "posted_date"]:
        if job.get(key):
            job[key] = re.sub(r'\s+', ' ', job[key]).strip()

    # Normalizar fecha (relativa o absoluta)
    if job.get("posted_date"):
        job["posted_date_normalized"] = parse_date(job["posted_date"])

    # Limpiar URL (quitar parámetros de tracking y anclas)
    if job.get("url"):
        base_url = job["url"].split("?")[0].split("#")[0]
        if not base_url.startswith(("http://", "https://")):
            # Fallback: dejarla tal cual si es relativa (se puede ajustar según el sitio)
            pass
        job["url"] = base_url

    # Metadata de procesamiento
    job["processed_at"] = datetime.now().isoformat()
    return job

def parse_date(date_str: str) -> str | None:
    """Convierte texto de fecha a formato ISO. Maneja formatos comunes en español/inglés."""
    date_str = date_str.lower().strip()
    try:
        # Caso 1: Fechas relativas ("hace 2 días", "hace 3 horas")
        if "hace" in date_str:
            days_match = re.search(r'(\d+)\s*d[ií]as?', date_str)
            hours_match = re.search(r'(\d+)\s*horas?', date_str)
            delta = timedelta(
                days=int(days_match.group(1)) if days_match else 0,
                hours=int(hours_match.group(1)) if hours_match else 0
            )
            return (datetime.now() - delta).isoformat()

        # Caso 2: Formatos absolutos comunes
        for fmt in ("%d/%m/%Y", "%Y-%m-%d", "%d %b %Y", "%b %d, %Y"):
            try:
                return datetime.strptime(date_str, fmt).isoformat()
            except ValueError:
                continue

        # Fallback seguro si no se reconoce el formato
        return datetime.now().isoformat()
    except Exception:
        return None