# src/utils/logger.py
from loguru import logger
import sys
from pathlib import Path

def setup_logger(log_file: str = "logs/app.log"):
    """Configura logger profesional con rotación diaria y colores en consola"""
    Path("logs").mkdir(exist_ok=True)
    
    # Remover handler por defecto para evitar duplicados
    logger.remove()
    
    # Salida a consola (con colores y formato limpio)
    logger.add(
        sys.stderr,
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
        level="INFO",
        colorize=True
    )
    
    # Salida a archivo (sin colores, rotación diaria, retención 7 días)
    logger.add(
        log_file,
        format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
        level="DEBUG",
        rotation="1 day",
        retention="7 days",
        encoding="utf-8"
    )
    
    return logger