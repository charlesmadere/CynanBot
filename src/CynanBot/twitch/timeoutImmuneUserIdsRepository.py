from CynanBot.twitch.timeoutImmuneUserIdsRepositoryInterface import TimeoutImmuneUserIdsRepositoryInterface


class TimeoutImmuneUserIdsRepository(TimeoutImmuneUserIdsRepositoryInterface):

    def __init__(
        self,
        immuneUserIds: list[str] = list()
    ):
        if not isinstance(immuneUserIds, list):
            raise TypeError(f'immuneUserIds argument is malformed: \"{immuneUserIds}\"')

        self.__immuneUserIds: set[str] = set(immuneUserIds)

    async def isImmune(self, userId: str) -> bool:
        return userId in self.__immuneUserIds
