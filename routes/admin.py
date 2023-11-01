from fastapi import APIRouter,  HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider
from dotenv import load_dotenv
import os 
from os.path import join, dirname 
from schemas import admin, client, demo

from auth.auth_handler import signJWT
from auth.auth_bearer import JWTBearer

dotenv_path = join(dirname(__file__), ".env")
load_dotenv(dotenv_path)

USERNAME = os.getenv("USERNAME")
PASSWORD = os.getenv("PASSWORD")

router = APIRouter(prefix='/admin', tags=['admin'])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

auth_provider = PlainTextAuthProvider(username=USERNAME, password=PASSWORD)
cluster = Cluster(['127.0.0.1'], auth_provider=auth_provider)
session = cluster.connect('brainmicroservice')

@router.post('/lostToken', dependencies=[Depends(JWTBearer())])
async def lost_token(model: admin.LoginUser):
    try:
        query = f"""
            SELECT password FROM admin_credential WHERE username = %s
        """
        result = session.execute(query, (model.username,))

        stored_password = result.one()
        if stored_password and model.password == stored_password.password:
            return {"token": signJWT(model.username)}
        else:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid username or password, try again!")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"{str(e)}")

@router.post('/register', dependencies=[Depends(JWTBearer())])
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
    
@router.post('/client/register', dependencies=[Depends(JWTBearer())])
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
    
@router.post('/demo/register', dependencies=[Depends(JWTBearer())])
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

@router.delete('/client/delete', dependencies=[Depends(JWTBearer())])
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
    
@router.delete('/demo/delete', dependencies=[Depends(JWTBearer())])
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
    
@router.delete('/admin/delete', dependencies=[Depends(JWTBearer())])
async def delete_admin_user(model: admin.DeleteUser):
    try:
        check_user = """
            SELECT username FROM admin_credential WHERE username = %s ALLOW FILTERING
        """
        user_result = session.execute(check_user, (model.username,))
        if not user_result.one():
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User not found")
        delete_query = f"""
            DELETE FROM admin_credential WHERE username = %s
        """
        session.execute(delete_query, (model.username,))
        return {"message": f"User {model.username} deleted successfully!"}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Erro: {str(e)}")