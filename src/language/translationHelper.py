import random
import traceback
from typing import Final

from .exceptions import (NoTranslationEnginesAvailableException,
                         TranslationLanguageHasNoIso6391Code)
from .languageEntry import LanguageEntry
from .languagesRepositoryInterface import LanguagesRepositoryInterface
from .translation.deepLTranslationApi import DeepLTranslationApi
from .translation.googleTranslationApi import GoogleTranslationApi
from .translation.translationApi import TranslationApi
from .translationHelperInterface import TranslationHelperInterface
from .translationResponse import TranslationResponse
from ..misc import utils as utils
from ..timber.timberInterface import TimberInterface


class TranslationHelper(TranslationHelperInterface):

    def __init__(
        self,
        deepLTranslationApi: DeepLTranslationApi,
        googleTranslationApi: GoogleTranslationApi,
        languagesRepository: LanguagesRepositoryInterface,
        timber: TimberInterface
    ):
        if not isinstance(deepLTranslationApi, DeepLTranslationApi):
            raise TypeError(f'deepLTranslationApi argument is malformed: \"{deepLTranslationApi}\"')
        elif not isinstance(googleTranslationApi, GoogleTranslationApi):
            raise TypeError(f'googleTranslationApi argument is malformed: \"{googleTranslationApi}\"')
        elif not isinstance(languagesRepository, LanguagesRepositoryInterface):
            raise TypeError(f'languagesRepository argument is malformed: \"{languagesRepository}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')

        self.__deepLTranslationApi: Final[TranslationApi] = deepLTranslationApi
        self.__googleTranslationApi: Final[TranslationApi] = googleTranslationApi
        self.__languagesRepository: Final[LanguagesRepositoryInterface] = languagesRepository
        self.__timber: Final[TimberInterface] = timber

    async def __getAvailableTranslationApis(self) -> list[TranslationApi]:
        translationApis: list[TranslationApi] = [
            self.__deepLTranslationApi,
            self.__googleTranslationApi,
        ]

        translationApisToRemove: list[TranslationApi] = list()

        for translationApi in translationApis:
            if not await translationApi.isAvailable():
                translationApisToRemove.append(translationApi)

        if len(translationApisToRemove) >= 1:
            for translationApiToRemove in translationApisToRemove:
                translationApis.remove(translationApiToRemove)

        return translationApis

    async def translate(
        self,
        text: str,
        targetLanguage: LanguageEntry | None = None,
    ) -> TranslationResponse:
        if not utils.isValidStr(text):
            raise TypeError(f'text argument is malformed: \"{text}\"')
        elif targetLanguage is not None and not isinstance(targetLanguage, LanguageEntry):
            raise TypeError(f'targetLanguageEntry argument is malformed: \"{targetLanguage}\"')

        if targetLanguage is not None and not utils.isValidStr(targetLanguage.iso6391Code):
            raise TranslationLanguageHasNoIso6391Code(
                languageEntry = targetLanguage,
                message = f'targetLanguage has no ISO 639-1 code ({targetLanguage=})',
            )

        text = utils.cleanStr(text)

        if targetLanguage is None:
            targetLanguage = LanguageEntry.ENGLISH

        translationApis = await self.__getAvailableTranslationApis()

        if len(translationApis) == 0:
            raise NoTranslationEnginesAvailableException(f'No translation engines are available! ({text=}) ({targetLanguage=}) ({translationApis=})')

        attempt = 0
        translationResponse: TranslationResponse | None = None

        while translationResponse is None and len(translationApis) >= 1:
            # In order to help keep us from running beyond the free usage tiers for the Google
            # Translate and DeepL translation services, let's randomly choose which translation
            # service to use. At the time of this writing, both services have a 500,000 character
            # monthly limit. So theoretically, this gives us a 1,000,000 character translation
            # capability.

            attempt = attempt + 1
            translationApi = random.choice(translationApis)

            try:
                translationResponse = await translationApi.translate(
                    text = text,
                    targetLanguage = targetLanguage,
                )
            except Exception as e:
                translationApis.remove(translationApi)
                translationApiSource = translationApi.translationApiSource
                self.__timber.log('TranslationHelper', f'Exception occurred when translating ({text=}) ({targetLanguage=}) ({attempt=}) ({translationApiSource=})', e, traceback.format_exc())

        if translationResponse is None or len(translationApis) == 0:
            raise NoTranslationEnginesAvailableException(
                message = f'Failed to translate after {attempt} attempt(s) ({text=}) ({targetLanguage=})',
            )

        return translationResponse
