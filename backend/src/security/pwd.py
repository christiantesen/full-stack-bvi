from passlib.context import CryptContext
from typing import Tuple
from random import randint, choice
from re import match

class PasswordManager:
    """
    Clase para gestionar la creación, validación y almacenamiento seguro de contraseñas.
    """

    SPECIAL_CHARACTERS = ['@', '#', '$', '.']
    REGEX_PASSWORD = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@#$%=:?./|~>]).{8,15}$'
    
    def __init__(self):
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def hash_password(self, password: str) -> str:
        """
        Devuelve la versión hasheada de la contraseña.
        """
        return self.pwd_context.hash(password)

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """
        Verifica si la contraseña sin procesar coincide con la contraseña hasheada.
        """
        return self.pwd_context.verify(plain_password, hashed_password)

    def is_password_strong_enough(self, password: str) -> Tuple[bool, str]:
        """
        Valida la fuerza de la contraseña según criterios predefinidos.
        """
        errors = []
        if len(password) < 8 or len(password) > 15:
            errors.append("La contraseña debe tener entre 8 y 15 caracteres.")
        if not any(char.isupper() for char in password):
            errors.append("La contraseña debe tener al menos una letra mayúscula.")
        if not any(char.islower() for char in password):
            errors.append("La contraseña debe tener al menos una letra minúscula.")
        if not any(char.isdigit() for char in password):
            errors.append("La contraseña debe tener al menos un número.")
        if not any(char in self.SPECIAL_CHARACTERS for char in password):
            errors.append("La contraseña debe tener al menos un caracter '@', '#', '$', o '.'.")
        return True if not errors else False, errors

    def generate_password(self) -> str:
        """
        Genera una contraseña aleatoria que cumple con los requisitos de seguridad.
        """
        chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789@#$./"
        while True:
            password_length = randint(8, 15)
            new_pass = ''.join(choice(chars) for _ in range(password_length))
            if match(self.REGEX_PASSWORD, new_pass) and self.is_password_strong_enough(new_pass)[0]:
                return new_pass

# Ejemplo de uso
if __name__ == "__main__":
    pm = PasswordManager()
    new_password = pm.generate_password()
    print(f"Generated Password: {new_password}")
    hashed = pm.hash_password(new_password)
    print(f"Hashed Password: {hashed}")
    is_verified = pm.verify_password(new_password, hashed)
    print(f"Password Verified: {is_verified}")
    strong_enough, errors = pm.is_password_strong_enough(new_password)
    if not strong_enough:
        print("Errors:", errors)

"""
Descripción de la Clase PasswordManager
Atributos:

SPECIAL_CHARACTERS: Lista de caracteres especiales permitidos en las contraseñas.
REGEX_PASSWORD: Expresión regular para validar la estructura de la contraseña.
Método __init__:

Inicializa el contexto de CryptContext para el hashing de contraseñas.
Método hash_password:

Devuelve la versión hasheada de una contraseña utilizando bcrypt.
Método verify_password:

Verifica si una contraseña en texto claro coincide con su versión hasheada.
Método is_password_strong_enough:

Comprueba si una contraseña cumple con los requisitos de longitud y contenido, devolviendo un booleano y una lista de errores si los hay.
Método generate_password:

Genera una contraseña aleatoria que cumple con los requisitos de seguridad definidos.
"""