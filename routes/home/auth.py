from fastapi import APIRouter, HTTPException, status, Request
from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider
import os 
from os.path import join, dirname
from dotenv import load_dotenv
from slowapi import Limiter
from slowapi.util import get_remote_address

from auth.utils_func import clientLogin, demoLogin, adminLogin
from schemas import client, demo, admin

dotenv_path = join(dirname(__file__), ".env")
load_dotenv(dotenv_path)

USERNAME = os.getenv("USERNAME")
PASSWORD = os.getenv("PASSWORD")

router = APIRouter(prefix='/auth', tags=['auth'])

auth_provider = PlainTextAuthProvider(username=USERNAME, password=PASSWORD)
cluster = Cluster(['127.0.0.1'], auth_provider=auth_provider)
session = cluster.connect('brainmicroservice')

limiter = Limiter(key_func=get_remote_address)
    
@router.post('/client/login')
@limiter.limit("5/minute")
async def client_login(model: client.LoginModel, request: Request):
    try:
        return(clientLogin(model.username, model.password))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"{str(e)}")
        
    
@router.post('/demo/login')
@limiter.limit("5/minute")
async def demo_login(model: demo.LoginModel, request: Request):
    try:
        return(demoLogin(model.username, model.password))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"{str(e)}")
    
@router.post('/admin/login')
@limiter.limit("5/minute")
async def admin_login(model: admin.LoginUser, request: Request):
    try:
        return(adminLogin(model.username, model.password))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"{str(e)}")