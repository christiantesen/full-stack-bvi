from loguru import logger
import sys

class LoggerConfig:
    """
    Configura el logger utilizando loguru con niveles y formatos personalizados.
    """
    
    MSG_INTERNAL_SERVER_ERROR = "🔴 Internal Server Error"

    def __init__(self):
        # Definir formatos personalizados para cada nivel
        logger.level("SUCCESS", color="<green>", icon="✔️")
        logger.level("INFO", color="<blue>", icon="ℹ️")
        logger.level("ERROR", color="<red>", icon="❌")
        logger.level("CRITICAL", color="<bold><red>", icon="🆘")

        # Definir el formato del log
        log_format = "{level}   {time:YYYY-MM-DD HH:mm:ss} - {message}"

        # Eliminar los manejadores existentes para evitar duplicados
        logger.remove()

        # Añadir un manejador para la salida de logs en la consola con el formato global
        logger.add(sys.stdout, level="DEBUG", format=log_format)

        # Añadir un manejador para la salida de logs en un archivo con rotación
        logger.add("api.log", rotation="1 MB", level="INFO", format=log_format)

    @classmethod
    def get_logger(cls):
        """Devuelve la instancia del logger configurado."""
        return logger

# Instanciar la configuración del logger
logger_config = LoggerConfig()
hyre = logger_config.get_logger()

# Ejemplo de uso
if __name__ == "__main__":
    hyre.success("Logger configurado exitosamente")
    hyre.info("Este es un mensaje informativo")
    hyre.error("Este es un mensaje de error")
    hyre.critical("Este es un mensaje crítico")

"""
Explicación de la Clase
Atributos de Clase:
MSG_INTERNAL_SERVER_ERROR: Mensaje de error interno del servidor.

Método __init__:
Se configuran los niveles de logging personalizados y sus respectivos colores e íconos.
Se define el formato de log.
Se eliminan los manejadores existentes para evitar duplicados.
Se añaden manejadores para la salida de logs en la consola y en un archivo con rotación.

Método get_logger:
Devuelve la instancia del logger configurado.
"""