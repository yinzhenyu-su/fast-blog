from pydantic import BaseModel, SecretStr

class User(BaseModel):
    id: str
    username: str
    password: SecretStr

