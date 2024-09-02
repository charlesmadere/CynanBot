import locale

from frozenlist import FrozenList

from .twitchChannelProvider import TwitchChannelProvider
from ..absTwitchPollHandler import AbsTwitchPollHandler
from ..api.twitchPollChoice import TwitchPollChoice
from ..api.twitchPollStatus import TwitchPollStatus
from ..api.websocket.twitchWebsocketDataBundle import TwitchWebsocketDataBundle
from ..api.websocket.twitchWebsocketSubscriptionType import TwitchWebsocketSubscriptionType
from ..twitchUtilsInterface import TwitchUtilsInterface
from ...misc import utils as utils
from ...streamAlertsManager.streamAlert import StreamAlert
from ...streamAlertsManager.streamAlertsManagerInterface import StreamAlertsManagerInterface
from ...timber.timberInterface import TimberInterface
from ...tts.ttsEvent import TtsEvent
from ...tts.ttsProvider import TtsProvider
from ...users.userInterface import UserInterface


class TwitchPollHandler(AbsTwitchPollHandler):

    def __init__(
        self,
        streamAlertsManager: StreamAlertsManagerInterface | None,
        timber: TimberInterface,
        twitchUtils: TwitchUtilsInterface
    ):
        if streamAlertsManager is not None and not isinstance(streamAlertsManager, StreamAlertsManagerInterface):
            raise TypeError(f'streamAlertsManager argument is malformed: \"{streamAlertsManager}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(twitchUtils, TwitchUtilsInterface):
            raise TypeError(f'twitchUtils argument is malformed: \"{twitchUtils}\"')

        self.__streamAlertsManager: StreamAlertsManagerInterface | None = streamAlertsManager
        self.__timber: TimberInterface = timber
        self.__twitchUtils: TwitchUtilsInterface = twitchUtils

        self.__twitchChannelProvider: TwitchChannelProvider | None = None

    async def __notifyChatOfPollResults(
        self,
        pollChoices: FrozenList[TwitchPollChoice],
        broadcasterUserId: str,
        title: str,
        pollStatus: TwitchPollStatus | None,
        subscriptionType: TwitchWebsocketSubscriptionType,
        user: UserInterface
    ):
        if not isinstance(pollChoices, FrozenList):
            raise TypeError(f'pollChoices argument is malformed: \"{pollChoices}\"')
        elif not utils.isValidStr(broadcasterUserId):
            raise TypeError(f'broadcasterUserId argument is malformed: \"{broadcasterUserId}\"')
        elif not utils.isValidStr(title):
            raise TypeError(f'title argument is malformed: \"{title}\"')
        elif pollStatus is not None and not isinstance(pollStatus, TwitchPollStatus):
            raise TypeError(f'pollStatus argument is malformed: \"{pollStatus}\"')
        elif not isinstance(subscriptionType, TwitchWebsocketSubscriptionType):
            raise TypeError(f'subscriptionType argument is malformed: \"{subscriptionType}\"')
        elif not isinstance(user, UserInterface):
            raise TypeError(f'user argument is malformed: \"{user}\"')

        twitchChannelProvider = self.__twitchChannelProvider

        if twitchChannelProvider is None:
            return
        elif len(pollChoices) == 0:
            return
        elif pollStatus is not TwitchPollStatus.COMPLETED:
            return
        elif subscriptionType is not TwitchWebsocketSubscriptionType.CHANNEL_POLL_END:
            return
        elif not user.isNotifyOfPollResultsEnabled:
            return

        largestVoteCount = utils.getIntMinSafeSize()

        for pollChoice in pollChoices:
            if pollChoice.votes > largestVoteCount:
                largestVoteCount = pollChoice.votes

        if largestVoteCount < 1:
            return

        winningPollChoices: list[TwitchPollChoice] = list()

        for pollChoice in pollChoices:
            if pollChoice.votes == largestVoteCount:
                winningPollChoices.append(pollChoice)

        if len(winningPollChoices) == 0:
            # this case should be impossible but ehhhh let's just handle it
            return
        elif len(winningPollChoices) > 3:
            # edge case to handle a situation with a large number of ties
            return

        twitchChannel = await twitchChannelProvider.getTwitchChannel(user.getHandle())
        votesString = locale.format_string("%d", winningPollChoices[0].votes, grouping = True)
        votesPlurality: str

        if winningPollChoices[0].votes == 0:
            votesPlurality = 'vote'
        else:
            votesPlurality = 'votes'

        if len(winningPollChoices) == 1:
            await self.__twitchUtils.safeSend(twitchChannel, f'🗳️ The winner of the poll is \"{winningPollChoices[0].title}\", with {votesString} {votesPlurality}!')
            return

        winningTitleStrings: list[str] = list()
        for winningPollChoice in winningPollChoices:
            winningTitleStrings.append(f'\"{winningPollChoice.title}\"')
        winningTitlesString = ', '.join(winningTitleStrings)

        await self.__twitchUtils.safeSend(twitchChannel, f'🗳️ The poll winners are {winningTitlesString}, with {votesString} {votesPlurality}!')

    async def onNewPoll(
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

        payload = dataBundle.requirePayload()
        event = payload.event

        if event is None:
            self.__timber.log('TwitchPollHandler', f'Received a data bundle that has no event (channel=\"{user.getHandle()}\") ({dataBundle=})')
            return

        broadcasterUserId = event.broadcasterUserId
        title = event.title
        choices = event.choices

        if not utils.isValidStr(broadcasterUserId) or not utils.isValidStr(title) or choices is None or len(choices) == 0:
            self.__timber.log('TwitchPollHandler', f'Received a data bundle that is missing crucial data: (channel=\"{user.getHandle()}\") ({dataBundle=}) ({broadcasterUserId=}) ({title=}) ({choices=})')
            return

        subscriptionType = payload.requireSubscription().subscriptionType
        self.__timber.log('TwitchPollHandler', f'\"{user.getHandle()}\" received poll event ({title=}) ({choices=}) ({subscriptionType=})')

        await self.__processTtsEvent(
            broadcasterUserId = broadcasterUserId,
            title = title,
            userId = userId,
            subscriptionType = subscriptionType,
            user = user
        )

        await self.__notifyChatOfPollResults(
            pollChoices = choices,
            broadcasterUserId = broadcasterUserId,
            title = title,
            pollStatus = event.pollStatus,
            subscriptionType = subscriptionType,
            user = user
        )

    async def __processTtsEvent(
        self,
        broadcasterUserId: str,
        title: str,
        userId: str,
        subscriptionType: TwitchWebsocketSubscriptionType,
        user: UserInterface
    ):
        if not utils.isValidStr(broadcasterUserId):
            raise TypeError(f'broadcasterUserId argument is malformed: \"{broadcasterUserId}\"')
        elif not utils.isValidStr(title):
            raise TypeError(f'title argument is malformed: \"{title}\"')
        elif not utils.isValidStr(userId):
            raise TypeError(f'userId argument is malformed: \"{userId}\"')
        elif not isinstance(subscriptionType, TwitchWebsocketSubscriptionType):
            raise TypeError(f'subscriptionType argument is malformed: \"{subscriptionType}\"')
        elif not isinstance(user, UserInterface):
            raise TypeError(f'user argument is malformed: \"{user}\"')

        streamAlertsManager = self.__streamAlertsManager

        if streamAlertsManager is None:
            return
        elif not user.isTtsEnabled():
            return
        elif subscriptionType is not TwitchWebsocketSubscriptionType.CHANNEL_POLL_BEGIN:
            return

        streamAlertsManager.submitAlert(StreamAlert(
            soundAlert = None,
            twitchChannel = user.getHandle(),
            twitchChannelId = broadcasterUserId,
            ttsEvent = TtsEvent(
                message = f'A new poll has begun! \"{title}\"',
                twitchChannel = user.getHandle(),
                twitchChannelId = broadcasterUserId,
                userId = userId,
                userName = user.getHandle(),
                donation = None,
                provider = TtsProvider.DEC_TALK,
                raidInfo = None
            )
        ))

    def setTwitchChannelProvider(self, provider: TwitchChannelProvider | None):
        if provider is not None and not isinstance(provider, TwitchChannelProvider):
            raise TypeError(f'provider argument is malformed: \"{provider}\"')

        self.__twitchChannelProvider = provider
