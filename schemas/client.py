from pydantic import BaseModel

class RegisterModel(BaseModel):
    email: str
    username: str 
    password: str 
    company: str 
    contracted_project: str 

class LoginModel(BaseModel):
    username: str 
    password: str 

class DeleteModel(BaseModel):
    username: str 