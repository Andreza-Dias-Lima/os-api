from fastapi import FastAPI

from sqlalchemy import text

from src.database.base import Base
from src.database.session import engine

from src.models.ordem_servico import OrdemServico


app = FastAPI(
    title="API Ordem de Serviço",
    version="1.0.0"
)


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }


@app.get("/db-check")
def db_check():

    with engine.connect() as conn:

        result = conn.execute(
            text("SELECT 1")
        )

        return {
            "database": "connected",
            "result": result.scalar()
        }