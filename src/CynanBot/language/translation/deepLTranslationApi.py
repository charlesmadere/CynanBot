import traceback
from typing import Any, Dict, List, Optional

import CynanBot.misc.utils as utils
from CynanBot.language.languageEntry import LanguageEntry
from CynanBot.language.languagesRepositoryInterface import \
    LanguagesRepositoryInterface
from CynanBot.language.translation.exceptions import (
    TranslationEngineUnavailableException, TranslationException)
from CynanBot.language.translation.translationApi import TranslationApi
from CynanBot.language.translationApiSource import TranslationApiSource
from CynanBot.language.translationResponse import TranslationResponse
from CynanBot.network.exceptions import GenericNetworkException
from CynanBot.network.networkClientProvider import NetworkClientProvider
from CynanBot.timber.timberInterface import TimberInterface


class DeepLTranslationApi(TranslationApi):

    def __init__(
        self,
        languagesRepository: LanguagesRepositoryInterface,
        networkClientProvider: NetworkClientProvider,
        deepLAuthKey: Optional[str],
        timber: TimberInterface
    ):
        assert isinstance(languagesRepository, LanguagesRepositoryInterface), f"malformed {languagesRepository=}"
        assert isinstance(networkClientProvider, NetworkClientProvider), f"malformed {networkClientProvider=}"
        assert deepLAuthKey is None or isinstance(deepLAuthKey, str), f"malformed {deepLAuthKey=}"
        assert isinstance(timber, TimberInterface), f"malformed {timber=}"

        self.__languagesRepository: LanguagesRepositoryInterface = languagesRepository
        self.__networkClientProvider: NetworkClientProvider = networkClientProvider
        self.__deepLAuthKey: Optional[str] = deepLAuthKey
        self.__timber: TimberInterface = timber

    def getTranslationApiSource(self) -> TranslationApiSource:
        return TranslationApiSource.DEEP_L

    async def isAvailable(self) -> bool:
        return utils.isValidStr(self.__deepLAuthKey)

    async def translate(self, text: str, targetLanguage: LanguageEntry) -> TranslationResponse:
        if not utils.isValidStr(text):
            raise TypeError(f'text argument is malformed: \"{text}\"')
        assert isinstance(targetLanguage, LanguageEntry), f"malformed {targetLanguage=}"
        if not targetLanguage.hasIso6391Code():
            raise ValueError(f'targetLanguage has no ISO 639-1 code: \"{targetLanguage}\"')

        deepLAuthKey = self.__deepLAuthKey

        if not utils.isValidStr(deepLAuthKey):
            raise TranslationEngineUnavailableException(
                message = f'DeepL Translation engine is currently unavailable ({text=}) ({targetLanguage=}) ({deepLAuthKey=})',
                translationApiSource = self.getTranslationApiSource()
            )

        self.__timber.log('DeepLTranslationApi', f'Fetching translation ({text=}) ({targetLanguage=})...')

        # Retrieve translation from DeepL API: https://www.deepl.com/en/docs-api/

        requestUrl = 'https://api-free.deepl.com/v2/translate?auth_key={}&text={}&target_lang={}'.format(
            deepLAuthKey, text, targetLanguage.requireIso6391Code())

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

        translationsJson: Optional[List[Dict[str, Any]]] = jsonResponse.get('translations')
        if not utils.hasItems(translationsJson):
            raise ValueError(f'DeepL\'s JSON response for \"{text}\" has missing or empty \"translations\" field: {jsonResponse}')

        translationJson: Optional[Dict[str, Any]] = translationsJson[0]
        if not utils.hasItems(translationJson):
            raise ValueError(f'DeepL\'s JSON response for \"{text}\" has missing or empty \"translations\" list entry: {jsonResponse}')

        originalLanguage: Optional[LanguageEntry] = None
        detectedSourceLanguage: Optional[str] = translationJson.get('detected_source_language')
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
