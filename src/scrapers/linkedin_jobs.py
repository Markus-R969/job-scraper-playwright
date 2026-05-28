# src/scrapers/linkedin_jobs.py
"""Scraper de empleos adaptable (plantilla base para portales de trabajo)"""
import time
import random
from datetime import datetime
from src.scrapers.base import BaseScraper
from src.utils.logger import setup_logger

logger = setup_logger()

class JobScraper(BaseScraper):
    def __init__(self, target_url: str, headless: bool = True, timeout: int = 30000):
        super().__init__(headless=headless, timeout=timeout)
        self.target_url = target_url
        self.jobs = []

    def _build_page_url(self, page_number: int) -> str:
        """Construye URL de paginación adaptable al sitio objetivo"""
        if page_number == 1:
            return self.target_url.rstrip("/")
        
        # Lógica específica para books.toscrape.com
        if "books.toscrape.com" in self.target_url:
            # Formato: /catalogue/page-N.html
            base = self.target_url.rstrip("/")
            if "/catalogue" in base:
                return f"{base.rsplit('/', 1)[0]}/page-{page_number}.html"
            return f"{base}/catalogue/page-{page_number}.html"
        
        # Fallback genérico para otros sitios
        return f"{self.target_url}&page={page_number}"

    def scrape_page(self, page_number: int = 1) -> list[dict]:
        """Extrae tarjetas de empleo de una página"""
        url = self._build_page_url(page_number)

        try:
            self.goto_with_retry(url)

            # Esperar contenedor de resultados (ajustar selector según el sitio real)
            if not self.wait_for_selector_safe(".product_pod, .job-card, .job-listing, article", timeout=15000):
                logger.warning("⚠️ No se encontraron resultados en esta página")
                return []

            # Extraer tarjetas (selectores genéricos, fáciles de adaptar)
            job_cards = self.page.query_selector_all(".product_pod, .job-card, .job-listing, article")
            logger.info(f"📦 Encontradas {len(job_cards)} ofertas en página {page_number}")

            for i, card in enumerate(job_cards):
                try:
                    title_el = card.query_selector("h3, h2, .title, a")
                    company_el = card.query_selector(".company, .company-name, .price_color, span[data-testid='company']")
                    location_el = card.query_selector(".location, .place, .availability, span[data-testid='location']")
                    date_el = card.query_selector(".date, .time, .posted-date, span[data-testid='posted-time']")
                    link_el = card.query_selector("a[href]")

                    job = {
                        "title": title_el.inner_text().strip() if title_el else "",
                        "company": company_el.inner_text().strip() if company_el else "",
                        "location": location_el.inner_text().strip() if location_el else "",
                        "posted_date": date_el.inner_text().strip() if date_el else "",
                        "url": link_el.get_attribute("href") if link_el else "",
                        "scraped_at": datetime.now().isoformat(),
                        "page": page_number
                    }
                    self.jobs.append(job)
                except Exception as e:
                    logger.debug(f"⚠️ Error procesando tarjeta {i+1}: {e}")
                    continue

            return self.jobs

        except Exception as e:
            logger.error(f"❌ Error en página {page_number}: {e}")
            return []

    def scrape_multiple_pages(self, max_pages: int = 3) -> list[dict]:
        """Scrapea múltiples páginas con delays humanos entre ellas"""
        all_jobs = []
        for page in range(1, max_pages + 1):
            logger.info(f"📄 Procesando página {page}/{max_pages}")
            jobs = self.scrape_page(page)
            all_jobs.extend(jobs)

            if page < max_pages and jobs:
                delay = random.uniform(3, 6)
                logger.info(f"⏱️ Pausa humana: {delay:.1f}s antes de siguiente página...")
                time.sleep(delay)
            elif not jobs:
                logger.info("🛑 No hay más resultados. Deteniendo scrapeo.")
                break

        return all_jobs