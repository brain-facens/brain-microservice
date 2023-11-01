from pydantic import BaseModel 

class RegisterUser(BaseModel):
    username: str 
    password: str 

class LoginUser(BaseModel):
    username: str 
    password: str 

class DeleteUser(BaseModel):
    username: str 