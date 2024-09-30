from fastapi import Form
from fastapi.security import OAuth2PasswordRequestForm

class OAuth2PasswordRequestForm2Params(OAuth2PasswordRequestForm):
    def __init__(
        self, 
        username: str = Form(...), 
        password: str = Form(...),
    ):
        super().__init__(username=username, password=password)

    @classmethod
    def as_form(
        cls, 
        username: str = Form(...), 
        password: str = Form(...)
    ):
        return cls(username=username, password=password)