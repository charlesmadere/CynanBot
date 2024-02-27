from abc import ABC, abstractmethod
from typing import Optional


class DeepLAuthKeyProviderInterface(ABC):

    @abstractmethod
    async def getDeepLAuthKey(self) -> Optional[str]:
        pass
