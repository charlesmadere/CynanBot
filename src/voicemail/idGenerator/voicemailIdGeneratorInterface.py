from abc import ABC, abstractmethod


class VoicemailIdGeneratorInterface(ABC):

    @abstractmethod
    async def generateVoicemailId(self) -> str:
        pass
