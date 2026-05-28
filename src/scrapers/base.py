# src/scrapers/base.py
"""Clase base para scrapers con Playwright: gestión de navegador, reintentos y comportamiento humano"""
import time
import random
from playwright.sync_api import sync_playwright, Page, Browser
from tenacity import retry, stop_after_attempt, wait_exponential
from src.utils.stealth import apply_stealth
from src.utils.logger import setup_logger

logger = setup_logger()

class BaseScraper:
    def __init__(self, headless: bool = True, timeout: int = 30000):
        self.headless = headless
        self.timeout = timeout
        self.playwright = None
        self.browser: Browser | None = None
        self.page: Page | None = None

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def start(self):
        """Inicializa el navegador con configuración anti-detección"""
        logger.info("🚀 Iniciando navegador Playwright...")
        self.playwright = sync_playwright().start()
        
        self.browser = self.playwright.chromium.launch(
            headless=self.headless,
            args=[
                "--disable-blink-features=AutomationControlled",
                "--no-sandbox",
                "--disable-dev-shm-usage",
            ]
        )
        
        self.page = self.browser.new_page()
        self.page.set_default_timeout(self.timeout)
        apply_stealth(self.page)
        logger.info("✅ Navegador listo y configurado con stealth")

    def close(self):
        """Cierra navegador y libera recursos"""
        if self.page: self.page.close()
        if self.browser: self.browser.close()
        if self.playwright: self.playwright.stop()
        logger.info("🔒 Navegador cerrado correctamente")

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10))
    def goto_with_retry(self, url: str):
        """Navega a una URL con reintentos automáticos ante fallos de red"""
        logger.info(f"🌐 Navegando a: {url}")
        response = self.page.goto(url, wait_until="networkidle")
        if response.status != 200:
            raise Exception(f"Error HTTP {response.status}")
        self.human_scroll()
        return response

    def human_scroll(self, max_scrolls: int = 3, delay_range: tuple = (0.8, 2.0)):
        """Simula scroll humano para cargar contenido dinámico y evitar rate-limits"""
        for _ in range(max_scrolls):
            self.page.evaluate("window.scrollBy(0, window.innerHeight * 0.8)")
            time.sleep(random.uniform(*delay_range))

    def wait_for_selector_safe(self, selector: str, timeout: int | None = None):
        """Espera por un elemento CSS con manejo seguro de errores"""
        try:
            self.page.wait_for_selector(selector, timeout=timeout or self.timeout)
            return True
        except Exception as e:
            logger.warning(f"⚠️ Selector no encontrado: {selector} - {e}")
            return False