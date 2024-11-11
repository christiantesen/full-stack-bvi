from . import base_model_config

class AuthResponse(base_model_config.BaseResponse):
    access_token: str
    refresh_token: str
    expires_in_seconds: int
    
    class Config:
        json_schema_extra = {
            "example": {
                "access_token": "eyJasdasdsadsadasdasdas",
                "refresh_token": "eyJasdasdasdasdasdas",
                "expires_in_seconds": 3600
            }
        }