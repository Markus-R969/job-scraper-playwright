# src/main.py
"""Punto de entrada principal para el scraper de empleos (Case 2)"""
import os
from datetime import datetime
from dotenv import load_dotenv
from src.scrapers.linkedin_jobs import JobScraper
from src.etl.clean import clean_job_data
from src.etl.load import export_to_csv, export_to_db
from src.utils.logger import setup_logger

# Cargar variables de entorno
load_dotenv("config/.env")

logger = setup_logger()

def main():
    logger.info("🤖 Job Scraper v2.0 - Playwright Edition")
    
    # Leer configuración desde .env
    target_url = os.getenv("TARGET_URL")
    if not target_url:
        logger.error("❌ TARGET_URL no definida en config/.env")
        return

    headless = os.getenv("HEADLESS", "true").lower() == "true"
    max_pages = int(os.getenv("MAX_PAGES", "3"))
    page_timeout = int(os.getenv("PAGE_TIMEOUT", "30000"))
    export_csv = os.getenv("EXPORT_PATH", "data/processed/jobs_{{date}}.csv")
    export_db = os.getenv("DB_PATH", "tracker.db")

    try:
        # Ejecutar scraping con context manager (garantiza cierre automático del navegador)
        with JobScraper(target_url=target_url, headless=headless, timeout=page_timeout) as scraper:
            raw_jobs = scraper.scrape_multiple_pages(max_pages=max_pages)

        if not raw_jobs:
            logger.warning("⚠️ No se extrajeron empleos. Verificar selectores o URL.")
            return

        # Limpiar y normalizar datos
        logger.info("🧹 Limpiando y normalizando datos...")
        cleaned_jobs = [clean_job_data(job) for job in raw_jobs]

        # Exportar resultados
        if export_csv:
            csv_path = export_csv.replace("{{date}}", datetime.now().strftime("%Y%m%d"))
            export_to_csv(cleaned_jobs, csv_path)

        if export_db:
            export_to_db(cleaned_jobs, export_db, table_name="jobs")

        logger.info(f"✅ Finalizado. {len(cleaned_jobs)} empleos procesados correctamente.")

    except KeyboardInterrupt:
        logger.info("🛑 Ejecución interrumpida por el usuario (Ctrl+C)")
    except Exception as e:
        logger.error(f"❌ Error crítico en la ejecución: {e}", exc_info=True)

if __name__ == "__main__":
    main()