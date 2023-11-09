from pydantic import BaseModel 

class RegisterUser(BaseModel):
    username: str 
    password: str 

class LoginUser(BaseModel):
    username: str 
    password: str

class DeleteUser(BaseModel):
    username: str 

class AddProject(BaseModel):
    username: str
    project_name: str
    url: str

class DeleteProject(BaseModel):
    username: str 
    project_name: str 