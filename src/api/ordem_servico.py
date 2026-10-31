from fastapi import APIRouter

router = APIRouter(
    prefix="/ordens-servico",
    tags=["Ordens de Serviço"]
)


@router.get("")
def listar():
    return []