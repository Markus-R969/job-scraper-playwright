# src/utils/stealth.py
"""Técnicas básicas para evadir detección de bots en Playwright"""
import random
from playwright.sync_api import Page

def apply_stealth(page: Page):
    """Aplica configuraciones anti-detección a una instancia de página"""
    
    # 1. User-Agents realistas (rotación automática)
    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0",
    ]
    page.set_extra_http_headers({"User-Agent": random.choice(user_agents)})
    
    # 2. Viewport realista (simula monitor estándar)
    page.set_viewport_size({"width": 1920, "height": 1080})
    
    # 3. Inyectar script para ocultar propiedades de automatización
    page.add_init_script("""
        Object.defineProperty(navigator, 'webdriver', {get: () => undefined});
        Object.defineProperty(navigator, 'plugins', {get: () => [1, 2, 3, 4, 5]});
        Object.defineProperty(navigator, 'languages', {get: () => ['es-ES', 'en-US']});
        window.chrome = {runtime: {}};
    """)