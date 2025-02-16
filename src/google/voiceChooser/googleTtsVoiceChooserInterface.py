from abc import ABC, abstractmethod

from ..models.googleVoiceSelectionParams import GoogleVoiceSelectionParams


class GoogleTtsVoiceChooserInterface(ABC):

    @abstractmethod
    async def choose(self) -> GoogleVoiceSelectionParams:
        pass
