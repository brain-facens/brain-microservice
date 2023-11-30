from fastapi import APIRouter, Depends
from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider
from dotenv import load_dotenv
import os 
from os.path import join, dirname 
from utils import *
import requests

dotenv_path = join(dirname(__file__), ".env")
load_dotenv(dotenv_path)

USERNAME = os.getenv("USERNAME")
PASSWORD = os.getenv("PASSWORD")
github_personal_access_token = os.getenv('github_personal_access_token')

router = APIRouter(prefix='/list', tags=['list'])

auth_provider = PlainTextAuthProvider(username=USERNAME, password=PASSWORD)
cluster = Cluster(['127.0.0.1'], auth_provider=auth_provider)

session = cluster.connect('brainmicroservice')

@router.get('/client/list_users')
async def list_client_users():
    try:
        query = "SELECT username from client_accounts"
        result = session.execute(query)

        users = []
        for row in result:
            path_users = row[0]
            users.append(path_users)
        
        return {"client users": users}
    except Exception as e:
        return {"Error": str(e)}
    
@router.get('/demo/list_users')
async def list_client_users():
    try:
        query = "SELECT username from demo_accounts"
        result = session.execute(query)

        users = []
        for row in result:
            path_users = row[0]
            users.append(path_users)
        return {"demo users": users}
    except Exception as e:
        return {"Error": f"{str(e)}"}
    
@router.get('/list_repository')
async def list_repo():
    session = requests.Session()
    session.headers.update({'Authorization': f'token {github_personal_access_token}'})
    org_repo_url = 'https://api.github.com/orgs/brain-facens/repos'
    response = session.get(org_repo_url)
    
    if response.status_code == 200:
        data = response.json()
        # Extract the name and URL of each repository
        repositories_info = [{"name": repo["name"], "url": repo["html_url"]} for repo in data]
        return repositories_info
    else:
        return []