from pydantic import BaseModel, EmailStr

## modelo de registrar tokens
class RegisterToken(BaseModel):  
    token: str

##
# modelo de registrar usuario

class RegisterRequest(BaseModel):
    username: str
    password: str
    email: EmailStr

class RegisterGoogle(BaseModel):
    username: str
    password: str