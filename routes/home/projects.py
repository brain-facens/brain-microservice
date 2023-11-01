from fastapi import APIRouter

# rota onde os projetos serão transformados em API e aqui alocadas as suas execuções

router = APIRouter(prefix='/projects', tags=['projects'])

@router.get('/root')
async def projects_root():
    return {"message": "Hello from projects root page"}

@router.get('/helmet-detector')
async def run_helmet():
    return {"message": "Hello from helmet-detector project!"}