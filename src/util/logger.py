from loguru import logger
import sys

# Definir formatos personalizados para cada nivel
logger.level("SUCCESS", color="<green>", icon="✔️")
logger.level("INFO", color="<blue>", icon="ℹ️")
logger.level("ERROR", color="<red>", icon="❌")
logger.level("CRITICAL", color="<bold><red>", icon="🆘")

# Definir el formato del log
log_format = "{level}   {time:YYYY-MM-DD HH:mm:ss} - {message}"

# Eliminar los manejadores existentes (si los hay) para evitar duplicados
logger.remove()

# Añadir un manejador para la salida de logs en la consola con el formato global
logger.add(sys.stdout, level="DEBUG", format=log_format)

# Añadir un manejador para la salida de logs en un archivo con rotación
logger.add("api.log", rotation="1 MB", level="INFO", format=log_format)