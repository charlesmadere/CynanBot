import traceback

from .translationApi import TranslationApi
from ..exceptions import (TranslationEngineUnavailableException,
                          TranslationException,
                          TranslationLanguageHasNoIso6391Code)
from ..languageEntry import LanguageEntry
from ..translationApiSource import TranslationApiSource
from ..translationResponse import TranslationResponse
from ...deepL.deepLApiServiceInterface import DeepLApiServiceInterface
from ...deepL.deepLAuthKeyProviderInterface import DeepLAuthKeyProviderInterface
from ...deepL.deepLTranslationRequest import DeepLTranslationRequest
from ...deepL.exceptions import DeepLAuthKeyUnavailableException
from ...misc import utils as utils
from ...network.exceptions import GenericNetworkException
from ...timber.timberInterface import TimberInterface


class DeepLTranslationApi(TranslationApi):

    def __init__(
        self,
        deepLApiService: DeepLApiServiceInterface,
        deepLAuthKeyProvider: DeepLAuthKeyProviderInterface,
        timber: TimberInterface
    ):
        if not isinstance(deepLApiService, DeepLApiServiceInterface):
            raise TypeError(f'deepLApiService argument is malformed: \"{deepLApiService}\"')
        elif not isinstance(deepLAuthKeyProvider, DeepLAuthKeyProviderInterface):
            raise TypeError(f'deepLAuthKeyProvider argument is malformed: \"{deepLAuthKeyProvider}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')

        self.__deepLApiService: DeepLApiServiceInterface = deepLApiService
        self.__deepLAuthKeyProvider: DeepLAuthKeyProviderInterface = deepLAuthKeyProvider
        self.__timber: TimberInterface = timber

    def getTranslationApiSource(self) -> TranslationApiSource:
        return TranslationApiSource.DEEP_L

    async def isAvailable(self) -> bool:
        deepLAuthKey = await self.__deepLAuthKeyProvider.getDeepLAuthKey()
        return utils.isValidStr(deepLAuthKey)

    async def translate(self, text: str, targetLanguage: LanguageEntry) -> TranslationResponse:
        if not utils.isValidStr(text):
            raise TypeError(f'text argument is malformed: \"{text}\"')
        elif not isinstance(targetLanguage, LanguageEntry):
            raise TypeError(f'targetLanguage argument is malformed: \"{targetLanguage}\"')

        if not utils.isValidStr(targetLanguage.iso6391Code):
            raise TranslationLanguageHasNoIso6391Code(
                languageEntry = targetLanguage,
                message = f'targetLanguage has no ISO 639-1 code: \"{targetLanguage}\"'
            )

        if not await self.isAvailable():
            raise TranslationEngineUnavailableException(
                message = f'DeepL Translation engine is currently unavailable ({text=}) ({targetLanguage=})',
                translationApiSource = self.getTranslationApiSource()
            )

        self.__timber.log('DeepLTranslationApi', f'Fetching translation ({text=}) ({targetLanguage=})...')

        request = DeepLTranslationRequest(
            targetLanguage = targetLanguage,
            text = text
        )

        try:
            response = await self.__deepLApiService.translate(request)
        except DeepLAuthKeyUnavailableException as e:
            self.__timber.log('DeepLTranslationApi', f'No DeepL authentication key is unavailable ({request=}): {e}', e, traceback.format_exc())

            raise TranslationException(
                message = f'No DeepL authentication key is available',
                translationApiSource = self.getTranslationApiSource()
            )
        except GenericNetworkException as e:
            self.__timber.log('DeepLTranslationApi', f'Encountered network error when translating ({request=}): {e}', e, traceback.format_exc())

            raise TranslationException(
                message = f'Encountered network error when translating ({request=}): {e}',
                translationApiSource = self.getTranslationApiSource()
            )

        translations = response.translations

        if translations is None or len(translations) == 0:
            self.__timber.log('DeepLTranslationApi', f'Received no translations from DeepL when translating ({request=})')

            raise TranslationException(
                message = f'Received no translations from DeepL when translating ({request})',
                translationApiSource = self.getTranslationApiSource()
            )

        return TranslationResponse(
            originalLanguage = translations[0].detectedSourceLanguage,
            translatedLanguage = targetLanguage,
            originalText = text,
            translatedText = translations[0].text,
            translationApiSource = self.getTranslationApiSource()
        )
