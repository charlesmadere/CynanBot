import CynanBot.misc.utils as utils
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
        googleAssertionTarget: str = 'https://oauth2.googleapis.com/token'
    ):
        if not isinstance(googleCloudCredentialsProvider, GoogleCloudProjectCredentialsProviderInterface):
            raise TypeError(f'(googleCloudCredentialsProvider argument is malformed: \"{googleCloudCredentialsProvider}\"')
        elif not isinstance(googleJsonMapper, GoogleJsonMapperInterface):
            raise TypeError(f'googleJsonMapper argument is malformed: \"{googleJsonMapper}\"')
        elif not isinstance(googleScopes, set):
            raise TypeError(f'googleScopes argument is malformed: \"{googleScopes}\"')
        elif len(googleScopes) == 0:
            raise ValueError(f'googleScopes argument is empty: \"{googleScopes}\"')
        elif not utils.isValidUrl(googleAssertionTarget):
            raise TypeError(f'googleAssertionTarget argument is malformed: \"{googleAssertionTarget}\"')

        self.__googleCloudCredentialsProvider: GoogleCloudProjectCredentialsProviderInterface = googleCloudCredentialsProvider
        self.__googleJsonMapper: GoogleJsonMapperInterface = googleJsonMapper
        self.__googleScopes: set[GoogleScope] = googleScopes
        self.__googleAssertionTarget: str = googleAssertionTarget

        self.__scopesString: str | None = None

    async def buildJwt(self) -> str:
        scopesString = await self.__buildScopesString()

        # TODO
        raise RuntimeError('Not implemented')

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
