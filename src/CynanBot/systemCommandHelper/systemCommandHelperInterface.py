from abc import ABC, abstractmethod


class SystemCommandHelperInterface(ABC):

    @abstractmethod
    async def executeCommand(self, command: str, timeoutSeconds: float = 10):
        pass

    @abstractmethod
    async def executeVlcCommand(self, filePath: str):
        pass
