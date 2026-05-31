# 💼 Job Scraper | Extractor de Ofertas de Empleo

Automatización en Python con Playwright para extraer ofertas de trabajo de portales dinámicos, limpiar datos y generar reportes listos para Excel/CSV.

---

## 📦 ¿Qué hace?
- ✅ Navega portales con JavaScript (InfoJobs, LinkedIn, Indeed, etc.)
- ✅ Extrae: título, empresa, ubicación, salario, fecha, URL
- ✅ Filtra por palabras clave y ubicación
- ✅ Exporta a Excel con formato limpio y filtros
- ✅ Anti-bots: delays aleatorios, user-agent rotativo
- ✅ 100% local: sin APIs de terceros, sin suscripciones

---

## 🏗️ Arquitectura Modular
El código está organizado para facilitar mantenimiento y escalabilidad:
- `src/scrapers/` → Lógica de navegación y extracción por portal
- `src/etl/` → Limpieza, validación y transformación de datos
- `src/utils/` → Helpers, logging y gestión de configuración

---

## 🚀 Instalación y Uso

1. Clona o descarga el repositorio
2. Instala dependencias:
   pip install -r requirements.txt
   playwright install chromium
3. Configura la búsqueda:
   - Copia config\.env.example → config\.env
   - Edita TARGET_URL y KEYWORDS
4. Ejecuta:
   python src/main.py

---

## 📤 Salida

Se genera automáticamente en output/:
- ofertas_empleo_YYYYMMDD_HHMM.csv → Datos crudos para análisis
- ofertas_empleo_YYYYMMDD_HHMM.xlsx → Excel con filtros y formato profesional
- logs/ → Registro de ejecución para depuración

---

## 💼 Casos de Uso
- 🔍 Headhunting: búsqueda proactiva de candidatos
-  Análisis de mercado laboral por sector/ubicación
- 🤖 Automatización de alertas de nuevas ofertas
- 📈 Comparativa de salarios y beneficios por empresa

---

## ️ Personalización (para clientes)

| Módulo | Descripción |
|--------|-------------|
|  Multi-portal | InfoJobs, LinkedIn, Indeed, Glassdoor, Tecnoempleo |
|  Filtros avanzados | Salario mínimo, experiencia, tipo de contrato |
| ⏰ Programación | Ejecución diaria/semanal vía Task Scheduler |
| 🔔 Alertas | Email/Telegram cuando aparezca una oferta que coincida |
|  Dashboard | Integración con Power BI para visualización de tendencias |

---

## 📩 Soporte y Desarrollo a Medida

¿Necesitas scrapear un portal específico, añadir filtros personalizados o integrar con tu ATS?

📧 mark.markuslab@gmail.com
💼 Portfolio: https://github.com/Markus-R969

---

*Hecho con Python, Playwright y pandas. Código limpio, documentado y listo para producción.*
