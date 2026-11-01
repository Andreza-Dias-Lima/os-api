from datetime import datetime

from src.models.ordem_servico import OrdemServico

from src.models.idempotency_key import (
    IdempotencyKey
)

from src.exceptions.not_found import (
    NotFoundException
)


class OrdemServicoService:

    def __init__(
        self,
        repository,
        requester_client,
        idempotency_repository
    ):
        self.repository = repository
        self.requester_client = requester_client
        self.idempotency_repository = (
            idempotency_repository
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
            criado_em=datetime.utcnow()
        )

        ordem = self.repository.criar(
            ordem
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