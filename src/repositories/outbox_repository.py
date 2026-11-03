from datetime import datetime
from datetime import UTC
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

    def buscar_pendentes(
        self
    ):
        return (
            self.db.query(
                OutboxEvent
            )
            .filter(
                OutboxEvent.published.is_(False)
            )
            .all()
        )

    def marcar_como_publicado(
        self,
        evento: OutboxEvent
    ):
        evento.published = True

        evento.published_at = (
            datetime.now(UTC)
        )

        self.db.commit()