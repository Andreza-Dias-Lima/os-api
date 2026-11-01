class EventPublisher:

    def publish(
        self,
        evento
    ):

        print(
            f"Publicando evento: "
            f"{evento.event_type}"
        )

        return True