from CynanBot.google.googleJsonMapperInterface import GoogleJsonMapperInterface
from CynanBot.google.googleJwtBuilderInterface import GoogleJwtBuilderInterface
from CynanBot.google.googleScope import GoogleScope


class GoogleJwtBuilder(GoogleJwtBuilderInterface):

    def __init__(
        self,
        googleJsonMapper: GoogleJsonMapperInterface,
        googleScopes: set[GoogleScope] = {
            GoogleScope.CLOUD_TEXT_TO_SPEECH,
            GoogleScope.CLOUD_TRANSLATION
        }
    ):
        if not isinstance(googleJsonMapper, GoogleJsonMapperInterface):
            raise TypeError(f'googleJsonMapper argument is malformed: \"{googleJsonMapper}\"')
        elif not isinstance(googleScopes, set):
            raise TypeError(f'googleScopes argument is malformed: \"{googleScopes}\"')
        elif len(googleScopes) == 0:
            raise ValueError(f'googleScopes argument is empty: \"{googleScopes}\"')

        self.__googleJsonMapper: GoogleJsonMapperInterface = googleJsonMapper
        self.__googleScopes: set[GoogleScope] = googleScopes

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
