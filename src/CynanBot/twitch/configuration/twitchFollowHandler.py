import CynanBot.misc.utils as utils
from CynanBot.timber.timberInterface import TimberInterface
from CynanBot.twitch.absTwitchFollowHandler import AbsTwitchFollowHandler
from CynanBot.twitch.api.websocket.twitchWebsocketDataBundle import \
    TwitchWebsocketDataBundle
from CynanBot.twitch.configuration.twitchChannelProvider import \
    TwitchChannelProvider
from CynanBot.twitch.followingStatus.twitchFollowingStatusRepositoryInterface import \
    TwitchFollowingStatusRepositoryInterface
from CynanBot.users.userInterface import UserInterface


class TwitchFollowHandler(AbsTwitchFollowHandler):

    def __init__(
        self,
        timber: TimberInterface,
        twitchChannelProvider: TwitchChannelProvider,
        twitchFollowingStatusRepository: TwitchFollowingStatusRepositoryInterface
    ):
        if not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(twitchChannelProvider, TwitchChannelProvider):
            raise TypeError(f'twitchChannelProvider argument is malformed: \"{twitchChannelProvider}\"')
        elif not isinstance(twitchFollowingStatusRepository, TwitchFollowingStatusRepositoryInterface):
            raise TypeError(f'twitchFollowingStatusRepository argument is malformed: \"{twitchFollowingStatusRepository}\"')

        self.__timber: TimberInterface = timber
        self.__twitchChannelProvider: TwitchChannelProvider = twitchChannelProvider
        self.__twitchFollowingStatusRepository: TwitchFollowingStatusRepositoryInterface = twitchFollowingStatusRepository

    async def onNewFollow(
        self,
        userId: str,
        user: UserInterface,
        dataBundle: TwitchWebsocketDataBundle
    ):
        if not utils.isValidStr(userId):
            raise TypeError(f'userId argument is malformed: \"{userId}\"')
        elif not isinstance(user, UserInterface):
            raise TypeError(f'user argument is malformed: \"{user}\"')
        elif not isinstance(dataBundle, TwitchWebsocketDataBundle):
            raise TypeError(f'dataBundle argument is malformed: \"{dataBundle}\"')

        event = dataBundle.requirePayload().event

        if event is None:
            self.__timber.log('TwitchFollowHandler', f'Received a data bundle that has no event (channel=\"{user.getHandle()}\") ({dataBundle=})')
            return

        # TODO
