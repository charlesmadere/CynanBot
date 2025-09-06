import random
from datetime import datetime, timedelta
from typing import Final

from frozendict import frozendict
from frozenlist import FrozenList

from .mostRecentAnivMessageTimeoutHelperInterface import MostRecentAnivMessageTimeoutHelperInterface
from ..models.anivTimeoutData import AnivTimeoutData
from ..models.mostRecentAnivMessage import MostRecentAnivMessage
from ..repositories.anivCopyMessageTimeoutScoreRepositoryInterface import \
    AnivCopyMessageTimeoutScoreRepositoryInterface
from ..repositories.anivUserIdsRepositoryInterface import AnivUserIdsRepositoryInterface
from ..repositories.mostRecentAnivMessageRepositoryInterface import MostRecentAnivMessageRepositoryInterface
from ..settings.anivSettingsInterface import AnivSettingsInterface
from ...aniv.models.whichAnivUser import WhichAnivUser
from ...language.languageEntry import LanguageEntry
from ...location.timeZoneRepositoryInterface import TimeZoneRepositoryInterface
from ...misc import utils as utils
from ...timber.timberInterface import TimberInterface
from ...timeout.idGenerator.timeoutIdGeneratorInterface import TimeoutIdGeneratorInterface
from ...timeout.machine.timeoutActionMachineInterface import TimeoutActionMachineInterface
from ...timeout.models.absTimeoutDuration import AbsTimeoutDuration
from ...timeout.models.actions.copyAnivMessageTimeoutAction import CopyAnivMessageTimeoutAction
from ...timeout.models.randomExponentialTimeoutDuration import RandomExponentialTimeoutDuration
from ...timeout.models.timeoutStreamStatusRequirement import TimeoutStreamStatusRequirement
from ...twitch.channelEditors.twitchChannelEditorsRepositoryInterface import TwitchChannelEditorsRepositoryInterface
from ...twitch.timeout.timeoutImmuneUserIdsRepositoryInterface import TimeoutImmuneUserIdsRepositoryInterface
from ...twitch.tokens.twitchTokensRepositoryInterface import TwitchTokensRepositoryInterface
from ...twitch.twitchHandleProviderInterface import TwitchHandleProviderInterface
from ...users.userIdsRepositoryInterface import UserIdsRepositoryInterface
from ...users.userInterface import UserInterface


