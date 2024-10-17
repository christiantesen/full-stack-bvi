from passlib.context import CryptContext
from typing import Tuple
from random import randint, choice
from re import match

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

SPECIAL_CHARACTERS = ['@', '#', '$', '.']
REGEX_PASSWORD = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@#$%=:?./|~>]).{8,15}$'

def hash_password(password: str) -> str:  # ? Validado
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password) -> bool:  # ? Validado
    return pwd_context.verify(plain_password, hashed_password)

def is_password_strong_enough(password: str) -> Tuple[bool, str]:  # ? Validado
    errors = []
    if len(password) < 8 or len(password) > 15:
        errors.append("La contraseña debe tener entre 8 y 15 caracteres.")
    if not any(char.isupper() for char in password):
        errors.append("La contraseña debe tener al menos una letra mayúscula.")
    if not any(char.islower() for char in password):
        errors.append("La contraseña debe tener al menos una letra minúscula.")
    if not any(char.isdigit() for char in password):
        errors.append("La contraseña debe tener al menos un número.")
    if not any(char in SPECIAL_CHARACTERS for char in password):
        errors.append("La contraseña debe tener al menos un caracter '@', '#', '$','.' y '/'.")
    return True if not errors else False, errors

def generate_password():  # ? Validado
    """
    Generates a random password that meets the following requirements:
    - At least one lowercase letter
    - At least one uppercase letter
    - At least one digit
    - At least one special character
    - Length between 8 and 15 characters
    """
    chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789@#$./"
    while True:
        password_length = randint(8, 15)
        new_pass = ''.join(choice(chars) for _ in range(password_length))
        if match(REGEX_PASSWORD, new_pass) and is_password_strong_enough(new_pass)[0]:
            return new_pass