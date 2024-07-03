from abc import ABC, abstractmethod

from ...google.googleVoiceAudioEncoding import GoogleVoiceAudioEncoding


class GoogleFileExtensionHelperInterface(ABC):

    @abstractmethod
    async def getFileExtension(self, audioEncoding: GoogleVoiceAudioEncoding) -> str:
        pass
