from pydantic import BaseModel
from pydantic import Field


class CriarOrdemServicoRequest(BaseModel):

    solicitante_id: str

    descricao: str = Field(
        min_length=3,
        max_length=500
    )


class OrdemServicoResponse(BaseModel):

    id: str

    solicitante_id: str

    descricao: str

    status: str

    class Config:
        from_attributes = True