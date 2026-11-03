import uuid

from datetime import datetime
from datetime import UTC

from sqlalchemy import String
from sqlalchemy import DateTime
from sqlalchemy import JSON

from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from src.database.base import Base


class IdempotencyKey(Base):

    __tablename__ = "idempotency_keys"

    id: Mapped[str] = mapped_column(
        String,
        primary_key=True,
        default=lambda: str(uuid.uuid4())
    )

    chave: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        nullable=False
    )

    ordem_servico_id: Mapped[str] = mapped_column(
        String
    )

    resposta: Mapped[dict] = mapped_column(
        JSON
    )

    criado_em: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.now(UTC)
    )