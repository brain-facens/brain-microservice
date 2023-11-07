from fastapi import APIRouter, BackgroundTasks
from starlette.responses import RedirectResponse
import httpx
from utils import *
from dotenv import load_dotenv
import os 
load_dotenv()

github_client_id = os.getenv('github_client_id')
github_client_secret = os.getenv('github_client_secret')
github_personal_access_token = os.getenv('github_personal_access_token')

cache_dir = './cache'

router = APIRouter(prefix='/dev', tags=['developer'])

@router.get('/github-login')
async def github_login():
    return RedirectResponse(f'https://github.com/login/oauth/authorize?client_id={github_client_id}', status_code=302)

@router.get('/github-code')
async def github_code(code: str):
    params = {
        'client_id': github_client_id,
        'client_secret': github_client_secret,
        'code': code
    }
    headers = {'Accept': 'application/json'}
    async with httpx.AsyncClient() as client:
        response = await client.post(url='https://github.com/login/oauth/access_token', params=params, headers=headers)
    response_json = response.json()
    access_token = response_json['access_token']
    async with httpx.AsyncClient() as client:
        headers.update({'Authorization': f'Bearer {access_token}'})
        response = await client.get('https://api.github.com/user', headers=headers)
    org_users = get_organization_members(org_name='brain-facens', access_token=github_personal_access_token)
    if response.json()['login'] in org_users:
        return "User successfully authenticated"
    else:
        return f"User: {response.json()['login']} is not part of the organization"
    
@router.get("/clone_repository")
async def clone_and_cache_repo(repo_url: str):
    # Create a directory for caching the repo
    cache_path = os.path.join(cache_dir, repo_url.split('/')[-1])
    
    # Check if the repo is already in the cache
    if os.path.exists(cache_path):
        return {"message": "Repository already cached"}
    
    # Clone the repository
    try:
        clone_repository(repo_url, cache_path)
        return {"message": "Repository cloned and cached"}
    except Exception as e:
        return {"message": f"Failed to clone the repository, error={str(e)}"}
    
@router.get("/cleanup_cache")
async def initiate_cleanup(background_tasks: BackgroundTasks):
    background_tasks.add_task(cleanup_cache(cache_dir=cache_dir))
    return {"message": "Cleanup initiated"}