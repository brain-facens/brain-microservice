from fastapi import APIRouter, HTTPException, status
from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider
import os 
from os.path import join, dirname
from dotenv import load_dotenv

from schemas import client, demo, admin
from auth.auth_bearer import JWTBearer
from auth.auth_handler import signJWT

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
        query = f"""
            SELECT password FROM client_accounts WHERE username = %s
        """
        result = session.execute(query, (model.username,))

        stored_password = result.one()
        if stored_password and model.password == stored_password.password:
            return {"message": f"User {model.username} logged in successfully! \n token: {signJWT(model.username)}"}
        else:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid username or password, try again!")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"{str(e)}")
    
@router.post('/demo/login')
async def client_login(model: demo.LoginModel):
    try:
        query = f"""
            SELECT password FROM demo_accounts WHERE username = %s
        """
        result = session.execute(query, (model.username,))

        stored_password = result.one()
        if stored_password and model.password == stored_password.password:
            return {"message": f"Demo {model.username} logged in successfully! \n token: {signJWT(model.username)}"}
        else:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid username or password, try again!")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"{str(e)}")
    
@router.post('/admin/login')
async def admin_login(model: admin.LoginUser):
    try:
        query = f"""
            SELECT password FROM admin_credential WHERE username = %s
        """
        result = session.execute(query, (model.username,))

        stored_password = result.one()
        if stored_password and model.password == stored_password.password:
            global last_successfull_login
            last_successfull_login = model.username
            return {"message": f"User {model.username} logged in successfully! \n token: {signJWT(model.username)}"}
        else:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid username or password, try again!")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"{str(e)}")
