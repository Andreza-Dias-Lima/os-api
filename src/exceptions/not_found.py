class NotFoundException(Exception):

     def __init__(self):

        self.type = (
            "/errors/not-found"
        )

        self.title = (
            "Solicitante não encontrado"
        )

        self.status = 404

        self.detail = (
            "O solicitante informado não existe"
        )

        super().__init__(self.detail)