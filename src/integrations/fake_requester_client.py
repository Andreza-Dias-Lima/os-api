from src.integrations.requester_client import (
    RequesterClient
)


class FakeRequesterClient(
    RequesterClient
):

    def exists(
        self,
        requester_id: str
    ) -> bool:

        valid_requesters = {
            "123",
            "456",
            "789"
        }

        return requester_id in valid_requesters