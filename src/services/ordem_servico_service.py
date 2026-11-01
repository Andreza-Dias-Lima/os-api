from datetime import datetime

from src.models.ordem_servico import OrdemServico
from src.repositories.ordem_servico_repository import (
    OrdemServicoRepository
)


class OrdemServicoService:

    def __init__(
        self,
        repository: OrdemServicoRepository
    ):
        self.repository = repository

    def criar(
        self,
        solicitante_id: str,
        descricao: str
    ):

        ordem = OrdemServico(
            solicitante_id=solicitante_id,
            descricao=descricao,
            status="CRIADA",
            criado_em=datetime.utcnow()
        )

        return self.repository.criar(ordem)