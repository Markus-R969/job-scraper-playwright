# src/etl/load.py
"""Carga de datos a CSV y SQLite"""
import pandas as pd
import sqlite3
from pathlib import Path
from src.utils.logger import setup_logger

logger = setup_logger()

def export_to_csv(data: list[dict], output_path: str) -> str:
    """Exporta lista de dicts a CSV con encoding UTF-8-SIG (100% compatible con Excel)"""
    if not data:
        logger.warning("⚠️ No hay datos para exportar a CSV")
        return ""

    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)

    df = pd.DataFrame(data)
    
    # Ordenar columnas para mantener consistencia en el archivo
    preferred_order = ["title", "company", "location", "posted_date", 
                       "posted_date_normalized", "url", "page", "scraped_at", "processed_at"]
    existing_cols = [c for c in preferred_order if c in df.columns]
    extra_cols = [c for c in df.columns if c not in preferred_order]
    df = df[existing_cols + extra_cols]

    df.to_csv(path, index=False, encoding="utf-8-sig")
    logger.info(f"📄 Exportado a CSV: {path.name} ({len(df)} registros)")
    return str(path)

def export_to_db(data: list[dict], db_path: str, table_name: str = "jobs"):
    """Exporta a SQLite (escalable a PostgreSQL/Supabase en el futuro)"""
    if not data:
        logger.warning("⚠️ No hay datos para exportar a DB")
        return

    path = Path(db_path)
    path.parent.mkdir(parents=True, exist_ok=True)

    conn = sqlite3.connect(str(path))
    try:
        df = pd.DataFrame(data)
        # pandas crea la tabla automáticamente si no existe, o añade si ya existe
        df.to_sql(table_name, conn, if_exists="append", index=False)
        logger.info(f"💾 Guardado en DB: {db_path} ({len(df)} nuevos registros en '{table_name}')")
    except Exception as e:
        logger.error(f"❌ Error al guardar en DB: {e}")
    finally:
        conn.close()