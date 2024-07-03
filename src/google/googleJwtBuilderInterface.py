from abc import ABC, abstractmethod


class GoogleJwtBuilderInterface(ABC):

    @abstractmethod
    async def buildJwt(self) -> str:
        pass
