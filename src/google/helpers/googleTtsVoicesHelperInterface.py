from abc import ABC, abstractmethod

from ..models.googleMultiSpeakerVoicePreset import GoogleMultiSpeakerVoicePreset
from ..models.googleVoicePreset import GoogleVoicePreset
from ...language.languageEntry import LanguageEntry


class GoogleTtsVoicesHelperInterface(ABC):

    @abstractmethod
    async def getEnglishMultiSpeakerVoice(self) -> GoogleMultiSpeakerVoicePreset:
        pass

    @abstractmethod
    async def getEnglishVoice(self) -> GoogleVoicePreset:
        pass

    @abstractmethod
    async def getVoiceForLanguage(
        self,
        languageEntry: LanguageEntry,
    ) -> GoogleVoicePreset | None:
        pass

    @abstractmethod
    async def getVoicesForLanguage(
        self,
        languageEntry: LanguageEntry,
    ) -> frozenset[GoogleVoicePreset]:
        pass
