from fastapi import APIRouter, HTTPException, status, responses
from cassandra import ConsistencyLevel
from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider
from cassandra.query import SimpleStatement
from dotenv import load_dotenv
import os 
from os.path import join, dirname
from email_validator import EmailNotValidError

from schemas.client import RegisterModel
from utils import is_valid_email

dotenv_path = join(dirname(__file__), ".env")
load_dotenv(dotenv_path)

USERNAME = os.getenv("USERNAME")
PASSWORD = os.getenv("PASSWORD")
github_personal_access_token = os.getenv('github_personal_access_token')

router = APIRouter(prefix='/client', tags=['client'])

auth_provider = PlainTextAuthProvider(username=USERNAME, password=PASSWORD)
cluster = Cluster(['127.0.0.1'], auth_provider=auth_provider)
session = cluster.connect('brainmicroservice')

@router.post('/register')
async def register_client_user(model: RegisterModel):
    try:
        query = f"""
            INSERT INTO client_accounts (username, email, password, contracted_project, company)
            VALUES (%s, %s, %s, %s, %s)
        """
        if not is_valid_email(model.email):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"{str(EmailNotValidError)}")
        session.execute(query, (model.username, model.email, model.password, model.contracted_project, model.company))
        return {"message": f"User {model.username} created successfully!"}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Error: {str(e)}")
    
@router.get('/inference/{username}')
async def query_project(username: str):
    get_project = """
        SELECT contracted_project FROM client_accounts WHERE username = %s ALLOW FILTERING
    """
    statement = SimpleStatement(get_project, consistency_level=ConsistencyLevel.ONE)
    get_result = session.execute(statement, (username,))
    if get_result:
        row = get_result[0]
        # Redirect to the run_project endpoint with the contracted project
        redirect_url = f"http://127.0.0.1:8000/client/inference/connect/{row.contracted_project}"
        return responses.RedirectResponse(url=redirect_url)
    else:
        raise HTTPException(status_code=404, detail="User not found")

@router.get('/inference/connect/{project_name}')
async def connect_project(project_name: str):
    try:
        redirect_url = f"http://127.0.0.1:8000/projects/{project_name}"
        return responses.RedirectResponse(url=redirect_url)
    except:
        return {"message": f"project {project_name} not found!"}