from fastapi import FastAPI
from routes import developer, client, demo, admin
from routes.home import projects, list, auth 

app = FastAPI()

app.include_router(admin.router)
app.include_router(developer.router)
app.include_router(client.router)
app.include_router(demo.router)
app.include_router(projects.router)
app.include_router(list.router)
app.include_router(auth.router)