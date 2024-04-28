from abc import ABC, abstractmethod

from CynanBot.google.googleVoiceSelectionParams import \
    GoogleVoiceSelectionParams


class GoogleTtsVoiceChooserInterface(ABC):

    @abstractmethod
    async def choose(self) -> GoogleVoiceSelectionParams:
        pass
