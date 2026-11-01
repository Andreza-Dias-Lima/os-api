from sqlalchemy.orm import Session

from src.models.ordem_servico import OrdemServico


class OrdemServicoRepository:

    def __init__(
        self,
        db: Session
    ):
        self.db = db

    def criar(
        self,
        ordem: OrdemServico
    ) -> OrdemServico:

        self.db.add(ordem)

        self.db.commit()

        self.db.refresh(ordem)

        return ordem