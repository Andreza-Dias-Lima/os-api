from sqlalchemy.orm import Session

from src.models.ordem_servico import OrdemServico


class OrdemServicoRepository:

    def __init__(self, db):
        self.db = db

    def criar(self, ordem):

        self.db.add(ordem)

        self.db.flush()

        self.db.refresh(ordem)

        return ordem