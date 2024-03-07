from abc import ABC, abstractmethod
from typing import Optional


class OneWeatherApiKeyProvider(ABC):

    @abstractmethod
    async def getOneWeatherApiKey(self) -> Optional[str]:
        pass
