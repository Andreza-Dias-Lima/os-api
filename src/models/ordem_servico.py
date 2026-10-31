import uuid

from sqlalchemy import String

from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from src.database.base import Base


class OrdemServico(Base):

    __tablename__ = "ordens_servico"

    id: Mapped[str] = mapped_column(
        String,
        primary_key=True,
        default=lambda: str(uuid.uuid4())
    )

    descricao: Mapped[str] = mapped_column(
        String(500)
    )