from pydantic import BaseModel 

class RegisterModel(BaseModel):
    email_facens: str 
    username: str 
    password: str 
    setor: str 

class LoginModel(BaseModel):
    username: str 
    password: str 

class DeleteModel(BaseModel):
    username: str