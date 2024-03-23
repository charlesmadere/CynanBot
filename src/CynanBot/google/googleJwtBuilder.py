import calendar
from datetime import datetime, timedelta, timezone, tzinfo

import jwt

import CynanBot.misc.utils as utils
from CynanBot.google.exceptions import (
    GoogleCloudProjectKeyIdUnavailableException,
    GoogleCloudServiceAccountEmailUnavailableException)
from CynanBot.google.googleCloudProjectCredentialsProviderInterface import \
    GoogleCloudProjectCredentialsProviderInterface
from CynanBot.google.googleJsonMapperInterface import GoogleJsonMapperInterface
from CynanBot.google.googleJwtBuilderInterface import GoogleJwtBuilderInterface
from CynanBot.google.googleScope import GoogleScope


class GoogleJwtBuilder(GoogleJwtBuilderInterface):

    def __init__(
        self,
        googleCloudCredentialsProvider: GoogleCloudProjectCredentialsProviderInterface,
        googleJsonMapper: GoogleJsonMapperInterface,
        googleScopes: set[GoogleScope] = {
            GoogleScope.CLOUD_TEXT_TO_SPEECH,
            GoogleScope.CLOUD_TRANSLATION
        },
        googleAlgorithmValue: str = 'RS256',
        googleAssertionTarget: str = 'https://oauth2.googleapis.com/token',
        googleTokenTypeValue: str = 'JWT',
        timeZone: tzinfo = timezone.utc
    ):
        if not isinstance(googleCloudCredentialsProvider, GoogleCloudProjectCredentialsProviderInterface):
            raise TypeError(f'(googleCloudCredentialsProvider argument is malformed: \"{googleCloudCredentialsProvider}\"')
        elif not isinstance(googleJsonMapper, GoogleJsonMapperInterface):
            raise TypeError(f'googleJsonMapper argument is malformed: \"{googleJsonMapper}\"')
        elif not isinstance(googleScopes, set):
            raise TypeError(f'googleScopes argument is malformed: \"{googleScopes}\"')
        elif len(googleScopes) == 0:
            raise ValueError(f'googleScopes argument is empty: \"{googleScopes}\"')
        elif not utils.isValidStr(googleAlgorithmValue):
            raise TypeError(f'googleAlgorithmValue argument is malformed: \"{googleAlgorithmValue}\"')
        elif not utils.isValidUrl(googleAssertionTarget):
            raise TypeError(f'googleAssertionTarget argument is malformed: \"{googleAssertionTarget}\"')
        elif not utils.isValidStr(googleTokenTypeValue):
            raise TypeError(f'googleTokenTypeValue argument is malformed: \"{googleTokenTypeValue}\"')
        elif not isinstance(timeZone, tzinfo):
            raise TypeError(f'timeZone argument is malformed: \"{timeZone}\"')

        self.__googleCloudCredentialsProvider: GoogleCloudProjectCredentialsProviderInterface = googleCloudCredentialsProvider
        self.__googleJsonMapper: GoogleJsonMapperInterface = googleJsonMapper
        self.__googleScopes: set[GoogleScope] = googleScopes
        self.__googleAlgorithmValue: str = googleAlgorithmValue
        self.__googleAssertionTarget: str = googleAssertionTarget
        self.__googleTokenTypeValue: str = googleTokenTypeValue
        self.__timeZone: tzinfo = timeZone

        self.__scopesString: str | None = None

    async def __buildExpirationTime(self) -> int:
        now = datetime.now(self.__timeZone)
        expirationTime = now + timedelta(minutes = 59, seconds = 45)
        return calendar.timegm(expirationTime.timetuple())

    async def __buildIssuedTime(self) -> int:
        now = datetime.now(self.__timeZone)
        return calendar.timegm(now.timetuple())

    async def buildJwt(self) -> str:
        serviceAccountEmail = await self.__googleCloudCredentialsProvider.getGoogleCloudServiceAccountEmail()
        if not utils.isValidStr(serviceAccountEmail):
            raise GoogleCloudServiceAccountEmailUnavailableException(f'No Google Cloud Service Account Email is available: \"{serviceAccountEmail}\"')

        payload: dict[str, object] = {
            'aud': self.__googleAssertionTarget,
            'exp': await self.__buildExpirationTime(),
            'iat': await self.__buildIssuedTime(),
            'iss': serviceAccountEmail,
            'scope': await self.__buildScopesString()
        }

        keyId = await self.__googleCloudCredentialsProvider.getGoogleCloudProjectKeyId()
        if not utils.isValidStr(keyId):
            raise GoogleCloudProjectKeyIdUnavailableException(f'No Google Cloud Project Key ID is available: \"{keyId}\"')

        headers: dict[str, object] = {
            'kid': keyId,
            'typ': self.__googleTokenTypeValue
        }

        return jwt.encode(
            algorithm = self.__googleAlgorithmValue,
            headers = headers,
            payload = payload
        )

    async def __buildScopesString(self) -> str:
        scopesString = self.__scopesString
        if scopesString is not None:
            return scopesString

        scopesStrings: list[str] = list()

        for googleScope in self.__googleScopes:
            scopesStrings.append(await self.__googleJsonMapper.serializeScope(googleScope))

        scopesString = ' '.join(scopesStrings)
        self.__scopesString = scopesString
        return scopesString
