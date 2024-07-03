from abc import ABC, abstractmethod
from typing import Any

from .googleAccessToken import GoogleAccessToken
from .googleScope import GoogleScope
from .googleTextSynthesisInput import GoogleTextSynthesisInput
from .googleTextSynthesisResponse import GoogleTextSynthesisResponse
from .googleTextSynthesizeRequest import GoogleTextSynthesizeRequest
from .googleTranslateTextGlossaryConfig import GoogleTranslateTextGlossaryConfig
from .googleTranslateTextResponse import GoogleTranslateTextResponse
from .googleTranslateTextTransliterationConfig import GoogleTranslateTextTransliterationConfig
from .googleTranslation import GoogleTranslation
from .googleTranslationRequest import GoogleTranslationRequest
from .googleVoiceAudioConfig import GoogleVoiceAudioConfig
from .googleVoiceAudioEncoding import GoogleVoiceAudioEncoding
from .googleVoiceGender import GoogleVoiceGender
from .googleVoiceSelectionParams import GoogleVoiceSelectionParams


class GoogleJsonMapperInterface(ABC):

    @abstractmethod
    async def parseAccessToken(
        self,
        jsonContents: dict[str, Any] | None | Any
    ) -> GoogleAccessToken | None:
        pass

    @abstractmethod
    async def parseTextSynthesisResponse(
        self,
        jsonContents: dict[str, Any] | None | Any
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
        jsonContents: dict[str, Any] | None | Any
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
    async def serializeScopes(
        self,
        scopes: list[GoogleScope]
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
