from datetime import datetime

from fastapi import APIRouter
from fastapi import Depends

from sqlalchemy.orm import Session

from src.database.dependencies import get_db
from src.models.ordem_servico import OrdemServico

from src.schemas.ordem_servico import (
    CriarOrdemServicoRequest
)

router = APIRouter(
    prefix="/ordens-servico",
    tags=["Ordens de Serviço"]
)

@router.post("")
def criar_ordem_servico(
    request: CriarOrdemServicoRequest,
    db: Session = Depends(get_db)
):

    ordem = OrdemServico(
        solicitante_id=request.solicitante_id,
        descricao=request.descricao,
        status="CRIADA",
        criado_em=datetime.utcnow()
    )

    db.add(ordem)

    db.commit()

    db.refresh(ordem)

    return ordem