from fastapi import FastAPI

from sqlalchemy import text

from src.database.base import Base
from src.database.session import engine

from src.models.ordem_servico import OrdemServico
from src.api.ordem_servico import router

from src.middlewares.exception_handler import (
    requester_not_found_handler
)

from src.exceptions.not_found import (
    NotFoundException
)

app = FastAPI(
    title="API Ordem de Serviço",
    version="1.0.0"
)

app.add_exception_handler(
    NotFoundException,
    requester_not_found_handler
)

app.include_router(
    router
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