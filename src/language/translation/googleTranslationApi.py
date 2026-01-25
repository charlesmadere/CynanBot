import traceback

from frozenlist import FrozenList

from .translationApi import TranslationApi
from ..exceptions import TranslationException, TranslationLanguageHasNoIso6391Code
from ..languageEntry import LanguageEntry
from ..languagesRepositoryInterface import LanguagesRepositoryInterface
from ..translationApiSource import TranslationApiSource
from ..translationResponse import TranslationResponse
from ...google.apiService.googleApiServiceInterface import GoogleApiServiceInterface
from ...google.googleCloudProjectCredentialsProviderInterface import GoogleCloudProjectCredentialsProviderInterface
from ...google.models.googleTranslationRequest import GoogleTranslationRequest
from ...misc import utils as utils
from ...timber.timberInterface import TimberInterface


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

    async def isAvailable(self) -> bool:
        projectId = await self.__googleCloudProjectCredentialsProvider.getGoogleCloudProjectId()
        keyId = await self.__googleCloudProjectCredentialsProvider.getGoogleCloudProjectKeyId()
        privateKey = await self.__googleCloudProjectCredentialsProvider.getGoogleCloudProjectPrivateKey()
        serviceAccountEmail = await self.__googleCloudProjectCredentialsProvider.getGoogleCloudServiceAccountEmail()

        return utils.isValidStr(projectId) \
            and utils.isValidStr(keyId) \
            and utils.isValidStr(privateKey) \
            and utils.isValidStr(serviceAccountEmail)

    async def translate(
        self,
        text: str,
        targetLanguage: LanguageEntry,
    ) -> TranslationResponse:
        if not utils.isValidStr(text):
            raise TypeError(f'text argument is malformed: \"{text}\"')
        elif not isinstance(targetLanguage, LanguageEntry):
            raise TypeError(f'targetLanguage argument is malformed: \"{targetLanguage}\"')

        if not utils.isValidStr(targetLanguage.iso6391Code):
            raise TranslationLanguageHasNoIso6391Code(
                languageEntry = targetLanguage,
                message = f'targetLanguage has no ISO 639-1 code ({targetLanguage=})',
            )

        contents: FrozenList[str] = FrozenList()
        contents.append(text)
        contents.freeze()

        request = GoogleTranslationRequest(
            glossaryConfig = None,
            contents = contents,
            mimeType = self.__mimeType,
            model = None,
            sourceLanguageCode = None,
            targetLanguageCode = targetLanguage.iso6391Code,
            transliterationConfig = None,
        )

        self.__timber.log('GoogleTranslationApi', f'Fetching translation from Google Translate ({request=})...')

        try:
            response = await self.__googleApiService.translate(request)
        except Exception as e:
            self.__timber.log('GoogleTranslationApi', f'Encountered an error when attempting to fetch translation from Google Translate ({request=})', e, traceback.format_exc())

            raise TranslationException(
                message = f'Encountered an error when attempting to fetch translation from Google Translate ({request=})',
                translationApiSource = self.translationApiSource,
            )

        translations = response.translations

        if translations is None or len(translations) == 0:
            self.__timber.log('GoogleTranslationApi', f'Received no translations from Google Translate ({request=}) ({response=})')

            raise TranslationException(
                message = f'Received no translations from Google Translate ({request=}) ({response=})',
                translationApiSource = self.translationApiSource,
            )

        translation = translations[0]
        translatedText = translation.translatedText

        if not utils.isValidStr(translatedText):
            self.__timber.log('GoogleTranslationApi', f'\"translatedText\" field is null/empty ({translatedText=}) ({text=}) ({targetLanguage=}) ({response=})')

            raise TranslationException(
                message = f'GoogleTranslationApi received a null/empty \"translatedText\" field ({translatedText=}) ({text=}) ({targetLanguage=}) ({response=})',
                translationApiSource = self.translationApiSource,
            )

        detectedLanguageCode = translation.detectedLanguageCode
        originalLanguage: LanguageEntry | None = None

        if utils.isValidStr(detectedLanguageCode):
            originalLanguage = await self.__languagesRepository.getLanguageForCommand(
                command = detectedLanguageCode,
                hasIso6391Code = True,
            )

        if originalLanguage is None:
            self.__timber.log('GoogleTranslationApi', f'Unable to find corresponding language entry for the given detected language code ({request=}) ({response=}) ({originalLanguage=})')

        return TranslationResponse(
            originalLanguage = originalLanguage,
            translatedLanguage = targetLanguage,
            originalText = text,
            translatedText = translatedText,
            translationApiSource = self.translationApiSource,
        )

    @property
    def translationApiSource(self) -> TranslationApiSource:
        return TranslationApiSource.GOOGLE_TRANSLATE
