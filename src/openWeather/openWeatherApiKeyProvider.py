from abc import ABC, abstractmethod


class OpenWeatherApiKeyProvider(ABC):

    @abstractmethod
    async def getOpenWeatherApiKey(self) -> str | None:
        pass
