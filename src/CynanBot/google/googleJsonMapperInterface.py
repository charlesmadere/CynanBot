from abc import ABC, abstractmethod
from typing import Any, Dict, Optional

from CynanBot.google.googleTextSynthesisResponse import \
    GoogleTextSynthesisResponse
from CynanBot.google.googleTranslateTextGlossaryConfig import \
    GoogleTranslateTextGlossaryConfig
from CynanBot.google.googleTranslateTextResponse import \
    GoogleTranslateTextResponse
from CynanBot.google.googleTranslateTextTransliterationConfig import \
    GoogleTranslateTextTransliterationConfig
from CynanBot.google.googleTranslation import GoogleTranslation
from CynanBot.google.googleTranslationRequest import GoogleTranslationRequest
from CynanBot.google.googleVoiceAudioConfig import GoogleVoiceAudioConfig
from CynanBot.google.googleVoiceAudioEncoding import GoogleVoiceAudioEncoding


class GoogleJsonMapperInterface(ABC):

    @abstractmethod
    async def parseTextSynthesisResponse(
        self,
        jsonContents: Optional[Dict[str, Any]]
    ) -> Optional[GoogleTextSynthesisResponse]:
        pass

    @abstractmethod
    async def parseTranslateTextGlossaryConfig(
        self,
        jsonContents: Optional[Dict[str, Any]]
    ) -> Optional[GoogleTranslateTextGlossaryConfig]:
        pass

    @abstractmethod
    async def parseTranslateTextResponse(
        self,
        jsonContents: Optional[Dict[str, Any]]
    ) -> Optional[GoogleTranslateTextResponse]:
        pass

    @abstractmethod
    async def parseTranslation(
        self,
        jsonContents: Optional[Dict[str, Any]]
    ) -> Optional[GoogleTranslation]:
        pass

    @abstractmethod
    async def parseVoiceAudioConfig(
        self,
        jsonContents: Optional[Dict[str, Any]]
    ) -> Optional[GoogleVoiceAudioConfig]:
        pass

    @abstractmethod
    async def parseVoiceAudioEncoding(
        self,
        jsonString: Optional[str]
    ) -> Optional[GoogleVoiceAudioEncoding]:
        pass

    @abstractmethod
    async def serializeGlossaryConfig(
        self,
        glossaryConfig: GoogleTranslateTextGlossaryConfig
    ) -> Dict[str, Any]:
        pass

    @abstractmethod
    async def serializeTranslationRequest(
        self,
        translationRequest: GoogleTranslationRequest
    ) -> Dict[str, Any]:
        pass

    @abstractmethod
    async def serializeTransliterationConfig(
        self,
        transliterationConfig: GoogleTranslateTextTransliterationConfig
    ) -> Dict[str, Any]:
        pass
