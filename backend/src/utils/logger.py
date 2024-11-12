from loguru import logger
import sys

class LoggerConfig:
    """
    Configura el logger utilizando loguru con niveles y formatos personalizados.
    """
    
    MSG_INTERNAL_SERVER_ERROR = "🔴 Internal Server Error"

    def __init__(self):
        # Eliminar los manejadores existentes para evitar duplicados
        logger.remove()
        # Define custom filters for each log level
        def level_filter(level):
            def is_level(record):
                return record["level"].name == level
            return is_level
        # Add handlers with custom formats
        logger.add(sys.stderr, format="<green>{level}</green>:  ✔️\n{message}", filter=level_filter(level="SUCCESS"))
        logger.add(sys.stderr, format="<blue>{level}</blue>:     ℹ\n{message}", filter=level_filter(level="INFO"))
        logger.add(sys.stderr, format="<yellow>{level}</yellow>:  ⚠️\n{message}", filter=level_filter(level="WARNING"))
        logger.add(sys.stderr, format="<red>{level}</red>:    ❌\n{message}", filter=level_filter(level="ERROR"))
        logger.add(sys.stderr, format="<bold><red>{level}</red></bold>:  🆘\n{message}", filter=level_filter(level="CRITICAL"))

        # Añadir un manejador para la salida de logs en un archivo con rotación
        logger.add("api.log", rotation="5 MB", level="DEBUG")

    @classmethod
    def get_logger(cls):
        """Devuelve la instancia del logger configurado."""
        return logger

# Instanciar la configuración del logger
logger_config = LoggerConfig()
hyre = logger_config.get_logger()

MSG_INTERNAL_SERVER_ERROR = logger_config.MSG_INTERNAL_SERVER_ERROR

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