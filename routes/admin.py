from fastapi import APIRouter,  HTTPException, status, Depends, responses
from fastapi.security import OAuth2PasswordBearer
from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider
from dotenv import load_dotenv
import os 
from os.path import join, dirname 
from datetime import date
import shutil

from schemas import admin, client, demo
from utils import clone_repo

dotenv_path = join(dirname(__file__), ".env")
load_dotenv(dotenv_path)

USERNAME = os.getenv("USERNAME")
PASSWORD = os.getenv("PASSWORD")

router = APIRouter(prefix='/admin', tags=['admin'])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

auth_provider = PlainTextAuthProvider(username=USERNAME, password=PASSWORD)
cluster = Cluster(['127.0.0.1'], auth_provider=auth_provider)
session = cluster.connect('brainmicroservice')

@router.get('/dashboard')
async def connect_dashboard():
    redirect_url = "https://www.apianalytics.dev/dashboard/885be5bc407e49d9b73c0d5f85086390"
    try:
        response = responses.RedirectResponse(url=redirect_url)
        return response
    except Exception as e:
        return {"message": f"Exception: {str(e)}"}

@router.post("/add_project")
async def add_project(model: admin.AddProject):
    now = date.today()
    try:
        check_user = """
            SELECT username FROM admin_credential WHERE username = %s ALLOW FILTERING
        """
        user_result = session.execute(check_user, (model.username,))
        if not user_result.one():
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"User not found")
        add_query = f"""
            INSERT INTO projects (name, date_created, url)
            VALUES (%s, %s, %s)
        """
        clone_repo(model.project_name, model.url)
        session.execute(add_query, (model.project_name, now, model.url))
        return {"message": f"Project {model.project_name} created registered sucessfully!"}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Error: {str(e)}")

@router.post('/register')
async def register_admin(model: admin.RegisterUser):
    try:
        query = f"""
            INSERT INTO admin_credential (username, password)
            VALUES (%s, %s)
        """
        session.execute(query, (model.username, model.password))
        return {"message": f"User {model.username} created successfully!"}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Error: {str(e)}")
    
@router.post('/client/register')
async def register_client_user(model: client.RegisterModel):
    try:
        query = f"""
            INSERT INTO client_accounts (username, email, password, contracted_project, company)
            VALUES (%s, %s, %s, %s, %s)
        """
        session.execute(query, (model.username, model.email, model.password, model.contracted_project, model.company))
        return {"message": f"User {model.username} created successfully!"}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Error: {str(e)}")
    
@router.post('/demo/register')
async def register_demo_user(model: demo.RegisterModel):
    try: 
        query = f"""
            INSERT INTO demo_accounts (username, email_facens, password, setor)
            VALUES (%s, %s, %s, %s)
        """
        session.execute(query, (model.username, model.email_facens, model.password, model.setor))
        return {"message": f"User {model.username} created successfully!"}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Error: {str(e)}")

@router.delete('/client/delete')
async def delete_client_user(model: client.DeleteModel):
    try:
        check_user = """
            SELECT username FROM client_accounts WHERE username = %s ALLOW FILTERING
        """
        user_result = session.execute(check_user, (model.username,))
        if not user_result.one():
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User not found")
        delete_query = f"""
            DELETE FROM client_accounts WHERE username = %s
        """
        session.execute(delete_query, (model.username,))
        return {"message": f"User {model.username} deleted successfully!"}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Erro: {str(e)}")
    
@router.delete('/demo/delete')
async def delete_demo_user(model: demo.DeleteModel):
    try:
        check_user = """
            SELECT username FROM demo_accounts WHERE username = %s ALLOW FILTERING
        """
        user_result = session.execute(check_user, (model.username,))
        if not user_result.one():
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User not found")
        delete_query = f"""
            DELETE FROM demo_accounts WHERE username = %s
        """
        session.execute(delete_query, (model.username,))
        return {"message": f"User {model.username} deleted successfully!"}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Erro: {str(e)}")
    
@router.delete('/delete_user')
async def delete_admin_user(model: admin.DeleteUser):
    try:
        check_user = """
            SELECT username FROM admin_credential WHERE username = %s ALLOW FILTERING
        """
        user_result = session.execute(check_user, (model.username,))
        if not user_result.one():
            raise HTTPException(status_code=status.HTTP_401_BAD_REQUEST, detail="User not found")
        delete_query = f"""
            DELETE FROM admin_credential WHERE username = %s
        """
        session.execute(delete_query, (model.username,))
        return {"message": f"User {model.username} deleted successfully!"}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Erro: {str(e)}")
    
@router.delete('/delete_project')
async def delete_project(model: admin.DeleteProject):
    try:
        check_user = """
            SELECT username FROM admin_credential WHERE username = %s ALLOW FILTERING
        """
        user_result = session.execute(check_user, (model.username,))
        if not user_result.one():
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
        delete_query = f"""
            DELETE FROM projects WHERE name = %s 
        """
        path = f"projects/{model.project_name}"
        shutil.rmtree(path)
        session.execute(delete_query, (model.project_name,))
        return {"message": f"Project {model.project_name} deleted successfully!"}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Error: {str(e)}")