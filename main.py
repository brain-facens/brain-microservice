from fastapi import FastAPI, responses
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os 
from os.path import join, dirname 
import uvicorn

from routes import client, admin
from routes.home import projects, list, auth
from api_analytics.fastapi import Analytics

dotenv_path = join(dirname(__file__), ".env")
load_dotenv(dotenv_path)

token = os.getenv("token")

app = FastAPI()

app.add_middleware(Analytics, api_key=token)

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