from sqlalchemy.orm import Session

from src.models.idempotency_key import (
    IdempotencyKey
)


class IdempotencyRepository:

    def __init__(
        self,
        db: Session
    ):
        self.db = db

    def buscar_por_chave(
        self,
        chave: str
    ):

        return (
            self.db.query(
                IdempotencyKey
            )
            .filter(
                IdempotencyKey.chave == chave
            )
            .first()
        )

    def salvar(
        self,
        registro: IdempotencyKey
    ):
        self.db.add(registro)