import traceback

import CynanBot.misc.utils as utils
from CynanBot.google.googleApiServiceInterface import GoogleApiServiceInterface
from CynanBot.google.googleCloudProjectCredentialsProviderInterface import \
    GoogleCloudProjectCredentialsProviderInterface
from CynanBot.google.googleTranslateTextResponse import \
    GoogleTranslateTextResponse
from CynanBot.google.googleTranslationRequest import GoogleTranslationRequest
from CynanBot.language.exceptions import (TranslationException,
                                          TranslationLanguageHasNoIso6391Code)
from CynanBot.language.languageEntry import LanguageEntry
from CynanBot.language.languagesRepositoryInterface import \
    LanguagesRepositoryInterface
from CynanBot.language.translation.translationApi import TranslationApi
from CynanBot.language.translationApiSource import TranslationApiSource
from CynanBot.language.translationResponse import TranslationResponse
from CynanBot.timber.timberInterface import TimberInterface


class GoogleTranslationApi(TranslationApi):

    def __init__(
        self,
        googleApiService: GoogleApiServiceInterface,
        googleCloudProjectCredentialsProvider: GoogleCloudProjectCredentialsProviderInterface,
        languagesRepository: LanguagesRepositoryInterface,
        timber: TimberInterface,
        mimeType: str = 'text/plain'
    ):
        if not isinstance(googleApiService, GoogleApiServiceInterface):
            raise TypeError(f'googleApiService argument is malformed: \"{googleApiService}\"')
        elif not isinstance(googleCloudProjectCredentialsProvider, GoogleCloudProjectCredentialsProviderInterface):
            raise TypeError(f'googleCloudProjectCredentialsProvider argument is malformed: \"{googleCloudProjectCredentialsProvider}\"')
        elif not isinstance(languagesRepository, LanguagesRepositoryInterface):
            raise TypeError(f'languagesRepository argument is malformed: \"{languagesRepository}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not utils.isValidStr(mimeType):
            raise TypeError(f'mimeType argument is malformed: \"{mimeType}\"')

        self.__googleApiService: GoogleApiServiceInterface = googleApiService
        self.__googleCloudProjectCredentialsProvider: GoogleCloudProjectCredentialsProviderInterface = googleCloudProjectCredentialsProvider
        self.__languagesRepository: LanguagesRepositoryInterface = languagesRepository
        self.__timber: TimberInterface = timber
        self.__mimeType: str = mimeType

    def getTranslationApiSource(self) -> TranslationApiSource:
        return TranslationApiSource.GOOGLE_TRANSLATE

    async def isAvailable(self) -> bool:
        projectId = await self.__googleCloudProjectCredentialsProvider.getGoogleCloudProjectId()
        keyId = await self.__googleCloudProjectCredentialsProvider.getGoogleCloudProjectKeyId()
        privateKey = await self.__googleCloudProjectCredentialsProvider.getGoogleCloudProjectPrivateKey()
        serviceAccountEmail = await self.__googleCloudProjectCredentialsProvider.getGoogleCloudServiceAccountEmail()

        return utils.isValidStr(projectId) \
            and utils.isValidStr(keyId) \
            and utils.isValidStr(privateKey) \
            and utils.isValidStr(serviceAccountEmail)

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

        request = GoogleTranslationRequest(
            glossaryConfig = None,
            contents = [ text ],
            mimeType = self.__mimeType,
            model = None,
            sourceLanguageCode = None,
            targetLanguageCode = iso6391Code,
            transliterationConfig = None
        )

        self.__timber.log('GoogleTranslationApi', f'Fetching translation from Google Translate ({text=}) ({targetLanguage=}) ({request=})...')
        response: GoogleTranslateTextResponse | None = None
        exception: Exception | None = None

        try:
            response = await self.__googleApiService.translate(request)
        except Exception as e:
            exception = e

        if response is None or exception is not None:
            self.__timber.log('GoogleTranslationApi', f'Encountered an error when attempting to fetch translation from Google Translate ({text=}) ({targetLanguage=}) ({response=}): {exception}', exception, traceback.format_exc())

            raise TranslationException(
                message = f'Encountered an error when attempting to fetch translation from Google Translate ({text=}) ({targetLanguage=}) ({response=}) ({exception=})',
                translationApiSource = self.getTranslationApiSource()
            )

        translations = response.getTranslations()
        if translations is None or len(translations) == 0:
            self.__timber.log('GoogleTranslationApi', f'\"translations\" field is null/empty ({translations=}) ({text=}) ({targetLanguage=}) ({response=})')

            raise TranslationException(
                message = f'GoogleTranslationApi received a null/empty \"translations\" field ({translations=}) ({text=}) ({targetLanguage=}) ({response=})',
                translationApiSource = self.getTranslationApiSource()
            )

        translation = translations[0]
        translatedText = translation.getTranslatedText()

        if not utils.isValidStr(translatedText):
            self.__timber.log('GoogleTranslationApi', f'\"translatedText\" field is null/empty ({translatedText=}) ({text=}) ({targetLanguage=}) ({response=})')

            raise TranslationException(
                message = f'GoogleTranslationApi received a null/empty \"translatedText\" field ({translatedText=}) ({text=}) ({targetLanguage=}) ({response=})',
                translationApiSource = self.getTranslationApiSource()
            )

        detectedLanguageCode = translation.getDetectedLanguageCode()
        originalLanguage: LanguageEntry | None = None

        if utils.isValidStr(detectedLanguageCode):
            originalLanguage = await self.__languagesRepository.getLanguageForCommand(
                command = detectedLanguageCode,
                hasIso6391Code = True
            )

        if originalLanguage is None:
            self.__timber.log('GoogleTranslationApi', f'Unable to find corresponding language entry for the given detected language code \"{translation.getDetectedLanguageCode}\" ({text=}) ({targetLanguage=}) ({response=})')

        return TranslationResponse(
            originalLanguage = originalLanguage,
            translatedLanguage = targetLanguage,
            originalText = text,
            translatedText = translatedText,
            translationApiSource = self.getTranslationApiSource()
        )
