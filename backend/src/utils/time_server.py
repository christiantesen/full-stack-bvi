from pytz import timezone
from datetime import datetime

class DateTimeUtils:
    """
    Clase utilitaria para manejar fechas y horas en la zona horaria de Perú.
    """

    def __init__(self):
        self.timezone_peru = timezone('America/Lima')

    def default_datetime(self) -> datetime:
        """
        Devuelve la fecha y hora actual en la zona horaria de Perú.
        """
        real_datetime = datetime.now(self.timezone_peru)
        # Devuelve un datetime sin microsegundos
        return datetime.strptime(real_datetime.strftime("%Y-%m-%d %H:%M:%S"), "%Y-%m-%d %H:%M:%S")

    def default_date(self) -> datetime.date:
        """
        Devuelve la fecha actual en la zona horaria de Perú.
        """
        return datetime.now(self.timezone_peru).date()

    def default_time(self) -> datetime.time:
        """
        Devuelve la hora actual en la zona horaria de Perú.
        """
        return datetime.now(self.timezone_peru).time()

# Ejemplo de uso
if __name__ == "__main__":
    dt_utils = DateTimeUtils()
    print("Fecha y hora actual:", dt_utils.default_datetime())
    print("Fecha actual:", dt_utils.default_date())
    print("Hora actual:", dt_utils.default_time())

"""
Explicación de la Clase
Atributo timezone_peru:
Almacena la zona horaria de Perú (America/Lima).

Método default_datetime:
Devuelve la fecha y hora actual en la zona horaria de Perú, sin microsegundos.

Método default_date:
Devuelve solo la fecha actual en la zona horaria de Perú.

Método default_time:
Devuelve solo la hora actual en la zona horaria de Perú.
"""