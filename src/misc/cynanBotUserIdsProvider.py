from .cynanBotUserIdsProviderInterface import CynanBotUserIdsProviderInterface


class CynanBotUserIdsProvider(CynanBotUserIdsProviderInterface):

    def __init__(
        self,
        cynanBotUserId: str | None = '477393386',
        cynanBotTtsUserId: str | None = '977636741'
    ):
        if cynanBotUserId is not None and not isinstance(cynanBotUserId, str):
            raise TypeError(f'cynanBotUserId argument is malformed: \"{cynanBotUserId}\"')
        elif cynanBotTtsUserId is not None and not isinstance(cynanBotTtsUserId, str):
            raise TypeError(f'cynanBotTtsUserId argument is malformed: \"{cynanBotTtsUserId}\"')

        self.__cynanBotUserId: str | None = cynanBotUserId
        self.__cynanBotTtsUserId: str | None = cynanBotTtsUserId

    async def getCynanBotUserId(self) -> str | None:
        return self.__cynanBotUserId

    async def getCynanBotTtsUserId(self) -> str | None:
        return self.__cynanBotTtsUserId
