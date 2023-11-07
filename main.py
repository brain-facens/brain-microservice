from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import developer, client, demo, admin
from routes.home import projects, list, auth

app = FastAPI()

origins = ["http://127.0.0.1:5000"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(admin.router)
app.include_router(developer.router)
app.include_router(client.router)
app.include_router(demo.router)
app.include_router(projects.router)
app.include_router(list.router)
app.include_router(auth.router)