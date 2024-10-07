from pytz import timezone
from datetime import datetime, timedelta

timezone_peru = timezone('America/Lima')

# Funciones para valores predeterminados dinámicos
def default_datetime():
    real_datetime = datetime.now(timezone_peru)
    real_datetime = datetime.strptime(real_datetime.strftime("%Y-%m-%d %H:%M:%S"), "%Y-%m-%d %H:%M:%S")
    return real_datetime

def default_date():
    return datetime.now(timezone_peru).date()

def default_time():
    return datetime.now(timezone_peru).time()