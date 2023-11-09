from fastapi import FastAPI, responses
from fastapi.middleware.cors import CORSMiddleware
from routes import client, admin
from routes.home import projects, list, auth
from api_analytics.fastapi import Analytics

app = FastAPI()

origins = ["http://127.0.0.1:5000"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(Analytics, api_key="a524dbc5-e15e-4d3f-a8de-bc55ada55977")

@app.get("/")
async def root():
    return {"message": "Nothing here. Try accessing <address>/docs"}

@app.get("/dashboard")
async def connect_dashboard():
    redirect_url = "https://www.apianalytics.dev/dashboard/885be5bc407e49d9b73c0d5f85086390"
    try:
        response = responses.RedirectResponse(url=redirect_url)
        return response
    except Exception as e:
        return {"message": f"Exception: {str(e)}"}

app.include_router(admin.router)
app.include_router(client.router)
app.include_router(projects.router)
app.include_router(list.router)
app.include_router(auth.router)