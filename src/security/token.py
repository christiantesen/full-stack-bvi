from base64 import b85encode, b85decode
from jose import jwt

def str_encode(str: str) -> str:  # ? Validado
    return b85encode(str.encode('ascii')).decode('ascii')


def str_decode(str: str) -> str:  # ? Validado
    return b85decode(str.encode('ascii')).decode('ascii')

def generate_token(payload: dict, secret: str, algo: str):
    return jwt.encode(payload, secret, algorithm=algo)


def get_token_payload(token: str, secr, algo):  # ? Validado
    try:
        payload = jwt.decode(token, secr, algorithms=algo)
    except Exception as jwt_exec:
        print(f"JWT Error: {str(jwt_exec)}")
        payload = None
    return payload