import calendar
from datetime import datetime, timedelta
from typing import Any

import jwt

from .googleJwtBuilderInterface import GoogleJwtBuilderInterface
from ..exceptions import (
    GoogleCloudServiceAccountEmailUnavailableException,
    GoogleCloudProjectKeyIdUnavailableException,
    GoogleCloudProjectPrivateKeyUnavailableException)
from ..googleCloudProjectCredentialsProviderInterface import GoogleCloudProjectCredentialsProviderInterface
from ..jsonMapper.googleJsonMapperInterface import GoogleJsonMapperInterface
from ..models.googleScope import GoogleScope
from ...location.timeZoneRepositoryInterface import TimeZoneRepositoryInterface
from ...misc import utils as utils


class GoogleJwtBuilder(GoogleJwtBuilderInterface):

    def __init__(
        self,
        googleCloudCredentialsProvider: GoogleCloudProjectCredentialsProviderInterface,
        googleJsonMapper: GoogleJsonMapperInterface,
        timeZoneRepository: TimeZoneRepositoryInterface,
        googleScopes: frozenset[GoogleScope] = frozenset({
            GoogleScope.CLOUD_TEXT_TO_SPEECH,
            GoogleScope.CLOUD_TRANSLATION,
        }),
    ):
        if not isinstance(googleCloudCredentialsProvider, GoogleCloudProjectCredentialsProviderInterface):
            raise TypeError(f'(googleCloudCredentialsProvider argument is malformed: \"{googleCloudCredentialsProvider}\"')
        elif not isinstance(googleJsonMapper, GoogleJsonMapperInterface):
            raise TypeError(f'googleJsonMapper argument is malformed: \"{googleJsonMapper}\"')
        elif not isinstance(timeZoneRepository, TimeZoneRepositoryInterface):
            raise TypeError(f'timeZoneRepository argument is malformed: \"{timeZoneRepository}\"')
        elif not isinstance(googleScopes, frozenset):
            raise TypeError(f'googleScopes argument is malformed: \"{googleScopes}\"')
        elif len(googleScopes) == 0:
            raise ValueError(f'googleScopes argument is empty: \"{googleScopes}\"')

        self.__googleCloudCredentialsProvider: GoogleCloudProjectCredentialsProviderInterface = googleCloudCredentialsProvider
        self.__googleJsonMapper: GoogleJsonMapperInterface = googleJsonMapper
        self.__timeZoneRepository: TimeZoneRepositoryInterface = timeZoneRepository
        self.__googleScopes: frozenset[GoogleScope] = googleScopes

        self.__scopesString: str | None = None

    async def __buildHeadersDictionary(self) -> dict[str, Any]:
        keyId = await self.__googleCloudCredentialsProvider.getGoogleCloudProjectKeyId()
        if not utils.isValidStr(keyId):
            raise GoogleCloudProjectKeyIdUnavailableException(f'No Google Cloud Project Key ID is available: \"{keyId}\"')

        return {
            'kid': keyId,
            'typ': 'JWT',
        }

    async def buildJwt(self) -> str:
        payload = await self.__buildPayloadDictionary()
        headers = await self.__buildHeadersDictionary()

        privateKey = await self.__googleCloudCredentialsProvider.getGoogleCloudProjectPrivateKey()
        if not utils.isValidStr(privateKey):
            raise GoogleCloudProjectPrivateKeyUnavailableException(f'No Google Cloud Project Private Key is available: \"{privateKey}\"')

        return jwt.encode(
            algorithm = 'RS256',
            key = privateKey,
            headers = headers,
            payload = payload,
        )

    async def __buildPayloadDictionary(self) -> dict[str, Any]:
        now = datetime.now(self.__timeZoneRepository.getDefault())
        expirationTime = calendar.timegm((now + timedelta(minutes = 59, seconds = 45)).timetuple())
        issuedTime = calendar.timegm(now.timetuple())

        serviceAccountEmail = await self.__googleCloudCredentialsProvider.getGoogleCloudServiceAccountEmail()
        if not utils.isValidStr(serviceAccountEmail):
            raise GoogleCloudServiceAccountEmailUnavailableException(f'No Google Cloud Service Account Email is available: \"{serviceAccountEmail}\"')

        return {
            'aud': 'https://oauth2.googleapis.com/token',
            'exp': expirationTime,
            'iat': issuedTime,
            'iss': serviceAccountEmail,
            'scope': await self.__buildScopesString(),
        }

    async def __buildScopesString(self) -> str:
        scopesString = self.__scopesString

        if scopesString is None:
            scopes = list(self.__googleScopes)
            scopesString = await self.__googleJsonMapper.serializeScopes(scopes)
            self.__scopesString = scopesString

        return scopesString
