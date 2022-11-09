from pydantic import BaseModel, Field, EmailStr

class UserSchema(BaseModel):
    login: str = Field(...)
    password: str = Field(...)

    class Config:
        schema_extra = {
            "example": {
                "login": "nick",
                "password": "strong_password"
            }
        }

class UserLoginSchema(BaseModel):
    login: str = Field(...)
    password: str = Field(...)

    class Config:
        schema_extra = {
            "example": {
                "login": "nick",
                "password": "strong_password"
            }
        }

class Url(BaseModel):
    url: str
class AuthorizationResponse(BaseModel):
    pass
class User(BaseModel):
    pass
class AuthUser(BaseModel):
    pass
class Token(BaseModel):
    pass