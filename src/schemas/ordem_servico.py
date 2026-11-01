from pydantic import BaseModel


class OrdemServicoResponse(BaseModel):

    id: str

    solicitante_id: str

    descricao: str

    status: str

    class Config:
        from_attributes = True