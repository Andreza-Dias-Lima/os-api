class FakeDB:

    def commit(self):
        pass


class FakeRepository:

    def __init__(self):
        self.db = FakeDB()

    def criar(self, ordem):

        ordem.id = "ordem-123"

        return ordem


class FakeRequesterClient:

    def exists(
        self,
        requester_id: str
    ):

        return requester_id in [
            "123",
            "456",
            "789"
        ]


class FakeIdempotencyRepository:

    def __init__(self):
        self.registros = {}

    def buscar_por_chave(
        self,
        chave
    ):

        return self.registros.get(
            chave
        )

    def salvar(
        self,
        registro
    ):

        self.registros[
            registro.chave
        ] = registro


class FakeOutboxRepository:

    def criar(
        self,
        evento
    ):

        return evento