from fastapi import APIRouter, responses
import os  

# rota onde os projetos serão transformados em API e aqui alocadas as suas execuções

"""
Projetos:
    - Tumor (docker)
    - Area delimitada (pegar projeto no PCzao, dentro pasta YOLO)
    - OCR Notas (docker)
    - emotion (local)
"""

router = APIRouter(prefix='/projects', tags=['projects'])

@router.get('/emotion')
async def run_emotion():
    os.system("bash ../brain-microservice/scripts/emotion.sh")
    redirect_url = "http://127.0.0.1:5000"
    response = responses.RedirectResponse(url=redirect_url)
    return response

@router.get('/ocr-notas')
async def run_ocr_notas():
    return {"message": "Hello from ocr-notas"}

@router.get('/tumor-detector')
async def run_tumor_detector():
    return {"message": "Hello from tumor-detector"}

@router.get('/area-delimitada')
async def run_area_delimitada():
    return {"message": "Hello from area delimitada"}