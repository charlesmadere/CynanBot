import traceback
from typing import Any

import CynanBot.misc.utils as utils
from CynanBot.deepL.deepLAuthKeyProviderInterface import \
    DeepLAuthKeyProviderInterface
from CynanBot.language.exceptions import (
    TranslationEngineUnavailableException, TranslationException,
    TranslationLanguageHasNoIso6391Code)
from CynanBot.language.languageEntry import LanguageEntry
from CynanBot.language.languagesRepositoryInterface import \
    LanguagesRepositoryInterface
from CynanBot.language.translation.translationApi import TranslationApi
from CynanBot.language.translationApiSource import TranslationApiSource
from CynanBot.language.translationResponse import TranslationResponse
from CynanBot.network.exceptions import GenericNetworkException
from CynanBot.network.networkClientProvider import NetworkClientProvider
from CynanBot.timber.timberInterface import TimberInterface


class DeepLTranslationApi(TranslationApi):

    def __init__(
        self,
        deepLAuthKeyProvider: DeepLAuthKeyProviderInterface,
        languagesRepository: LanguagesRepositoryInterface,
        networkClientProvider: NetworkClientProvider,
        timber: TimberInterface
    ):
        if not isinstance(deepLAuthKeyProvider, DeepLAuthKeyProviderInterface):
            raise TypeError(f'deepLAuthKeyProvider argument is malformed: \"{deepLAuthKeyProvider}\"')
        if not isinstance(languagesRepository, LanguagesRepositoryInterface):
            raise TypeError(f'languagesRepository argument is malformed: \"{languagesRepository}\"')
        elif not isinstance(networkClientProvider, NetworkClientProvider):
            raise TypeError(f'networkClientProvider argument is malformed: \"{networkClientProvider}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')

        self.__deepLAuthKeyProvider: DeepLAuthKeyProviderInterface = deepLAuthKeyProvider
        self.__languagesRepository: LanguagesRepositoryInterface = languagesRepository
        self.__networkClientProvider: NetworkClientProvider = networkClientProvider
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

        iso6391Code = targetLanguage.getIso6391Code()

        if not utils.isValidStr(iso6391Code):
            raise TranslationLanguageHasNoIso6391Code(
                languageEntry = targetLanguage,
                message = f'targetLanguage has no ISO 639-1 code: \"{targetLanguage}\"'
            )

        deepLAuthKey = await self.__deepLAuthKeyProvider.getDeepLAuthKey()

        if not utils.isValidStr(deepLAuthKey):
            raise TranslationEngineUnavailableException(
                message = f'DeepL Translation engine is currently unavailable ({text=}) ({targetLanguage=}) ({deepLAuthKey=})',
                translationApiSource = self.getTranslationApiSource()
            )

        self.__timber.log('DeepLTranslationApi', f'Fetching translation ({text=}) ({targetLanguage=})...')

        # Retrieve translation from DeepL API: https://www.deepl.com/en/docs-api/

        requestUrl = 'https://api-free.deepl.com/v2/translate?auth_key={}&text={}&target_lang={}'.format(
            deepLAuthKey, text, iso6391Code)

        clientSession = await self.__networkClientProvider.get()

        try:
            response = await clientSession.get(requestUrl)
        except GenericNetworkException as e:
            self.__timber.log('DeepLTranslationApi', f'Encountered network error when translating \"{text}\": {e}', e, traceback.format_exc())

            raise TranslationException(
                message = f'Encountered network error when translating \"{text}\": {e}',
                translationApiSource = self.getTranslationApiSource()
            )

        if response.getStatusCode() != 200:
            self.__timber.log('DeepLTranslationApi', f'Encountered non-200 HTTP status code when fetching translation from DeepL for \"{text}\": {response.getStatusCode()}')
            raise RuntimeError(f'Encountered non-200 HTTP status code when fetching translation from DeepL for \"{text}\": {response.getStatusCode()}')

        jsonResponse = await response.json()
        await response.close()

        if not utils.hasItems(jsonResponse):
            self.__timber.log('DeepLTranslationApi', f'DeepL\'s JSON response is null/empty for \"{text}\": {jsonResponse}')
            raise ValueError(f'DeepL\'s JSON response is null/empty for \"{text}\": {jsonResponse}')

        translationsJson: list[dict[str, Any]] | None = jsonResponse.get('translations')
        if not utils.hasItems(translationsJson):
            raise ValueError(f'DeepL\'s JSON response for \"{text}\" has missing or empty \"translations\" field: {jsonResponse}')

        translationJson: dict[str, Any] | None = translationsJson[0]
        if not utils.hasItems(translationJson):
            raise ValueError(f'DeepL\'s JSON response for \"{text}\" has missing or empty \"translations\" list entry: {jsonResponse}')

        originalLanguage: LanguageEntry | None = None
        detectedSourceLanguage: str | None = translationJson.get('detected_source_language')
        if utils.isValidStr(detectedSourceLanguage):
            originalLanguage = await self.__languagesRepository.getLanguageForCommand(
                command = detectedSourceLanguage,
                hasIso6391Code = True
            )

        translatedText = utils.getStrFromDict(
            translationJson,
            key = 'text',
            clean = True,
            htmlUnescape = True
        )

        return TranslationResponse(
            originalLanguage = originalLanguage,
            translatedLanguage = targetLanguage,
            originalText = text,
            translatedText = translatedText,
            translationApiSource = self.getTranslationApiSource()
        )
