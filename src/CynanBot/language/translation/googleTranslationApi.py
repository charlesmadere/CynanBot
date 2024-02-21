import json
import traceback
from json.decoder import JSONDecodeError
from typing import Any, Dict, Optional

import aiofiles
import aiofiles.ospath

isGoogleMissing = False

try:
    from google.cloud import translate_v2 as translate
except:
    isGoogleMissing = True

import CynanBot.misc.utils as utils
from CynanBot.language.languageEntry import LanguageEntry
from CynanBot.language.languagesRepositoryInterface import \
    LanguagesRepositoryInterface
from CynanBot.language.translation.exceptions import (
    TranslationEngineUnavailableException, TranslationException)
from CynanBot.language.translation.translationApi import TranslationApi
from CynanBot.language.translationApiSource import TranslationApiSource
from CynanBot.language.translationResponse import TranslationResponse
from CynanBot.timber.timberInterface import TimberInterface


class GoogleTranslationApi(TranslationApi):

    def __init__(
        self,
        languagesRepository: LanguagesRepositoryInterface,
        timber: TimberInterface,
        googleServiceAccountFile: str = 'googleServiceAccount.json'
    ):
        self.__languagesRepository: LanguagesRepositoryInterface = languagesRepository
        self.__timber: TimberInterface = timber
        self.__googleServiceAccountFile: str = googleServiceAccountFile

        self.__googleTranslateClient: Optional[Any] = None

    async def __getGoogleTranslateClient(self) -> Optional[Any]:
        if isGoogleMissing:
            return None

        if self.__googleTranslateClient is None:
            self.__timber.log('GoogleTranslationApi', f'Initializing new Google translate.Client instance...')

            if not await self.__hasGoogleApiCredentials():
                raise RuntimeError(f'Unable to initialize a new Google translate.Client instance because the Google API credentials are missing')
            if not await aiofiles.ospath.exists(self.__googleServiceAccountFile):
                raise FileNotFoundError(f'googleServiceAccount file not found: \"{self.__googleServiceAccountFile}\"')

            self.__googleTranslateClient = translate.Client.from_service_account_json(self.__googleServiceAccountFile)

        return self.__googleTranslateClient

    def getTranslationApiSource(self) -> TranslationApiSource:
        return TranslationApiSource.GOOGLE_TRANSLATE

    async def __hasGoogleApiCredentials(self) -> bool:
        if self.__googleTranslateClient is not None:
            return True
        elif isGoogleMissing:
            return False
        elif not await aiofiles.ospath.exists(self.__googleServiceAccountFile):
            return False

        jsonContents: Optional[Dict[str, Any]] = None
        exception: Optional[JSONDecodeError] = None

        async with aiofiles.open(self.__googleServiceAccountFile, mode = 'r', encoding = 'utf-8') as file:
            data = await file.read()

            try:
                jsonContents = json.loads(data)
            except JSONDecodeError as e:
                exception = e

        return isinstance(jsonContents, Dict) and len(jsonContents) >= 1 and exception is None

    async def isAvailable(self) -> bool:
        return await self.__hasGoogleApiCredentials()

    async def translate(self, text: str, targetLanguage: LanguageEntry) -> TranslationResponse:
        if not utils.isValidStr(text):
            raise TypeError(f'text argument is malformed: \"{text}\"')
        assert isinstance(targetLanguage, LanguageEntry), f"malformed {targetLanguage=}"
        if not targetLanguage.hasIso6391Code():
            raise ValueError(f'targetLanguage has no ISO 639-1 code: \"{targetLanguage}\"')

        googleTranslateClient = await self.__getGoogleTranslateClient()

        if googleTranslateClient is None:
            raise TranslationEngineUnavailableException(
                message = f'Google Translation engine is currently unavailable ({text=}) ({targetLanguage=})',
                translationApiSource = self.getTranslationApiSource()
            )

        self.__timber.log('GoogleTranslationApi', f'Fetching translation from Google Translate ({text=}) ({targetLanguage=})...')
        translationResult: Optional[Dict[str, Any]] = None
        exception: Optional[Exception] = None

        try:
            translationResult = googleTranslateClient.translate(
                text,
                target_language = targetLanguage.requireIso6391Code()
            )
        except Exception as e:
            exception = e

        if translationResult is None or len(translationResult) == 0 or exception is not None:
            self.__timber.log('GoogleTranslationApi', f'Encountered an error when attempting to fetch translation from Google Translate ({text=}) ({targetLanguage=})', exception, traceback.format_exc())

            raise TranslationException(
                message = f'Encountered an error when attempting to fetch translation from Google Translate ({text=}) ({targetLanguage=}) ({translationResult=}) ({exception=})',
                translationApiSource = self.getTranslationApiSource()
            )

        originalText: Optional[str] = translationResult.get('input')
        if not utils.isValidStr(originalText):
            raise RuntimeError(f'\"input\" field is missing or malformed from translation result for \"{text}\": {translationResult}')

        translatedText: Optional[str] = translationResult.get('translatedText')
        if not utils.isValidStr(translatedText):
            raise RuntimeError(f'\"translatedText\" field is missing or malformed from translation result for \"{text}\": {translationResult}')

        originalLanguage: Optional[LanguageEntry] = None
        detectedSourceLanguage: Optional[str] = translationResult.get('detectedSourceLanguage')
        if utils.isValidStr(detectedSourceLanguage):
            originalLanguage = await self.__languagesRepository.getLanguageForCommand(
                command = detectedSourceLanguage,
                hasIso6391Code = True
            )

        translatedText = utils.cleanStr(
            s = translatedText,
            htmlUnescape = True
        )

        return TranslationResponse(
            originalLanguage = originalLanguage,
            translatedLanguage = targetLanguage,
            originalText = originalText,
            translatedText = translatedText,
            translationApiSource = self.getTranslationApiSource()
        )
