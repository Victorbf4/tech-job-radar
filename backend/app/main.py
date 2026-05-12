from fastapi import APIRouter, FastAPI
from sqlalchemy import text
from fastapi.middleware.cors import CORSMiddleware

from app.db.session import db
from app.api.endpoints.jobs import router as jobs_router

app = FastAPI(
    title="Tech Job Radar API",
    description="API para el análisis y seguimiento de ofertas de trabajo tecnológicas",
    version="0.1.0"
)

api_router = APIRouter(prefix="/api")
api_router.include_router(jobs_router)
app.include_router(api_router)

# Configuración de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Ajustar en producción
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Bienvenido a Tech Job Radar API"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.get("/db/ping")
async def db_ping():
    async for session in db.get_session():
        result = await session.execute(text("SELECT 1"))
        value = result.scalar_one()
        return {"db": "ok", "result": value}
