from fastapi import APIRouter, responses
import os  

# rota onde os projetos serão transformados em API e aqui alocadas as suas execuções

router = APIRouter(prefix='/projects', tags=['projects'])

@router.get('/emotion')
async def run_emotion():
    os.system("bash ../brain-microservice/scripts/emotion.sh")

@router.get('/brainTumorDetection')
async def run_tumor_detector():
    os.system("bash ../brain-microservice/scripts/tumor.sh")

@router.get('/notaFiscal')
async def run_nota_fiscal():
    os.system("bash ../brain-microservice/scripts/notafiscal.sh")