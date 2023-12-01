from fastapi import FastAPI
from dotenv import load_dotenv
import os
from os.path import join, dirname
import uvicorn
from slowapi.errors import RateLimitExceeded
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address

from routes import client, admin
from routes.home import projects, list, auth
from api_analytics.fastapi import Analytics

dotenv_path = join(dirname(__file__), ".env")
load_dotenv(dotenv_path)

token = os.getenv("token")

app = FastAPI()

app.add_middleware(Analytics, api_key=token)

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter 
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

@app.get("/")
async def root():
    return {"message": "Nothing here. Try accessing <address>/docs"}

app.include_router(admin.router)
app.include_router(client.router)
app.include_router(projects.router)
app.include_router(list.router)
app.include_router(auth.router)

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
