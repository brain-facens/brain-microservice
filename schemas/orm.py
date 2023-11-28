from pydantic import BaseModel 

class Insert(BaseModel):
    table: str 
    username: str 
    email: str 
    password: str 
    contracted_project: str 
    company: str 