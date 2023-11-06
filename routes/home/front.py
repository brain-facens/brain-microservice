from fastapi import APIRouter, responses

router = APIRouter(prefix='/interface', tags=['interface'])

@router.get('/')
async def run_interface():
    redirect_url = "http://127.0.0.1:5000"
    try:
        response = responses.RedirectResponse(url=redirect_url)
        return response
    except Exception as e:
        return {"message": f"Exception: {str(e)}"}