from fastapi import APIRouter, HTTPException, status
from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider
import os 
from os.path import join, dirname
from dotenv import load_dotenv
from auth.utils_func import clientLogin, demoLogin, adminLogin

from schemas import client, demo, admin

dotenv_path = join(dirname(__file__), ".env")
load_dotenv(dotenv_path)

USERNAME = os.getenv("USERNAME")
PASSWORD = os.getenv("PASSWORD")
github_client_id = os.getenv('github_client_id')
github_client_secret = os.getenv('github_client_secret')
github_personal_access_token = os.getenv('github_personal_access_token')

router = APIRouter(prefix='/auth', tags=['auth'])

auth_provider = PlainTextAuthProvider(username=USERNAME, password=PASSWORD)
cluster = Cluster(['127.0.0.1'], auth_provider=auth_provider)
session = cluster.connect('brainmicroservice')

last_successfull_login = None
    
@router.post('/client/login')
async def client_login(model: client.LoginModel):
    try:
        return(clientLogin(model.username, model.password))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"{str(e)}")
        
    
@router.post('/demo/login')
async def demo_login(model: demo.LoginModel):
    try:
        return(demoLogin(model.username, model.password))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"{str(e)}")
    
@router.post('/admin/login')
async def admin_login(model: admin.LoginUser):
    try:
        return(adminLogin(model.username, model.password))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"{str(e)}")