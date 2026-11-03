import uuid

from datetime import datetime
from datetime import UTC

from sqlalchemy import String
from sqlalchemy import DateTime
from sqlalchemy import Boolean
from sqlalchemy import JSON

from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from src.database.base import Base


class OutboxEvent(Base):

    __tablename__ = "outbox_events"

    id: Mapped[str] = mapped_column(
        String,
        primary_key=True,
        default=lambda: str(uuid.uuid4())
    )

    event_type: Mapped[str] = mapped_column(
        String(100)
    )

    payload: Mapped[dict] = mapped_column(
        JSON
    )

    published: Mapped[bool] = mapped_column(
        Boolean,
        default=False
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.now(UTC)
    )

    published_at: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True
    )