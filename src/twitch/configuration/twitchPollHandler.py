from typing import Final

from ..absTwitchPollHandler import AbsTwitchPollHandler
from ..api.models.twitchWebsocketDataBundle import TwitchWebsocketDataBundle
from ..api.models.twitchWebsocketSubscriptionType import TwitchWebsocketSubscriptionType
from ..chatMessenger.twitchChatMessengerInterface import TwitchChatMessengerInterface
from ..localModels.mapper.twitchLocalModelsMapperInterface import TwitchLocalModelsMapperInterface
from ..localModels.twitchPollChoice import TwitchPollChoice
from ..localModels.twitchPollStatus import TwitchPollStatus
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
        twitchChatMessenger: TwitchChatMessengerInterface,
        twitchLocalModelsMapper: TwitchLocalModelsMapperInterface,
    ):
        if not isinstance(streamAlertsManager, StreamAlertsManagerInterface):
            raise TypeError(f'streamAlertsManager argument is malformed: \"{streamAlertsManager}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(twitchChatMessenger, TwitchChatMessengerInterface):
            raise TypeError(f'twitchChatMessenger argument is malformed: \"{twitchChatMessenger}\"')
        elif not isinstance(twitchLocalModelsMapper, TwitchLocalModelsMapperInterface):
            raise TypeError(f'twitchLocalModelsMapper argument is malformed: \"{twitchLocalModelsMapper}\"')

        self.__streamAlertsManager: Final[StreamAlertsManagerInterface] = streamAlertsManager
        self.__timber: Final[TimberInterface] = timber
        self.__twitchChatMessenger: Final[TwitchChatMessengerInterface] = twitchChatMessenger
        self.__twitchLocalModelsMapper: Final[TwitchLocalModelsMapperInterface] = twitchLocalModelsMapper

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

        votesString = winningPollChoices[0].votesStr

        votesPlurality: str
        if winningPollChoices[0].votes == 1:
            votesPlurality = 'vote'
        else:
            votesPlurality = 'votes'

        if len(winningPollChoices) == 1:
            self.__twitchChatMessenger.send(
                text = f'🗳️ The winner of the poll is \"{winningPollChoices[0].title}\", with {votesString} {votesPlurality}!',
                twitchChannelId = pollData.twitchChannelId,
            )
            return
        elif len(winningPollChoices) == 2:
            self.__twitchChatMessenger.send(
                text = f'🗳️ The poll winners are \"{winningPollChoices[0].title}\" and \"{winningPollChoices[1].title}\", with {votesString} {votesPlurality}!',
                twitchChannelId = pollData.twitchChannelId,
            )
            return

        winningTitlesString = ''
        for index, winningPollChoice in enumerate(winningPollChoices):
            if index == 0:
                winningTitlesString = f'\"{winningPollChoice.title}\"'
            elif index + 1 == len(winningPollChoices):
                winningTitlesString = f'{winningTitlesString}, and \"{winningPollChoice.title}\"'
            else:
                winningTitlesString = f'{winningTitlesString}, \"{winningPollChoice.title}\"'

        self.__twitchChatMessenger.send(
            text = f'🗳️ The poll winners are {winningTitlesString}, with {votesString} {votesPlurality}!',
            twitchChannelId = pollData.twitchChannelId,
        )

    async def __notifyChatOfPollStart(self, pollData: AbsTwitchPollHandler.PollData):
        user = pollData.user

        if not user.isNotifyOfPollStartEnabled:
            return
        elif pollData.subscriptionType is not TwitchWebsocketSubscriptionType.CHANNEL_POLL_BEGIN:
            return

        # intentionally empty for now
        pass

    async def onNewPoll(self, pollData: AbsTwitchPollHandler.PollData):
        if not isinstance(pollData, AbsTwitchPollHandler.PollData):
            raise TypeError(f'pollData argument is malformed: \"{pollData}\"')

        if pollData.user.isTtsEnabled:
            await self.__processTtsEvent(
                pollData = pollData,
            )

        if pollData.user.isNotifyOfPollStartEnabled:
            await self.__notifyChatOfPollStart(
                pollData = pollData,
            )

        if pollData.user.isNotifyOfPollResultsEnabled:
            await self.__notifyChatOfPollResults(
                pollData = pollData,
            )

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

        choices = await self.__twitchLocalModelsMapper.mapPollChoices(event.choices)
        title = event.title
        pollStatus = await self.__twitchLocalModelsMapper.mapPollStatus(event.pollStatus)
        subscriptionType = dataBundle.metadata.subscriptionType

        if len(choices) == 0 or not utils.isValidStr(title) or pollStatus is None or subscriptionType is None:
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
