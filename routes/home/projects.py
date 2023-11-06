from fastapi import APIRouter, responses
from fastapi.responses import HTMLResponse
import os  
from bs4 import BeautifulSoup

# rota onde os projetos serão transformados em API e aqui alocadas as suas execuções

"""
Projetos:
    - Tumor (docker)
    - Area delimitada (pegar projeto no PCzao, dentro pasta YOLO)
    - OCR Notas (docker)
    - emotion (local)
"""

router = APIRouter(prefix='/projects', tags=['projects'])

@router.get('/interface')
async def run_interface():
    redirect_url = "http://127.0.0.1:5000/home"
    try:
        response = responses.RedirectResponse(url=redirect_url)
        return response
    except Exception as e:
        return {"message": f"Exception: {str(e)}"}

@router.get('/emotion')
async def run_emotion():
    os.system("bash ../brain-microservice/scripts/emotion.sh")

@router.get('/ocr-notas')
async def run_ocr_notas():
    return {"message": "Hello from ocr-notas"}

@router.get('/tumor-detector')
async def run_tumor_detector():
    return {"message": "Hello from tumor-detector"}

@router.get('/area-delimitada')
async def run_area_delimitada():
    return {"message": "Hello from area delimitada"}