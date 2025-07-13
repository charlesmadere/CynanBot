from typing import Final

from twitchio.channel import Channel

from ..twitchChannel import TwitchChannel
from ..twitchConfigurationType import TwitchConfigurationType
from ..twitchMessageable import TwitchMessageable
from ....users.userIdsRepositoryInterface import UserIdsRepositoryInterface


class TwitchIoChannel(TwitchChannel, TwitchMessageable):

    def __init__(
        self,
        channel: Channel,
        userIdsRepository: UserIdsRepositoryInterface,
    ):
        if not isinstance(channel, Channel):
            raise TypeError(f'channel argument is malformed: \"{channel}\"')
        elif not isinstance(userIdsRepository, UserIdsRepositoryInterface):
            raise TypeError(f'userIdsRepository argument is malformed: \"{userIdsRepository}\"')

        self.__channel: Final[Channel] = channel
        self.__userIdsRepository: Final[UserIdsRepositoryInterface] = userIdsRepository

        self.__twitchChannelId: str | None = None

    async def getTwitchChannelId(self) -> str:
        twitchChannelId = self.__twitchChannelId

        if twitchChannelId is None:
            twitchChannelId = await self.__userIdsRepository.requireUserId(
                userName = self.getTwitchChannelName()
            )

            self.__twitchChannelId = twitchChannelId

        return twitchChannelId

    def getTwitchChannelName(self) -> str:
        return self.__channel.name

    def __repr__(self) -> str:
        return self.getTwitchChannelName()

    async def send(self, message: str):
        await self.__channel.send(message)

    @property
    def twitchConfigurationType(self) -> TwitchConfigurationType:
        return TwitchConfigurationType.TWITCHIO
