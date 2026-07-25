from fastapi import FastAPI

from app.core.config import settings
from app.api.v1.database import router as database_router


app = FastAPI(
    title=settings.APP_NAME,
    version = settings.APP_VERSION
)

app.include_router(database_router)

@app.get("/")
async def root():

    return{
        "message": "Welcome Home"
    }

@app.get("/health")
async def health():
    return{
        "status": "healthy"}