class MostRecentAnivMessageTimeoutHelper(MostRecentAnivMessageTimeoutHelperInterface):

    def __init__(
        self,
        anivCopyMessageTimeoutScoreRepository: AnivCopyMessageTimeoutScoreRepositoryInterface,
        anivSettings: AnivSettingsInterface,
        anivUserIdsRepository: AnivUserIdsRepositoryInterface,
        mostRecentAnivMessageRepository: MostRecentAnivMessageRepositoryInterface,
        timber: TimberInterface,
        timeoutActionMachine: TimeoutActionMachineInterface,
        timeoutIdGenerator: TimeoutIdGeneratorInterface,
        timeoutImmuneUserIdsRepository: TimeoutImmuneUserIdsRepositoryInterface,
        timeZoneRepository: TimeZoneRepositoryInterface,
        twitchChannelEditorsRepository: TwitchChannelEditorsRepositoryInterface,
        twitchHandleProvider: TwitchHandleProviderInterface,
        twitchTokensRepository: TwitchTokensRepositoryInterface,
        userIdsRepository: UserIdsRepositoryInterface,
    ):
        if not isinstance(anivCopyMessageTimeoutScoreRepository, AnivCopyMessageTimeoutScoreRepositoryInterface):
            raise TypeError(f'anivCopyMessageTimeoutScoreRepository argument is malformed: \"{anivCopyMessageTimeoutScoreRepository}\"')
        elif not isinstance(anivSettings, AnivSettingsInterface):
            raise TypeError(f'anivSettings argument is malformed: \"{anivSettings}\"')
        elif not isinstance(anivUserIdsRepository, AnivUserIdsRepositoryInterface):
            raise TypeError(f'anivUserIdsRepository argument is malformed: \"{anivUserIdsRepository}\"')
        elif not isinstance(mostRecentAnivMessageRepository, MostRecentAnivMessageRepositoryInterface):
            raise TypeError(f'mostRecentAnivMessageRepository argument is malformed: \"{mostRecentAnivMessageRepository}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(timeoutActionMachine, TimeoutActionMachineInterface):
            raise TypeError(f'timeoutActionMachine argument is malformed: \"{timeoutActionMachine}\"')
        elif not isinstance(timeoutIdGenerator, TimeoutIdGeneratorInterface):
            raise TypeError(f'timeoutIdGenerator argument is malformed: \"{timeoutIdGenerator}\"')
        elif not isinstance(timeoutImmuneUserIdsRepository, TimeoutImmuneUserIdsRepositoryInterface):
            raise TypeError(f'timeoutImmuneUserIdsRepository argument is malformed: \"{timeoutImmuneUserIdsRepository}\"')
        elif not isinstance(timeZoneRepository, TimeZoneRepositoryInterface):
            raise TypeError(f'timeZoneRepository argument is malformed: \"{timeZoneRepository}\"')
        elif not isinstance(twitchChannelEditorsRepository, TwitchChannelEditorsRepositoryInterface):
            raise TypeError(f'twitchChannelEditorsRepository argument is malformed: \"{twitchChannelEditorsRepository}\"')
        elif not isinstance(twitchHandleProvider, TwitchHandleProviderInterface):
            raise TypeError(f'twitchHandleProvider argument is malformed: \"{twitchHandleProvider}\"')
        elif not isinstance(twitchTokensRepository, TwitchTokensRepositoryInterface):
            raise TypeError(f'twitchTokensRepository argument is malformed: \"{twitchTokensRepository}\"')
        elif not isinstance(userIdsRepository, UserIdsRepositoryInterface):
            raise TypeError(f'userIdsRepository argument is malformed: \"{userIdsRepository}\"')

        self.__anivCopyMessageTimeoutScoreRepository: Final[AnivCopyMessageTimeoutScoreRepositoryInterface] = anivCopyMessageTimeoutScoreRepository
        self.__anivSettings: Final[AnivSettingsInterface] = anivSettings
        self.__anivUserIdsRepository: Final[AnivUserIdsRepositoryInterface] = anivUserIdsRepository
        self.__mostRecentAnivMessageRepository: Final[MostRecentAnivMessageRepositoryInterface] = mostRecentAnivMessageRepository
        self.__timber: Final[TimberInterface] = timber
        self.__timeoutActionMachine: Final[TimeoutActionMachineInterface] = timeoutActionMachine
        self.__timeoutIdGenerator: Final[TimeoutIdGeneratorInterface] = timeoutIdGenerator
        self.__timeoutImmuneUserIdsRepository: Final[TimeoutImmuneUserIdsRepositoryInterface] = timeoutImmuneUserIdsRepository
        self.__timeZoneRepository: Final[TimeZoneRepositoryInterface] = timeZoneRepository
        self.__twitchChannelEditorsRepository: Final[TwitchChannelEditorsRepositoryInterface] = twitchChannelEditorsRepository
        self.__twitchHandleProvider: Final[TwitchHandleProviderInterface] = twitchHandleProvider
        self.__twitchTokensRepository: Final[TwitchTokensRepositoryInterface] = twitchTokensRepository
        self.__userIdsRepository: Final[UserIdsRepositoryInterface] = userIdsRepository

    async def checkMessageAndMaybeTimeout(
        self,
        chatterMessage: str | None,
        chatterUserId: str,
        chatterUserName: str,
        twitchChannelId: str,
        user: UserInterface,
    ) -> bool:
        if chatterMessage is not None and not isinstance(chatterMessage, str):
            raise TypeError(f'chatterMessage argument is malformed: \"{chatterMessage}\"')
        elif not utils.isValidStr(chatterUserId):
            raise TypeError(f'chatterUserId argument is malformed: \"{chatterUserId}\"')
        elif not utils.isValidStr(chatterUserName):
            raise TypeError(f'chatterUserName argument is malformed: \"{chatterUserName}\"')
        elif not utils.isValidStr(twitchChannelId):
            raise TypeError(f'twitchChannelId argument is malformed: \"{twitchChannelId}\"')
        elif not isinstance(user, UserInterface):
            raise TypeError(f'user argument is malformed: \"{user}\"')

        if not await self.__anivSettings.areCopyMessageTimeoutsEnabled():
            return False
        elif not user.isAnivMessageCopyTimeoutEnabled:
            return False
        elif chatterUserId == twitchChannelId:
            return False

        allAnivUsers = await self.__anivUserIdsRepository.getAllUsers()
        if chatterUserId in allAnivUsers.values():
            return False

        cleanedMessage = utils.cleanStr(chatterMessage)
        if not utils.isValidStr(cleanedMessage):
            return False

        copiedAnivMessage = await self.__findMatchingCopiedAnivMessage(
            cleanedMessage = cleanedMessage,
            twitchChannelId = twitchChannelId,
            user = user,
        )

        if copiedAnivMessage is None:
            return False

        anivUserId = allAnivUsers.get(copiedAnivMessage.whichAnivUser, None)
        if not utils.isValidStr(anivUserId):
            self.__timber.log('MostRecentAnivMessageTimeoutHelper', f'In {user.handle}, failed to fetch user ID for {copiedAnivMessage.whichAnivUser} when potentially trying to time out {chatterUserName}:{chatterUserId} for copying a message ({copiedAnivMessage=})')
            return False

        if await self.__isImmuneChatter(
            chatterUserId = chatterUserId,
            twitchChannelId = twitchChannelId,
        ):
            self.__timber.log('MostRecentAnivMessageTimeoutHelper', f'In {user.handle}, not proceeding with potentially timing out {chatterUserName}:{chatterUserId}, as they are an immune chatter ({copiedAnivMessage=})')
            return False

        userTwitchAccessToken = await self.__twitchTokensRepository.getAccessTokenById(
            twitchChannelId = twitchChannelId,
        )

        if not utils.isValidStr(userTwitchAccessToken):
            self.__timber.log('MostRecentAnivMessageTimeoutHelper', f'In {user.handle}, failed to fetch Twitch access token when potentially trying to time out {chatterUserName}:{chatterUserId} for copying a message ({copiedAnivMessage=})')
            return False
        elif not await self.__isTimeoutRoll(user):
            await self.__anivCopyMessageTimeoutScoreRepository.incrementDodgeScore(
                chatterUserId = chatterUserId,
                twitchChannelId = twitchChannelId,
            )
            return False

        moderatorUserId = await self.__userIdsRepository.requireUserId(
            userName = await self.__twitchHandleProvider.getTwitchHandle(),
            twitchAccessToken = userTwitchAccessToken,
        )

        moderatorTwitchAccessToken = await self.__twitchTokensRepository.requireAccessTokenById(
            twitchChannelId = moderatorUserId,
        )

        timeoutDuration = await self.__determineTimeoutDuration(
            user = user,
        )

        self.__timeoutActionMachine.submitAction(CopyAnivMessageTimeoutAction(
            timeoutDuration = timeoutDuration,
            actionId = await self.__timeoutIdGenerator.generateActionId(),
            anivUserId = anivUserId,
            moderatorTwitchAccessToken = moderatorTwitchAccessToken,
            moderatorUserId = moderatorUserId,
            targetUserId = chatterUserId,
            twitchChannelId = twitchChannelId,
            userTwitchAccessToken = userTwitchAccessToken,
            streamStatusRequirement = TimeoutStreamStatusRequirement.ANY,
            user = user,
            whichAnivUser = copiedAnivMessage.whichAnivUser,
        ))

        return True

    async def __determineTimeoutDuration(
        self,
        user: UserInterface,
    ) -> AbsTimeoutDuration:
        timeoutScale = random.random()

        minimumSeconds = user.anivMessageCopyTimeoutMinSeconds
        if not utils.isValidInt(minimumSeconds):
            minimumSeconds = await self.__anivSettings.getCopyMessageTimeoutSeconds()

        maximumSeconds = user.anivMessageCopyTimeoutMaxSeconds
        if not utils.isValidInt(maximumSeconds):
            maximumSeconds = await self.__anivSettings.getCopyMessageTimeoutMaxSeconds()

        return RandomExponentialTimeoutDuration(
            scale = timeoutScale,
            maximumSeconds = maximumSeconds,
            minimumSeconds = minimumSeconds,
        )

    async def __isTimeoutRoll(
        self,
        user: UserInterface,
    ) -> bool:
        if not isinstance(user, UserInterface):
            raise TypeError(f'user argument is malformed: \"{user}\"')

        timeoutProbability = user.anivMessageCopyTimeoutProbability
        if not utils.isValidNum(timeoutProbability):
            timeoutProbability = await self.__anivSettings.getCopyMessageTimeoutProbability()

        randomNumber = random.random()
        return randomNumber > timeoutProbability

    async def __determineTimeoutReason(
        self,
        timeoutData: AnivTimeoutData,
        anivUserName: str,
        user: UserInterface,
    ) -> str:
        match user.defaultLanguage:
            case LanguageEntry.SPANISH:
                return f'{timeoutData.durationSecondsStr} de suspension por copiar un mensaje de {anivUserName}'

            case _:
                return f'{timeoutData.durationMessage} timeout for copying an {anivUserName} message'

    async def __findMatchingCopiedAnivMessage(
        self,
        cleanedMessage: str,
        twitchChannelId: str,
        user: UserInterface,
    ) -> MostRecentAnivMessage | None:
        anivMessages = await self.__mostRecentAnivMessageRepository.get(
            twitchChannelId = twitchChannelId,
        )

        if len(anivMessages) == 0:
            return None

        validAnivMessages = await self.__trimToValidAnivMessagesOnly(
            anivMessages = anivMessages,
            user = user,
        )

        if len(validAnivMessages) == 0:
            return None

        for validAnivMessage in validAnivMessages:
            if validAnivMessage.message == cleanedMessage:
                return validAnivMessage

        return None

    async def __isImmuneChatter(
        self,
        chatterUserId: str,
        twitchChannelId: str,
    ) -> bool:
        if await self.__timeoutImmuneUserIdsRepository.isImmune(
            userId = chatterUserId,
        ):
            return True
        elif await self.__twitchChannelEditorsRepository.isEditor(
            chatterUserId = chatterUserId,
            twitchChannelId = twitchChannelId,
        ):
            return True
        else:
            return False

    async def __trimToValidAnivMessagesOnly(
        self,
        anivMessages: frozendict[WhichAnivUser, MostRecentAnivMessage | None],
        user: UserInterface,
    ) -> FrozenList[MostRecentAnivMessage]:
        validAnivMessages: FrozenList[MostRecentAnivMessage] = FrozenList()
        now = datetime.now(self.__timeZoneRepository.getDefault())

        maxAgeSeconds = user.anivMessageCopyMaxAgeSeconds
        if not utils.isValidInt(maxAgeSeconds):
            maxAgeSeconds = await self.__anivSettings.getCopyMessageMaxAgeSeconds()

        for anivUser, mostRecentMessage in anivMessages.items():
            if mostRecentMessage is None:
                continue

            expirationTime = mostRecentMessage.dateTime + timedelta(seconds = maxAgeSeconds)

            if expirationTime >= now:
                validAnivMessages.append(mostRecentMessage)

        validAnivMessages.freeze()
        return validAnivMessages
