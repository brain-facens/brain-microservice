from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from dotenv import load_dotenv
import os
from os.path import join, dirname
from slowapi.errors import RateLimitExceeded
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
import logging
from logging.handlers import RotatingFileHandler

from routes import client, admin
from routes.home import projects, list, auth
from api_analytics.fastapi import Analytics

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

log_file = "logs/api.log"
handler = RotatingFileHandler(log_file, maxBytes=1000000, backupCount=5)  # maxBytes define o tamanho máximo de cada arquivo e backupCount define a quantidade máxima de arquivos a serem mantidos
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

dotenv_path = join(dirname(__file__), ".env")
load_dotenv(dotenv_path)

token = os.getenv("token")

app = FastAPI()

app.add_middleware(Analytics, api_key=token)

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter 
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

@app.get("/")
async def root(request: Request):
    client_ip = request.client.host

    response_content = {"message": "Nothing here. Try accessing <address>/docs"}
    response = JSONResponse(content=response_content, status_code=200)
    status_code = response.status_code
    logger.info(f"STATUS = {status_code} | Endereço IP: {client_ip} | Requisição rota '/'")
    return response 

app.include_router(admin.router)
app.include_router(client.router)
app.include_router(projects.router)
app.include_router(list.router)
app.include_router(auth.router)