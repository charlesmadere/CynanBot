from typing import Any, Final

from frozenlist import FrozenList

from .deepLJsonMapperInterface import DeepLJsonMapperInterface
from .deepLTranslationRequest import DeepLTranslationRequest
from .deepLTranslationResponse import DeepLTranslationResponse
from .deepLTranslationResponses import DeepLTranslationResponses
from ..language.languageEntry import LanguageEntry
from ..language.languagesRepositoryInterface import LanguagesRepositoryInterface
from ..misc import utils as utils
from ..timber.timberInterface import TimberInterface


class DeepLJsonMapper(DeepLJsonMapperInterface):

    def __init__(
        self,
        languagesRepository: LanguagesRepositoryInterface,
        timber: TimberInterface,
    ):
        if not isinstance(languagesRepository, LanguagesRepositoryInterface):
            raise TypeError(f'languagesRepository argument is malformed: \"{languagesRepository}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')

        self.__languagesRepository: Final[LanguagesRepositoryInterface] = languagesRepository
        self.__timber: Final[TimberInterface] = timber

    async def parseTranslationResponse(
        self,
        jsonContents: dict[str, Any] | Any | None,
    ) -> DeepLTranslationResponse | None:
        if not isinstance(jsonContents, dict) or len(jsonContents) == 0:
            return None

        if not utils.isValidStr(jsonContents.get('text')):
            return None

        text = utils.getStrFromDict(jsonContents, 'text')

        detectedSourceLanguage: LanguageEntry | None = None
        if 'detected_source_language' in jsonContents:
            detectedSourceLanguageString = jsonContents.get('detected_source_language')

            if utils.isValidStr(detectedSourceLanguageString):
                detectedSourceLanguage = await self.__languagesRepository.getLanguageForCommand(
                    command = detectedSourceLanguageString,
                    hasIso6391Code = True,
                )

                if detectedSourceLanguage is None:
                    self.__timber.log('DeepLJsonMapper', f'Encountered detectedSourceLanguage that has no corresponding LanguageEntry ({detectedSourceLanguageString=}) ({jsonContents=})')

        return DeepLTranslationResponse(
            detectedSourceLanguage = detectedSourceLanguage,
            text = text,
        )

    async def parseTranslationResponses(
        self,
        jsonContents: dict[str, Any] | Any | None,
    ) -> DeepLTranslationResponses | None:
        if not isinstance(jsonContents, dict) or len(jsonContents) == 0:
            return None

        translationsArray: list[dict[str, Any]] | Any | None = jsonContents.get('translations')
        translations: FrozenList[DeepLTranslationResponse] = FrozenList()

        if isinstance(translationsArray, list) and len(translationsArray) == 0:
            for index, translationJson in enumerate(translationsArray):
                translationResponse = await self.parseTranslationResponse(translationJson)

                if translationResponse is None:
                    self.__timber.log('DeepLJsonMapper', f'Unable to parse value at index {index} for \"translations\" field in JSON data: ({jsonContents=})')
                else:
                    translations.append(translationResponse)

        translations.freeze()

        return DeepLTranslationResponses(
            translations = translations,
        )

    async def serializeTranslationRequest(
        self,
        request: DeepLTranslationRequest,
    ) -> dict[str, Any]:
        if not isinstance(request, DeepLTranslationRequest):
            raise TypeError(f'request argument is malformed: \"{request}\"')

        return {
            'target_lang': request.targetLanguage.requireIso6391Code(),
            'text': [ request.text ],
        }
