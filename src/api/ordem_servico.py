from datetime import datetime

from fastapi import APIRouter
from fastapi import Depends

from sqlalchemy.orm import Session

from src.database.dependencies import get_db
from src.models.ordem_servico import OrdemServico

from src.repositories.ordem_servico_repository import OrdemServicoRepository
from src.schemas.ordem_servico import (
    CriarOrdemServicoRequest
)
from src.services.ordem_servico_service import OrdemServicoService

router = APIRouter(
    prefix="/ordens-servico",
    tags=["Ordens de Serviço"]
)

@router.post("")
def criar_ordem_servico(
    request: CriarOrdemServicoRequest,
    db: Session = Depends(get_db)
):

    repository = OrdemServicoRepository(db)

    service = OrdemServicoService(
        repository
    )

    return service.criar(
        solicitante_id=request.solicitante_id,
        descricao=request.descricao
    )