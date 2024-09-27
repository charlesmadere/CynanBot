from .twitchFriendsUserIdRepositoryInterface import TwitchFriendsUserIdRepositoryInterface


class TwitchFriendsUserIdRepository(TwitchFriendsUserIdRepositoryInterface):

    def __init__(
        self,
        charlesUserId: str | None = '74350217',
        eddieUserId: str | None = '22587336',
        stashiocatUserId: str | None = '20889981'
    ):
        if charlesUserId is not None and not isinstance(charlesUserId, str):
            raise TypeError(f'charlesUserId argument is malformed: \"{charlesUserId}\"')
        elif eddieUserId is not None and not isinstance(eddieUserId, str):
            raise TypeError(f'eddie argument is malformed: \"{eddieUserId}\"')
        elif stashiocatUserId is not None and not isinstance(stashiocatUserId, str):
            raise TypeError(f'stashiocatUserId argument is malformed: \"{stashiocatUserId}\"')

        self.__charlesUserId: str | None = charlesUserId
        self.__eddieUserId: str | None = eddieUserId
        self.__stashiocatUserId: str | None = stashiocatUserId

    async def getCharlesUserId(self) -> str | None:
        return self.__charlesUserId

    async def getEddieUserId(self) -> str | None:
        return self.__eddieUserId

    async def getStashiocatUserId(self) -> str | None:
        return self.__stashiocatUserId
