from typing import Final

from .twitchChatMessengerInterface import TwitchChatMessengerInterface
from ...location.timeZoneRepositoryInterface import TimeZoneRepositoryInterface
from ...misc import utils as utils
from ...misc.backgroundTaskHelperInterface import BackgroundTaskHelperInterface
from ...timber.timberInterface import TimberInterface


class TwitchChatMessenger(TwitchChatMessengerInterface):

    def __init__(
        self,
        backgroundTaskHelper: BackgroundTaskHelperInterface,
        timber: TimberInterface,
        timeZoneRepository: TimeZoneRepositoryInterface,
    ):
        if not isinstance(backgroundTaskHelper, BackgroundTaskHelperInterface):
            raise TypeError(f'backgroundTaskHelper argument is malformed: \"{backgroundTaskHelper}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(timeZoneRepository, TimeZoneRepositoryInterface):
            raise TypeError(f'timeZoneRepository argument is malformed: \"{timeZoneRepository}\"')

        self.__backgroundTaskHelper: Final[BackgroundTaskHelperInterface] = backgroundTaskHelper
        self.__timber: Final[TimberInterface] = timber
        self.__timeZoneRepository: Final[TimeZoneRepositoryInterface] = timeZoneRepository

        self.__isStarted: bool = False

    def start(self):
        if self.__isStarted:
            self.__timber.log('TwitchChatMessenger', 'Not starting TwitchChatMessenger as it has already been started')
            return

        self.__isStarted = True
        self.__timber.log('TwitchChatMessenger', 'Starting TwitchChatMessenger...')
        self.__backgroundTaskHelper.createTask(self.__startMessageLoop())

    async def __startMessageLoop(self):
        # TODO
        pass

    def submit(
        self,
        text: str,
        twitchChannelId: str,
        delaySeconds: int | None = None,
        replyMessageId: str | None = None,
    ):
        if not isinstance(text, str):
            raise TypeError(f'text argument is malformed: \"{text}\"')
        elif not utils.isValidStr(twitchChannelId):
            raise TypeError(f'twitchChannelId argument is malformed: \"{twitchChannelId}\"')
        elif delaySeconds is not None and (not utils.isValidInt(delaySeconds) or delaySeconds < 1):
            raise TypeError(f'delaySeconds argument is malformed: \"{delaySeconds}\"')
        elif replyMessageId is not None and not isinstance(replyMessageId, str):
            raise TypeError(f'replyMessageId argument is malformed: \"{replyMessageId}\"')

        # TODO
        pass
