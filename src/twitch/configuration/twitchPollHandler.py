from typing import Final

from .twitchChannelProvider import TwitchChannelProvider
from ..absTwitchPollHandler import AbsTwitchPollHandler
from ..api.models.twitchPollChoice import TwitchPollChoice
from ..api.models.twitchPollStatus import TwitchPollStatus
from ..api.models.twitchWebsocketDataBundle import TwitchWebsocketDataBundle
from ..api.models.twitchWebsocketSubscriptionType import TwitchWebsocketSubscriptionType
from ..api.twitchApiServiceInterface import TwitchApiServiceInterface
from ..twitchUtilsInterface import TwitchUtilsInterface
from ...misc import utils as utils
from ...streamAlertsManager.streamAlert import StreamAlert
from ...streamAlertsManager.streamAlertsManagerInterface import StreamAlertsManagerInterface
from ...timber.timberInterface import TimberInterface
from ...tts.models.ttsEvent import TtsEvent
from ...tts.models.ttsProviderOverridableStatus import TtsProviderOverridableStatus
from ...users.userInterface import UserInterface


class TwitchPollHandler(AbsTwitchPollHandler):

    def __init__(
        self,
        streamAlertsManager: StreamAlertsManagerInterface,
        timber: TimberInterface,
        twitchApiService: TwitchApiServiceInterface,
        twitchUtils: TwitchUtilsInterface,
    ):
        if not isinstance(streamAlertsManager, StreamAlertsManagerInterface):
            raise TypeError(f'streamAlertsManager argument is malformed: \"{streamAlertsManager}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(twitchApiService, TwitchApiServiceInterface):
            raise TypeError(f'twitchApiService argument is malformed: \"{twitchApiService}\"')
        elif not isinstance(twitchUtils, TwitchUtilsInterface):
            raise TypeError(f'twitchUtils argument is malformed: \"{twitchUtils}\"')

        self.__streamAlertsManager: Final[StreamAlertsManagerInterface] = streamAlertsManager
        self.__timber: Final[TimberInterface] = timber
        self.__twitchApiService: Final[TwitchApiServiceInterface] = twitchApiService
        self.__twitchUtils: Final[TwitchUtilsInterface] = twitchUtils

        self.__twitchChannelProvider: TwitchChannelProvider | None = None

    async def __notifyChatOfPollResults(self, pollData: AbsTwitchPollHandler.PollData):
        user = pollData.user
        pollChoices = pollData.choices
        pollStatus = pollData.pollStatus

        if not user.isNotifyOfPollResultsEnabled:
            return
        elif len(pollChoices) == 0:
            return
        elif pollStatus is not TwitchPollStatus.COMPLETED:
            return
        elif pollData.subscriptionType is not TwitchWebsocketSubscriptionType.CHANNEL_POLL_END:
            return

        twitchChannelProvider = self.__twitchChannelProvider
        if twitchChannelProvider is None:
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

        twitchChannel = await twitchChannelProvider.getTwitchChannel(user.handle)
        votesString = winningPollChoices[0].votesStr

        votesPlurality: str
        if winningPollChoices[0].votes == 1:
            votesPlurality = 'vote'
        else:
            votesPlurality = 'votes'

        if len(winningPollChoices) == 1:
            await self.__twitchUtils.safeSend(twitchChannel, f'🗳️ The winner of the poll is \"{winningPollChoices[0].title}\", with {votesString} {votesPlurality}!')
            return
        elif len(winningPollChoices) == 2:
            await self.__twitchUtils.safeSend(twitchChannel, f'🗳️ The poll winners are \"{winningPollChoices[0].title}\" and \"{winningPollChoices[1].title}\", with {votesString} {votesPlurality}!')
            return

        winningTitlesString = ''
        for index, winningPollChoice in enumerate(winningPollChoices):
            if index == 0:
                winningTitlesString = f'\"{winningPollChoice.title}\"'
            elif index + 1 == len(winningPollChoices):
                winningTitlesString = f'{winningTitlesString}, and \"{winningPollChoice.title}\"'
            else:
                winningTitlesString = f'{winningTitlesString}, \"{winningPollChoice.title}\"'

        await self.__twitchUtils.safeSend(twitchChannel, f'🗳️ The poll winners are {winningTitlesString}, with {votesString} {votesPlurality}!')

    async def __notifyChatOfPollStart(self, pollData: AbsTwitchPollHandler.PollData):
        user = pollData.user

        if not user.isNotifyOfPollStartEnabled:
            return
        elif pollData.subscriptionType is not TwitchWebsocketSubscriptionType.CHANNEL_POLL_BEGIN:
            return

        # TODO
        pass

    async def onNewPoll(self, pollData: AbsTwitchPollHandler.PollData):
        if not isinstance(pollData, AbsTwitchPollHandler.PollData):
            raise TypeError(f'pollData argument is malformed: \"{pollData}\"')

        if pollData.user.isTtsEnabled:
            await self.__processTtsEvent(pollData)

        if pollData.user.isNotifyOfPollStartEnabled:
            await self.__notifyChatOfPollStart(pollData)

        if pollData.user.isNotifyOfPollResultsEnabled:
            await self.__notifyChatOfPollResults(pollData)

    async def onNewPollDataBundle(
        self,
        twitchChannelId: str,
        user: UserInterface,
        dataBundle: TwitchWebsocketDataBundle,
    ):
        if not utils.isValidStr(twitchChannelId):
            raise TypeError(f'twitchChannelId argument is malformed: \"{twitchChannelId}\"')
        elif not isinstance(user, UserInterface):
            raise TypeError(f'user argument is malformed: \"{user}\"')
        elif not isinstance(dataBundle, TwitchWebsocketDataBundle):
            raise TypeError(f'dataBundle argument is malformed: \"{dataBundle}\"')

        event = dataBundle.requirePayload().event

        if event is None:
            self.__timber.log('TwitchPollHandler', f'Received a data bundle that is missing event data ({user=}) ({dataBundle=})')
            return

        choices = event.choices
        title = event.title
        pollStatus = event.pollStatus
        subscriptionType = dataBundle.metadata.subscriptionType

        if choices is None or len(choices) == 0 or not utils.isValidStr(title) or pollStatus is None or subscriptionType is None:
            self.__timber.log('TwitchPollHandler', f'Received a data bundle that is missing crucial data: ({user=}) ({dataBundle=}) ({choices=}) ({title=}) ({pollStatus=}) ({subscriptionType=})')
            return

        pollData = AbsTwitchPollHandler.PollData(
            choices = choices,
            title = title,
            twitchChannelId = twitchChannelId,
            pollStatus = pollStatus,
            subscriptionType = subscriptionType,
            user = user,
        )

        await self.onNewPoll(
            pollData = pollData,
        )

    async def __processTtsEvent(self, pollData: AbsTwitchPollHandler.PollData):
        user = pollData.user

        if not user.isTtsEnabled:
            return
        elif not user.isNotifyOfPollStartEnabled:
            return
        elif pollData.subscriptionType is not TwitchWebsocketSubscriptionType.CHANNEL_POLL_BEGIN:
            return

        self.__streamAlertsManager.submitAlert(StreamAlert(
            soundAlert = None,
            twitchChannel = user.handle,
            twitchChannelId = pollData.twitchChannelId,
            ttsEvent = TtsEvent(
                message = f'A new poll has begun! \"{pollData.title}\"',
                twitchChannel = user.handle,
                twitchChannelId = pollData.twitchChannelId,
                userId = pollData.twitchChannelId,
                userName = user.handle,
                donation = None,
                provider = user.defaultTtsProvider,
                providerOverridableStatus = TtsProviderOverridableStatus.THIS_EVENT_DISABLED,
                raidInfo = None,
            ),
        ))

    def setTwitchChannelProvider(self, provider: TwitchChannelProvider | None):
        if provider is not None and not isinstance(provider, TwitchChannelProvider):
            raise TypeError(f'provider argument is malformed: \"{provider}\"')

        self.__twitchChannelProvider = provider
