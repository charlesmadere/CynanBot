from .theRunBotUserIdProviderInterface import TheRunBotUserIdProviderInterface


class TheRunBotUserIdProvider(TheRunBotUserIdProviderInterface):

    def __init__(self, theRunBotUserId: str | None = '795719761'):
        if theRunBotUserId is not None and not isinstance(theRunBotUserId, str):
            raise TypeError(f'theRunBotUserId argument is malformed: \"{theRunBotUserId}\"')

        self.__theRunBotUserId: str | None = theRunBotUserId

    async def getTheRunBotUserId(self) -> str | None:
        return self.__theRunBotUserId
