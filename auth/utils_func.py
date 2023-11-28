from fastapi import HTTPException, status
from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider
import os 
from os.path import join, dirname
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), ".env")
load_dotenv(dotenv_path)
USERNAME = os.getenv("USERNAME")
PASSWORD = os.getenv("PASSWORD")

auth_provider = PlainTextAuthProvider(username=USERNAME, password=PASSWORD)
cluster = Cluster(['127.0.0.1'], auth_provider=auth_provider)
session = cluster.connect('brainmicroservice')

def clientLogin(username: str, password: str):
    query = f"""
        SELECT password FROM client_accounts WHERE username = %s
    """
    result = session.execute(query, (username,))
    stored_password = result.one()
    if stored_password and password == stored_password.password:
        return {"message": f"User {username} logged in successfully!"}
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid username or password")
    
def demoLogin(username: str, password: str):
    query = f"""
        SELECT password FROM demo_accounts WHERE username = %s
    """
    result = session.execute(query, (username,))
    stored_password = result.one()
    if stored_password and password == stored_password.password:
        return {"message": f"Demo {username} logged in successfully!"}
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid username or password")

def adminLogin(username: str, password: str):
    query = f"""
        SELECT password FROM admin_credential WHERE username = %s
    """
    result = session.execute(query, (username,))
    stored_password = result.one()
    if stored_password and password == stored_password.password:
        global last_successfull_login
        last_successfull_login = username 
        return {"message": f"User {username} logged in sucessfully!"}
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detial="Invalid username or password")