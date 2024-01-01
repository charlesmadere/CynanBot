import json
import random
import traceback
from json.decoder import JSONDecodeError
from typing import Any, Dict, List, Optional

import aiofiles
import aiofiles.ospath

isGoogleMissing = False

try:
    from google.cloud import translate_v2 as translate
except:
    isGoogleMissing = True

import CynanBot.misc.utils as utils
from CynanBot.language.languageEntry import LanguageEntry
from CynanBot.language.languagesRepository import LanguagesRepository
from CynanBot.language.translationApiSource import TranslationApiSource
from CynanBot.language.translationHelperInterface import \
    TranslationHelperInterface
from CynanBot.language.translationResponse import TranslationResponse
from CynanBot.network.exceptions import GenericNetworkException
from CynanBot.network.networkClientProvider import NetworkClientProvider
from CynanBot.timber.timberInterface import TimberInterface


class TranslationHelper(TranslationHelperInterface):

    def __init__(
        self,
        languagesRepository: LanguagesRepository,
        networkClientProvider: NetworkClientProvider,
        deepLAuthKey: str,
        timber: TimberInterface,
        googleServiceAccountFile: str = 'googleServiceAccount.json'
    ):
        if not isinstance(languagesRepository, LanguagesRepository):
            raise ValueError(f'languagesRepository argument is malformed: \"{languagesRepository}\"')
        elif not isinstance(networkClientProvider, NetworkClientProvider):
            raise ValueError(f'networkClientProvider argument is malformed: \"{networkClientProvider}\"')
        elif not utils.isValidStr(deepLAuthKey):
            raise ValueError(f'deepLAuthKey argument is malformed: \"{deepLAuthKey}\"')
        elif not isinstance(timber, TimberInterface):
            raise ValueError(f'timber argument is malformed: \"{timber}\"')
        elif not utils.isValidStr(googleServiceAccountFile):
            raise ValueError(f'googleServiceAccountFile argument is malformed: \"{googleServiceAccountFile}\"')

        self.__languagesRepository: LanguagesRepository = languagesRepository
        self.__networkClientProvider: NetworkClientProvider = networkClientProvider
        self.__deepLAuthKey: str = deepLAuthKey
        self.__timber: TimberInterface = timber
        self.__googleServiceAccountFile: str = googleServiceAccountFile

        self.__googleTranslateClient: Optional[Any] = None

    async def __deepLTranslate(self, text: str, targetLanguageEntry: LanguageEntry) -> TranslationResponse:
        self.__timber.log('TranslationHelper', f'Fetching translation from DeepL...')

        # Retrieve translation from DeepL API: https://www.deepl.com/en/docs-api/

        requestUrl = 'https://api-free.deepl.com/v2/translate?auth_key={}&text={}&target_lang={}'.format(
            self.__deepLAuthKey, text, targetLanguageEntry.getIso6391Code())

        clientSession = await self.__networkClientProvider.get()

        try:
            response = await clientSession.get(requestUrl)
        except GenericNetworkException as e:
            self.__timber.log('TranslationHelper', f'Encountered network error when translating \"{text}\": {e}', e, traceback.format_exc())
            raise RuntimeError(f'Encountered network error when translating \"{text}\": {e}')

        if response.getStatusCode() != 200:
            self.__timber.log('TranslationHelper', f'Encountered non-200 HTTP status code when fetching translation from DeepL for \"{text}\": {response.getStatusCode()}')
            raise RuntimeError(f'Encountered non-200 HTTP status code when fetching translation from DeepL for \"{text}\": {response.getStatusCode()}')

        jsonResponse: Optional[Dict[str, Any]] = await response.json()
        await response.close()

        if not utils.hasItems(jsonResponse):
            self.__timber.log('TranslationHelper', f'DeepL\'s JSON response is null/empty for \"{text}\": {jsonResponse}')
            raise ValueError(f'DeepL\'s JSON response is null/empty for \"{text}\": {jsonResponse}')

        translationsJson: Optional[List[Dict[str, Any]]] = jsonResponse.get('translations')
        if not utils.hasItems(translationsJson):
            raise ValueError(f'DeepL\'s JSON response for \"{text}\" has missing or empty \"translations\" field: {jsonResponse}')

        translationJson: Optional[Dict[str, Any]] = translationsJson[0]
        if not utils.hasItems(translationJson):
            raise ValueError(f'DeepL\'s JSON response for \"{text}\" has missing or empty \"translations\" list entry: {jsonResponse}')

        originalLanguage: Optional[LanguageEntry] = None
        detectedSourceLanguage: str = translationJson.get('detected_source_language')
        if utils.isValidStr(detectedSourceLanguage):
            originalLanguage = await self.__languagesRepository.getLanguageForCommand(
                command = detectedSourceLanguage,
                hasIso6391Code = True
            )

        return TranslationResponse(
            originalLanguage = originalLanguage,
            translatedLanguage = targetLanguageEntry,
            originalText = text,
            translatedText = utils.getStrFromDict(translationJson, 'text', clean = True, htmlUnescape = True),
            translationApiSource = TranslationApiSource.DEEP_L
        )

    async def __getGoogleTranslateClient(self) -> Optional[Any]:
        if isGoogleMissing:
            return None

        if self.__googleTranslateClient is None:
            self.__timber.log('TranslationHelper', f'Initializing new Google translate.Client instance...')

            if not await self.__hasGoogleApiCredentials():
                raise RuntimeError(f'Unable to initialize a new Google translate.Client instance because the Google API credentials are missing')
            elif not await aiofiles.ospath.exists(self.__googleServiceAccountFile):
                raise FileNotFoundError(f'googleServiceAccount file not found: \"{self.__googleServiceAccountFile}\"')

            self.__googleTranslateClient = translate.Client.from_service_account_json(self.__googleServiceAccountFile)

        return self.__googleTranslateClient

    async def __googleTranslate(self, text: str, targetLanguageEntry: LanguageEntry) -> TranslationResponse:
        self.__timber.log('TranslationHelper', f'Fetching translation from Google Translate...')

        googleTranslateClient = await self.__getGoogleTranslateClient()
        if googleTranslateClient is None:
            raise RuntimeError(f'googleTranslateClient is None!')

        translationResult: Optional[Dict[str, Any]] = googleTranslateClient.translate(
            text,
            target_language = targetLanguageEntry.getIso6391Code()
        )

        if not utils.hasItems(translationResult):
            raise RuntimeError(f'error in the data response when attempting to translate \"{text}\": {translationResult}')

        originalText: str = translationResult.get('input')
        if not utils.isValidStr(originalText):
            raise RuntimeError(f'\"input\" field is missing or malformed from translation result for \"{text}\": {translationResult}')

        translatedText: str = translationResult.get('translatedText')
        if not utils.isValidStr(translatedText):
            raise RuntimeError(f'\"translatedText\" field is missing or malformed from translation result for \"{text}\": {translationResult}')

        originalLanguage: Optional[LanguageEntry] = None
        detectedSourceLanguage: Optional[str] = translationResult.get('detectedSourceLanguage')
        if utils.isValidStr(detectedSourceLanguage):
            originalLanguage = await self.__languagesRepository.getLanguageForCommand(
                command = detectedSourceLanguage,
                hasIso6391Code = True
            )

        return TranslationResponse(
            originalLanguage = originalLanguage,
            translatedLanguage = targetLanguageEntry,
            originalText = originalText,
            translatedText = utils.cleanStr(translatedText, htmlUnescape = True),
            translationApiSource = TranslationApiSource.GOOGLE_TRANSLATE
        )

    async def __hasGoogleApiCredentials(self) -> bool:
        if not await aiofiles.ospath.exists(self.__googleServiceAccountFile):
            return False

        jsonContents: Optional[Dict[str, Any]] = None
        exception: Optional[JSONDecodeError] = None

        async with aiofiles.open(self.__googleServiceAccountFile, mode = 'r', encoding = 'utf-8') as file:
            data = await file.read()

            try:
                jsonContents = json.loads(data)
            except JSONDecodeError as e:
                exception = e

        return utils.hasItems(jsonContents) and exception is None

    async def translate(
        self,
        text: str,
        targetLanguageEntry: Optional[LanguageEntry] = None
    ) -> TranslationResponse:
        if not utils.isValidStr(text):
            raise ValueError(f'text argument is malformed: \"{text}\"')

        text = utils.cleanStr(text)

        if targetLanguageEntry is not None and not targetLanguageEntry.hasIso6391Code():
            raise ValueError(f'the given LanguageEntry is not supported for translation: \"{targetLanguageEntry.getName()}\"')
        elif targetLanguageEntry is None:
            targetLanguageEntry = await self.__languagesRepository.requireLanguageForCommand(
                command = 'en',
                hasIso6391Code = True
            )

        if self.__googleTranslateClient is None and not await self.__hasGoogleApiCredentials():
            # This isn't an optimal situation, but it means that we're currently running in a
            # situation where we have no Google API credentials, but we do have DeepL credentials.
            # So here we'll just always use DeepL for translation, rather than evenly splitting
            # the workload between both services.
            return await self.__deepLTranslate(text, targetLanguageEntry)

        # In order to help keep us from running beyond the free usage tiers for the Google
        # Translate and DeepL translation services, let's randomly choose which translation service
        # to use. At the time of this writing, both services have a 500,000 character monthly limit.
        # So theoretically, this gives us a 1,000,000 character translation capability.

        translationApiSource = random.choice(list(TranslationApiSource))
        while not translationApiSource.isEnabled():
            translationApiSource = random.choice(list(TranslationApiSource))

        if translationApiSource is TranslationApiSource.DEEP_L:
            return await self.__deepLTranslate(text, targetLanguageEntry)
        elif translationApiSource is TranslationApiSource.GOOGLE_TRANSLATE:
            return await self.__googleTranslate(text, targetLanguageEntry)
        else:
            raise ValueError(f'unknown TranslationApiSource: \"{translationApiSource}\"')
