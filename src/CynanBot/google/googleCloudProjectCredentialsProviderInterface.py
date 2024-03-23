from abc import ABC, abstractmethod


class GoogleCloudProjectCredentialsProviderInterface(ABC):

    @abstractmethod
    async def getGoogleCloudApiKey(self) -> str | None:
        pass

    @abstractmethod
    async def getGoogleCloudProjectKeyId(self) -> str | None:
        pass

    @abstractmethod
    async def getGoogleCloudProjectId(self) -> str | None:
        pass

    @abstractmethod
    async def getGoogleCloudProjectPrivateKey(self) -> str | None:
        pass

    @abstractmethod
    async def getGoogleCloudServiceAccountEmail(self) -> str | None:
        pass
