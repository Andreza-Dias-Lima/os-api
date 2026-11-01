from abc import ABC
from abc import abstractmethod


class RequesterClient(ABC):

    @abstractmethod
    def exists(
        self,
        requester_id: str
    ) -> bool:
        pass