"""Configuración del archivo de logs (solo se usan archivos para eventos y errores)."""
import logging  # módulo estándar de Python para registrar eventos
import os       # para construir rutas y crear carpetas

# Ruta del archivo de logs: carpeta "logs" junto a este archivo
RUTA_LOG = os.path.join(os.path.dirname(os.path.abspath(__file__)), "logs", "software_fj.log")


def obtener_logger(nombre="software_fj"):
    """Devuelve un logger que escribe en logs/software_fj.log."""
    logger = logging.getLogger(nombre)          # obtiene (o crea) el logger por nombre
    if not logger.handlers:                     # evita duplicar manejadores si se llama varias veces
        os.makedirs(os.path.dirname(RUTA_LOG), exist_ok=True)  # crea la carpeta logs si no existe
        logger.setLevel(logging.DEBUG)          # registra todos los niveles
        manejador = logging.FileHandler(RUTA_LOG, encoding="utf-8")  # escribe en archivo
        formato = logging.Formatter("%(asctime)s | %(levelname)s | %(message)s")  # formato de línea
        manejador.setFormatter(formato)         # aplica el formato al manejador
        logger.addHandler(manejador)            # conecta el manejador al logger
    return logger                               # devuelve el logger listo para usar
