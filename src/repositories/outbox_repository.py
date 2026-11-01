from sqlalchemy.orm import Session

from src.models.outbox_event import (
    OutboxEvent
)


class OutboxRepository:

    def __init__(
        self,
        db: Session
    ):
        self.db = db

    def criar(
        self,
        evento: OutboxEvent
    ):

        self.db.add(evento)

        return evento