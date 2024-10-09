from pydantic import BaseModel, ConfigDict
from typing import Optional, Dict


class BaseResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True, arbitrary_types_allowed=True)
    
class BaseRequest(BaseModel):
    model_config = ConfigDict(from_attributes=True)