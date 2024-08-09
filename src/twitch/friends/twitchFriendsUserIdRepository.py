from .twitchFriendsUserIdRepositoryInterface import TwitchFriendsUserIdRepositoryInterface


class TwitchFriendsUserIdRepository(TwitchFriendsUserIdRepositoryInterface):

    def __init__(
        self,
        charlesUserId: str | None = '74350217'
    ):
        if charlesUserId is not None and not isinstance(charlesUserId, str):
            raise TypeError(f'charlesUserId argument is malformed: \"{charlesUserId}\"')

        self.__charlesUserId: str | None = charlesUserId

    async def getCharlesUserId(self) -> str | None:
        return self.__charlesUserId
