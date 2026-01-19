from abc import ABC, abstractmethod
from typing import Any, Collection

from ..accessToken.googleAccessToken import GoogleAccessToken
from ..models.absGoogleTextSynthesisInput import AbsGoogleTextSynthesisInput
from ..models.absGoogleVoicePreset import AbsGoogleVoicePreset
from ..models.googleMultiSpeakerMarkup import GoogleMultiSpeakerMarkup
from ..models.googleMultiSpeakerMarkupTurn import GoogleMultiSpeakerMarkupTurn
from ..models.googleScope import GoogleScope
from ..models.googleTextSynthesisResponse import GoogleTextSynthesisResponse
from ..models.googleTextSynthesizeRequest import GoogleTextSynthesizeRequest
from ..models.googleTranslateTextGlossaryConfig import GoogleTranslateTextGlossaryConfig
from ..models.googleTranslateTextResponse import GoogleTranslateTextResponse
from ..models.googleTranslateTextTransliterationConfig import GoogleTranslateTextTransliterationConfig
from ..models.googleTranslation import GoogleTranslation
from ..models.googleTranslationRequest import GoogleTranslationRequest
from ..models.googleVoiceAudioConfig import GoogleVoiceAudioConfig
from ..models.googleVoiceAudioEncoding import GoogleVoiceAudioEncoding
from ..models.googleVoiceGender import GoogleVoiceGender
from ..models.googleVoiceSelectionParams import GoogleVoiceSelectionParams


class GoogleJsonMapperInterface(ABC):

    @abstractmethod
    async def parseAccessToken(
        self,
        jsonContents: dict[str, Any] | Any | None,
    ) -> GoogleAccessToken | None:
        pass

    @abstractmethod
    async def parseTextSynthesisResponse(
        self,
        jsonContents: dict[str, Any] | Any | None,
    ) -> GoogleTextSynthesisResponse | None:
        pass

    @abstractmethod
    async def parseTranslateTextGlossaryConfig(
        self,
        jsonContents: dict[str, Any] | Any | None
    ) -> GoogleTranslateTextGlossaryConfig | None:
        pass

    @abstractmethod
    async def parseTranslateTextResponse(
        self,
        jsonContents: dict[str, Any] | Any | None,
    ) -> GoogleTranslateTextResponse | None:
        pass

    @abstractmethod
    async def parseTranslation(
        self,
        jsonContents: dict[str, Any] | Any | None,
    ) -> GoogleTranslation | None:
        pass

    @abstractmethod
    async def parseVoiceAudioConfig(
        self,
        jsonContents: dict[str, Any] | Any | None,
    ) -> GoogleVoiceAudioConfig | None:
        pass

    @abstractmethod
    async def parseVoiceAudioEncoding(
        self,
        jsonString: str | Any | None,
    ) -> GoogleVoiceAudioEncoding | None:
        pass

    @abstractmethod
    async def parseVoiceGender(
        self,
        jsonString: str | Any | None,
    ) -> GoogleVoiceGender | None:
        pass

    @abstractmethod
    async def parseVoicePreset(
        self,
        jsonString: str | Any | None,
    ) -> AbsGoogleVoicePreset | None:
        pass

    @abstractmethod
    async def requireVoiceAudioEncoding(
        self,
        jsonString: str | Any | None,
    ) -> GoogleVoiceAudioEncoding:
        pass

    @abstractmethod
    async def requireVoicePreset(
        self,
        jsonString: str | Any | None,
    ) -> AbsGoogleVoicePreset:
        pass

    @abstractmethod
    async def serializeGlossaryConfig(
        self,
        glossaryConfig: GoogleTranslateTextGlossaryConfig,
    ) -> dict[str, Any]:
        pass

    @abstractmethod
    async def serializeMultiSpeakerMarkupTurn(
        self,
        markupTurn: GoogleMultiSpeakerMarkupTurn,
    ) -> dict[str, Any]:
        pass

    @abstractmethod
    async def serializeMultiSpeakerMarkup(
        self,
        markup: GoogleMultiSpeakerMarkup,
    ) -> dict[str, Any]:
        pass

    @abstractmethod
    async def serializeScope(
        self,
        scope: GoogleScope,
    ) -> str:
        pass

    @abstractmethod
    async def serializeScopes(
        self,
        scopes: Collection[GoogleScope],
    ) -> str:
        pass

    @abstractmethod
    async def serializeTextSynthesisInput(
        self,
        synthesisInput: AbsGoogleTextSynthesisInput,
    ) -> dict[str, Any]:
        pass

    @abstractmethod
    async def serializeTextSynthesizeRequest(
        self,
        synthesizeRequest: GoogleTextSynthesizeRequest,
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
        voiceGender: GoogleVoiceGender,
    ) -> str:
        pass

    @abstractmethod
    async def serializeVoicePreset(
        self,
        voicePreset: AbsGoogleVoicePreset,
    ) -> str:
        pass

    @abstractmethod
    async def serializeVoiceSelectionParams(
        self,
        voiceSelectionParams: GoogleVoiceSelectionParams,
    ) -> dict[str, Any]:
        pass
