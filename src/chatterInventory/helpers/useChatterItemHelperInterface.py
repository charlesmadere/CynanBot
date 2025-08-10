from abc import ABC, abstractmethod

from ..models.useChatterItemRequest import UseChatterItemRequest
from ..models.useChatterItemResult import UseChatterItemResult


class UseChatterItemHelperInterface(ABC):

    @abstractmethod
    async def useItem(self, request: UseChatterItemRequest) -> UseChatterItemResult:
        pass
