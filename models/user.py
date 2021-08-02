from typing import Optional
from pydantic import BaseModel, SecretStr
from pydantic.types import UUID4

class User(BaseModel):
    id: Optional[UUID4]
    username: str
    password: str
