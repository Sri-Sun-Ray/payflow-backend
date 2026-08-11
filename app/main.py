from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings

from app.modules.auth.router import router as auth_router
from app.modules.payments.router import router as payments_router



app = FastAPI(
    title=settings.APP_NAME,
    version = settings.APP_VERSION
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(payments_router)

@app.get("/")
async def root():

    return{
        "message": "Welcome Home"
    }

@app.get("/health")
async def health():
    return{
        "status": "healthy"}
