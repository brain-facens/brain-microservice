from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import os  
from utils import projectsWriter

html = projectsWriter("templates/template.html", "src/config.json")
html.create("templates/index.html")

# rota onde os projetos serão transformados em API e aqui alocadas as suas execuções

"""
Projetos:
    - Tumor (docker)
    - Area delimitada (pegar projeto no PCzao, dentro pasta YOLO)
    - OCR Notas (docker)
    - emotion (local)
"""

router = APIRouter(prefix='/projects', tags=['projects'])

templates = Jinja2Templates(directory="templates")
router.mount("/static", StaticFiles(directory="static"), name="static")

@router.get('/root', response_class=HTMLResponse)
async def projects_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@router.get('/emotion')
async def run_emotion():
    """
    TODO: transformar o detect.py em endpoint real de API, fonte: https://stackoverflow.com/questions/70167811/how-to-load-custom-model-in-pytorch & https://github.com/WelkinU/yolov5-fastapi-demo
    """
    os.system("cd ../brain-microservice/projects/emotion/scripts && python3 detect.py --source 0 --weights best4.onnx")

@router.get('/helmet-detector')
async def run_helmet():
    return {"message": "helmet detector"}