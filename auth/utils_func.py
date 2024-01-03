from fastapi import HTTPException, status, Request 
from fastapi.responses import JSONResponse
from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider
import os 
from os.path import join, dirname
from dotenv import load_dotenv
import logging 
from logging.handlers import RotatingFileHandler

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

log_file = "logs/api.log"
handler = RotatingFileHandler(log_file, maxBytes=1000000, backupCount=5)  # maxBytes define o tamanho máximo de cada arquivo e backupCount define a quantidade máxima de arquivos a serem mantidos
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

dotenv_path = join(dirname(__file__), ".env")
load_dotenv(dotenv_path)
USERNAME = os.getenv("USERNAME")
PASSWORD = os.getenv("PASSWORD")

auth_provider = PlainTextAuthProvider(username=USERNAME, password=PASSWORD)
cluster = Cluster(['127.0.0.1'], auth_provider=auth_provider)
session = cluster.connect('brainmicroservice')

def clientLogin(username: str, password: str, request: Request):
    client_ip = request.client.host 
    query = f"""
        SELECT password FROM client_accounts WHERE username = %s
    """
    result = session.execute(query, (username,))
    stored_password = result.one()
    if stored_password and password == stored_password.password:
        response_content = {"message": f"User {username} logged in successfully!"}
        response = JSONResponse(content=response_content, status_code=200)
        status_code = response.status_code
        logger.info(f"STATUS = {status_code} | Endereço IP: {client_ip} | Data: {response_content} | CLIENT")
        return response_content
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid username or password")
    
def demoLogin(username: str, password: str, request: Request):
    client_ip = request.client.host 
    query = f"""
        SELECT password FROM demo_accounts WHERE username = %s
    """
    result = session.execute(query, (username,))
    stored_password = result.one()
    if stored_password and password == stored_password.password:
        response_content = {"message": f"User {username} logged in successfully!"}
        response = JSONResponse(content=response_content, status_code=200)
        status_code = response.status_code
        logger.info(f"STATUS = {status_code} | Endereço IP: {client_ip} | Data: {response_content} | DEMO")
        return response_content
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid username or password")

def adminLogin(username: str, password: str, request: Request):
    client_ip = request.client.host 
    query = f"""
        SELECT password FROM admin_credential WHERE username = %s
    """
    result = session.execute(query, (username,))
    stored_password = result.one()
    if stored_password and password == stored_password.password:
        response_content = {"message": f"User {username} logged in successfully!"}
        response = JSONResponse(content=response_content, status_code=200)
        status_code = response.status_code
        logger.info(f"STATUS = {status_code} | Endereço IP: {client_ip} | Data: {response_content} | ADMIN")
        return response_content
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid username or password")