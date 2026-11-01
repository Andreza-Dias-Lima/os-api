from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException

from sqlalchemy.orm import Session

from src.database.dependencies import get_db

from src.repositories.ordem_servico_repository import (
    OrdemServicoRepository
)

from src.schemas.ordem_servico import (
    CriarOrdemServicoRequest
)

from src.services.ordem_servico_service import (
    OrdemServicoService
)

from src.integrations.fake_requester_client import (
    FakeRequesterClient
)

from src.exceptions.not_found import (
    NotFoundException
)

from fastapi import Header

from src.repositories.idempotency_repository import (
    IdempotencyRepository
)

router = APIRouter(
    prefix="/ordens-servico",
    tags=["Ordens de Serviço"]
)


@router.post("")
def criar_ordem_servico(
    request: CriarOrdemServicoRequest,
    db: Session = Depends(get_db),
    idempotency_key: str = Header(...)
):
    idempotency_repository = (
        IdempotencyRepository(db)
    )

    repository = OrdemServicoRepository(db)

    requester_client = FakeRequesterClient()

    service = OrdemServicoService(
        repository=repository,
        requester_client=requester_client,
        idempotency_repository=idempotency_repository
    )

    try:

        return service.criar(
            solicitante_id=request.solicitante_id,
            descricao=request.descricao,
            idempotency_key=idempotency_key
        )

    except NotFoundException as ex:

        raise HTTPException(
            status_code=404,
            detail=str(ex)
        )