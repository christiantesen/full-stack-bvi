class CharacterValidator:
    PERMITTED_CHARS = [
        '-', '_', '@', '#', '$', '%', '&', '*', '!', '+', '=', '.', ',', '?', ':', ';', '(', ')'
    ]
    FORBIDDEN_CHARS = [
        '<', '>', '{', '}', '[', ']', '\\', '/', '|', '~', '^', '`', '"', "'"
    ]

    @classmethod
    def is_valid(cls, text: str) -> bool:
        """
        Validates if the given text contains only permitted characters
        and does not contain any forbidden characters.
        
        Args:
            text (str): The text to validate.
        
        Returns:
            bool: True if valid, False otherwise.
        """
        return all(char in cls.PERMITTED_CHARS or char.isalnum() for char in text) and \
               not any(char in cls.FORBIDDEN_CHARS for char in text)

    @classmethod
    def get_permitted_chars(cls) -> list:
        """Returns a list of permitted characters."""
        return cls.PERMITTED_CHARS

    @classmethod
    def get_forbidden_chars(cls) -> list:
        """Returns a list of forbidden characters."""
        return cls.FORBIDDEN_CHARS

"""
Explicación de la Clase
Atributos de Clase:
PERMITTED_CHARS: Lista de caracteres que están permitidos.
FORBIDDEN_CHARS: Lista de caracteres que están prohibidos.

Métodos de Clase:
is_valid(text): Comprueba si el texto contiene solo caracteres permitidos y no contiene caracteres prohibidos.
get_permitted_chars(): Devuelve la lista de caracteres permitidos.
get_forbidden_chars(): Devuelve la lista de caracteres prohibidos.
"""