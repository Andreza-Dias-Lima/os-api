from datetime import datetime

from src.models.ordem_servico import OrdemServico

from src.exceptions.not_found import (
    NotFoundException
)


class OrdemServicoService:

    def __init__(
        self,
        repository,
        requester_client
    ):
        self.repository = repository
        self.requester_client = requester_client

    def criar(
        self,
        solicitante_id: str,
        descricao: str
    ):

        if not self.requester_client.exists(
            solicitante_id
        ):
            raise NotFoundException()

        ordem = OrdemServico(
            solicitante_id=solicitante_id,
            descricao=descricao,
            status="CRIADA",
            criado_em=datetime.utcnow()
        )

        return self.repository.criar(ordem)