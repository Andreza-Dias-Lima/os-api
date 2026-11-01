from src.database.session import (
    SessionLocal
)

from src.repositories.outbox_repository import (
    OutboxRepository
)

from src.integrations.event_publisher import (
    EventPublisher
)

from src.observability.logger import (
    logger
)

def processar_outbox():

    db = SessionLocal()

    try:

        repositorio = OutboxRepository(db)

        publisher = EventPublisher()

        eventos = repositorio.buscar_pendentes()

        print(
            f"Eventos encontrados: {len(eventos)}"
        )

        for evento in eventos:
            
            logger.info(
                f"Publicando evento "
                f"{evento.id}"
            )

            publisher.publish(
                evento
            )

            logger.info(
                f"Evento publicado "
                f"{evento.id}"
            )

            repositorio.marcar_como_publicado(
                evento
            )

    finally:

        db.close()