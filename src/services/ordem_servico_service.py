from datetime import datetime
from datetime import UTC

from src.models.ordem_servico import OrdemServico

from src.models.idempotency_key import (
    IdempotencyKey
)

from src.exceptions.not_found import (
    NotFoundException
)

from src.observability.logger import (
    logger
)

from src.observability.correlation import (
    correlation_id
)

class OrdemServicoService:

    def __init__(
        self,
        repository,
        requester_client,
        idempotency_repository,
        outbox_repository
    ):

        self.repository = repository
        self.requester_client = requester_client
        self.idempotency_repository = (
            idempotency_repository
        )
        self.outbox_repository = (
            outbox_repository
        )

    def criar(
        self,
        solicitante_id: str,
        descricao: str,
        idempotency_key: str
    ):

        # Verifica se a requisição já foi processada
        registro_existente = (
            self.idempotency_repository
            .buscar_por_chave(
                idempotency_key
            )
        )

        if registro_existente:
            return registro_existente.resposta

        # Valida solicitante
        if not self.requester_client.exists(
            solicitante_id
        ):
            raise NotFoundException()

        # Cria a ordem
        ordem = OrdemServico(
            solicitante_id=solicitante_id,
            descricao=descricao,
            status="CRIADA",
            criado_em=datetime.now(UTC)
        )

        ordem = self.repository.criar(
            ordem
        )

        logger.info(
            f"Ordem criada: {ordem.id}"
        )

        from src.models.outbox_event import ( OutboxEvent )

        # Cria evento de outbox
        evento = OutboxEvent(
            event_type="ORDEM_SERVICO_CRIADA",
            payload={
                "correlation_id": correlation_id.get(),
                "ordem_id": ordem.id,
                "solicitante_id": ordem.solicitante_id,
                "status": ordem.status
                }
            )

        self.outbox_repository.criar( evento )

        logger.info(
            f"Evento criado: "
            f"{evento.id}"
        )

        # Monta resposta
        resposta = {
            "id": ordem.id,
            "solicitante_id": ordem.solicitante_id,
            "descricao": ordem.descricao,
            "status": ordem.status
        }

        # Registra chave de idempotência
        registro = IdempotencyKey(
            chave=idempotency_key,
            ordem_servico_id=ordem.id,
            resposta=resposta
        )

        self.idempotency_repository.salvar(
            registro
        )

        # Persistência da chave
        self.repository.db.commit()

        return resposta