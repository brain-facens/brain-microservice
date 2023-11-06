from fastapi import APIRouter
import os  

# rota onde os projetos serão transformados em API e aqui alocadas as suas execuções

"""
Projetos:
    - Tumor
    - Area delimitada
    - OCR Notas
    - emotion
"""

router = APIRouter(prefix='/projects', tags=['projects'])

@router.get('/root')
async def projects_root():
    return {"message": "Hello from projects root page"}

@router.get('/emotion')
async def run_emotion():
    """
    TODO: transformar o detect.py em endpoint real de API, fonte: https://stackoverflow.com/questions/70167811/how-to-load-custom-model-in-pytorch & https://github.com/WelkinU/yolov5-fastapi-demo
    """
    os.system("cd ../brain-microservice/projects/emotion/scripts && python3 detect.py --source 0 --weights best4.onnx")

@router.get('/helmet-detector')
async def run_helmet():
    return {"message": "helmet detector"}