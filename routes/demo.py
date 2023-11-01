# Rota para que o comercial tenha privilégios híbridos, acesso à todos os projetos
# porém somente para apresentação, modo leitura, inferência

from fastapi import APIRouter, Depends
from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider
from dotenv import load_dotenv
import os 
from os.path import join, dirname 

from auth.auth_bearer import JWTBearer

dotenv_path = join(dirname(__file__), ".env")
load_dotenv(dotenv_path)

USERNAME = os.getenv("USERNAME")
PASSWORD = os.getenv("PASSWORD")

router = APIRouter(prefix='/demo', tags=['demo'])

auth_provider = PlainTextAuthProvider(username=USERNAME, password=PASSWORD)
cluster = Cluster(['127.0.0.1'], auth_provider=auth_provider)
session = cluster.connect('brainmicroservice')

@router.get('/root')
async def demo_root():
    return {"message": "Hello from demo root page"}

@router.get('/projects', dependencies=[Depends(JWTBearer())])
async def infer_projects():
    """
    TODO: sistema onde roda a aplicação chamando a API da aplicação, baseado no nome do projeto requisitado pelo usuário
    """