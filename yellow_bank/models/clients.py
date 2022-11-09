from pydantic import BaseModel

class ClientBase(BaseModel):
    login: str
    password: str

class Client(ClientBase):
    id: int

    class Config:
        orm_mode = True