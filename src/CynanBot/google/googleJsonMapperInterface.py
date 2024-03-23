from abc import ABC, abstractmethod
from typing import Any

from CynanBot.google.googleAccessToken import GoogleAccessToken
from CynanBot.google.googleScope import GoogleScope
from CynanBot.google.googleTextSynthesisInput import GoogleTextSynthesisInput
from CynanBot.google.googleTextSynthesisResponse import \
    GoogleTextSynthesisResponse
from CynanBot.google.googleTextSynthesizeRequest import \
    GoogleTextSynthesizeRequest
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
from CynanBot.google.googleVoiceGender import GoogleVoiceGender
from CynanBot.google.googleVoiceSelectionParams import \
    GoogleVoiceSelectionParams


class GoogleJsonMapperInterface(ABC):

    @abstractmethod
    async def parseAccessToken(
        self,
        jsonContents: dict[str, Any] | None
    ) -> GoogleAccessToken | None:
        pass

    @abstractmethod
    async def parseTextSynthesisResponse(
        self,
        jsonContents: dict[str, Any] | None
    ) -> GoogleTextSynthesisResponse | None:
        pass

    @abstractmethod
    async def parseTranslateTextGlossaryConfig(
        self,
        jsonContents: dict[str, Any] | None
    ) -> GoogleTranslateTextGlossaryConfig | None:
        pass

    @abstractmethod
    async def parseTranslateTextResponse(
        self,
        jsonContents: dict[str, Any] | None
    ) -> GoogleTranslateTextResponse | None:
        pass

    @abstractmethod
    async def parseTranslation(
        self,
        jsonContents: dict[str, Any] | None
    ) -> GoogleTranslation | None:
        pass

    @abstractmethod
    async def parseVoiceAudioConfig(
        self,
        jsonContents: dict[str, Any] | None
    ) -> GoogleVoiceAudioConfig | None:
        pass

    @abstractmethod
    async def parseVoiceAudioEncoding(
        self,
        jsonString: str | None
    ) -> GoogleVoiceAudioEncoding | None:
        pass

    @abstractmethod
    async def parseVoiceGender(
        self,
        jsonString: str | None
    ) -> GoogleVoiceGender | None:
        pass

    @abstractmethod
    async def serializeGlossaryConfig(
        self,
        glossaryConfig: GoogleTranslateTextGlossaryConfig
    ) -> dict[str, Any]:
        pass

    @abstractmethod
    async def serializeSynthesizeRequest(
        self,
        synthesizeRequest: GoogleTextSynthesizeRequest
    ) -> dict[str, Any]:
        pass

    @abstractmethod
    async def serializeScope(
        self,
        scope: GoogleScope
    ) -> str:
        pass

    @abstractmethod
    async def serializeTextSynthesisInput(
        self,
        textSynthesisInput: GoogleTextSynthesisInput
    ) -> dict[str, Any]:
        pass

    @abstractmethod
    async def serializeTranslationRequest(
        self,
        translationRequest: GoogleTranslationRequest
    ) -> dict[str, Any]:
        pass

    @abstractmethod
    async def serializeTransliterationConfig(
        self,
        transliterationConfig: GoogleTranslateTextTransliterationConfig
    ) -> dict[str, Any]:
        pass

    @abstractmethod
    async def serializeVoiceAudioConfig(
        self,
        voiceAudioConfig: GoogleVoiceAudioConfig
    ) -> dict[str, Any]:
        pass

    @abstractmethod
    async def serializeVoiceAudioEncoding(
        self,
        voiceAudioEncoding: GoogleVoiceAudioEncoding
    ) -> str:
        pass

    @abstractmethod
    async def serializeVoiceGender(
        self,
        voiceGender: GoogleVoiceGender
    ) -> str:
        pass

    @abstractmethod
    async def serializeVoiceSelectionParams(
        self,
        voiceSelectionParams: GoogleVoiceSelectionParams
    ) -> dict[str, Any]:
        pass
