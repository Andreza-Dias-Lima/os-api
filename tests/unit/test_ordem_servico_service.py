import pytest

from src.services.ordem_servico_service import (
    OrdemServicoService
)

from src.exceptions.not_found import (
    NotFoundException
)

from tests.unit.conftest import (
    FakeRepository,
    FakeRequesterClient,
    FakeIdempotencyRepository,
    FakeOutboxRepository
)


def test_deve_criar_ordem():

    service = OrdemServicoService(
        repository=FakeRepository(),
        requester_client=FakeRequesterClient(),
        idempotency_repository=FakeIdempotencyRepository(),
        outbox_repository=FakeOutboxRepository()
    )

    resultado = service.criar(
        solicitante_id="123",
        descricao="Troca de equipamento",
        idempotency_key="abc-123"
    )

    assert resultado["status"] == "CRIADA"

    assert resultado["solicitante_id"] == "123"

    assert resultado["id"] == "ordem-123"


def test_deve_lancar_excecao_para_solicitante_invalido():

    service = OrdemServicoService(
        repository=FakeRepository(),
        requester_client=FakeRequesterClient(),
        idempotency_repository=FakeIdempotencyRepository(),
        outbox_repository=FakeOutboxRepository()
    )

    with pytest.raises(
        NotFoundException
    ):

        service.criar(
            solicitante_id="999",
            descricao="Teste",
            idempotency_key="abc"
        )


def test_deve_retornar_resposta_existente():

    fake_repo = FakeIdempotencyRepository()

    class RegistroIdempotencia:

        def __init__(self):

            self.chave = "abc"

            self.resposta = {
                "id": "123",
                "status": "CRIADA"
            }

    fake_repo.registros["abc"] = (
        RegistroIdempotencia()
    )

    service = OrdemServicoService(
        repository=FakeRepository(),
        requester_client=FakeRequesterClient(),
        idempotency_repository=fake_repo,
        outbox_repository=FakeOutboxRepository()
    )

    resultado = service.criar(
        solicitante_id="123",
        descricao="Teste",
        idempotency_key="abc"
    )

    assert resultado["id"] == "123"

    assert resultado["status"] == "CRIADA"