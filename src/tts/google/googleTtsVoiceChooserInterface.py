from abc import ABC, abstractmethod

from ...google.googleVoiceSelectionParams import GoogleVoiceSelectionParams


class GoogleTtsVoiceChooserInterface(ABC):

    @abstractmethod
    async def choose(self) -> GoogleVoiceSelectionParams:
        pass
