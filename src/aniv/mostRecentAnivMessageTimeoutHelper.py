import random
from datetime import datetime, timedelta

from .anivCopyMessageTimeoutScore import AnivCopyMessageTimeoutScore
from .anivCopyMessageTimeoutScoreRepositoryInterface import AnivCopyMessageTimeoutScoreRepositoryInterface
from .anivSettingsRepositoryInterface import AnivSettingsRepositoryInterface
from .anivTimeoutData import AnivTimeoutData
from .anivUserIdProviderInterface import AnivUserIdProviderInterface
from .mostRecentAnivMessage import MostRecentAnivMessage
from .mostRecentAnivMessageRepositoryInterface import MostRecentAnivMessageRepositoryInterface
from .mostRecentAnivMessageTimeoutHelperInterface import MostRecentAnivMessageTimeoutHelperInterface
from ..location.timeZoneRepositoryInterface import TimeZoneRepositoryInterface
from ..misc import utils as utils
from ..timber.timberInterface import TimberInterface
from ..trollmoji.trollmojiHelperInterface import TrollmojiHelperInterface
from ..twitch.configuration.twitchChannelProvider import TwitchChannelProvider
from ..twitch.timeout.twitchTimeoutHelperInterface import TwitchTimeoutHelperInterface
from ..twitch.timeout.twitchTimeoutResult import TwitchTimeoutResult
from ..twitch.twitchHandleProviderInterface import TwitchHandleProviderInterface
from ..twitch.twitchTokensRepositoryInterface import TwitchTokensRepositoryInterface
from ..twitch.twitchUtilsInterface import TwitchUtilsInterface
from ..users.userInterface import UserInterface


class MostRecentAnivMessageTimeoutHelper(MostRecentAnivMessageTimeoutHelperInterface):

    def __init__(
        self,
        anivCopyMessageTimeoutScoreRepository: AnivCopyMessageTimeoutScoreRepositoryInterface,
        anivSettingsRepository: AnivSettingsRepositoryInterface,
        anivUserIdProvider: AnivUserIdProviderInterface,
        mostRecentAnivMessageRepository: MostRecentAnivMessageRepositoryInterface,
        timber: TimberInterface,
        timeZoneRepository: TimeZoneRepositoryInterface,
        trollmojiHelper: TrollmojiHelperInterface,
        twitchHandleProvider: TwitchHandleProviderInterface,
        twitchTimeoutHelper: TwitchTimeoutHelperInterface,
        twitchTokensRepository: TwitchTokensRepositoryInterface,
        twitchUtils: TwitchUtilsInterface
    ):
        if not isinstance(anivCopyMessageTimeoutScoreRepository, AnivCopyMessageTimeoutScoreRepositoryInterface):
            raise TypeError(f'anivCopyMessageTimeoutScoreRepository argument is malformed: \"{anivCopyMessageTimeoutScoreRepository}\"')
        elif not isinstance(anivSettingsRepository, AnivSettingsRepositoryInterface):
            raise TypeError(f'anivSettingsRepository argument is malformed: \"{anivSettingsRepository}\"')
        elif not isinstance(anivUserIdProvider, AnivUserIdProviderInterface):
            raise TypeError(f'anivUserIdProvider argument is malformed: \"{anivUserIdProvider}\"')
        elif not isinstance(mostRecentAnivMessageRepository, MostRecentAnivMessageRepositoryInterface):
            raise TypeError(f'mostRecentAnivMessageRepository argument is malformed: \"{mostRecentAnivMessageRepository}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(timeZoneRepository, TimeZoneRepositoryInterface):
            raise TypeError(f'timeZoneRepository argument is malformed: \"{timeZoneRepository}\"')
        elif not isinstance(trollmojiHelper, TrollmojiHelperInterface):
            raise TypeError(f'trollmojiHelper argument is malformed: \"{trollmojiHelper}\"')
        elif not isinstance(twitchHandleProvider, TwitchHandleProviderInterface):
            raise TypeError(f'twitchHandleProvider argument is malformed: \"{twitchHandleProvider}\"')
        elif not isinstance(twitchTimeoutHelper, TwitchTimeoutHelperInterface):
            raise TypeError(f'twitchTimeoutHelper argument is malformed: \"{twitchTimeoutHelper}\"')
        elif not isinstance(twitchTokensRepository, TwitchTokensRepositoryInterface):
            raise TypeError(f'twitchTokensRepository argument is malformed: \"{twitchTokensRepository}\"')
        elif not isinstance(twitchUtils, TwitchUtilsInterface):
            raise TypeError(f'twitchUtils argument is malformed: \"{twitchUtils}\"')

        self.__anivCopyMessageTimeoutScoreRepository: AnivCopyMessageTimeoutScoreRepositoryInterface = anivCopyMessageTimeoutScoreRepository
        self.__anivSettingsRepository: AnivSettingsRepositoryInterface = anivSettingsRepository
        self.__anivUserIdProvider: AnivUserIdProviderInterface = anivUserIdProvider
        self.__mostRecentAnivMessageRepository: MostRecentAnivMessageRepositoryInterface = mostRecentAnivMessageRepository
        self.__timber: TimberInterface = timber
        self.__timeZoneRepository: TimeZoneRepositoryInterface = timeZoneRepository
        self.__trollmojiHelper: TrollmojiHelperInterface = trollmojiHelper
        self.__twitchHandleProvider: TwitchHandleProviderInterface = twitchHandleProvider
        self.__twitchTimeoutHelper: TwitchTimeoutHelperInterface = twitchTimeoutHelper
        self.__twitchTokensRepository: TwitchTokensRepositoryInterface = twitchTokensRepository
        self.__twitchUtils: TwitchUtilsInterface = twitchUtils

        self.__twitchChannelProvider: TwitchChannelProvider | None = None

    async def checkMessageAndMaybeTimeout(
        self,
        chatterMessage: str | None,
        chatterUserId: str,
        chatterUserName: str,
        twitchChannelId: str,
        user: UserInterface
    ) -> bool:
        if not user.isAnivMessageCopyTimeoutEnabled:
            return False

        anivUserId = await self.__anivUserIdProvider.getAnivUserId()

        if not utils.isValidStr(anivUserId) or anivUserId == chatterUserId or twitchChannelId == chatterUserId:
            return False

        chatterMessage = utils.cleanStr(chatterMessage)
        anivMessage = await self.__mostRecentAnivMessageRepository.get(twitchChannelId)

        if not utils.isValidStr(chatterMessage) or anivMessage is None or not utils.isValidStr(anivMessage.message):
            return False

        now = datetime.now(self.__timeZoneRepository.getDefault())
        expirationTime = await self.__determineExpirationTime(anivMessage, user)

        if chatterMessage != anivMessage.message or expirationTime < now:
            return False

        twitchHandle = await self.__twitchHandleProvider.getTwitchHandle()
        twitchAccessToken = await self.__twitchTokensRepository.getAccessToken(twitchHandle)
        if not utils.isValidStr(twitchAccessToken):
            self.__timber.log('MostRecentAnivMessageTimeoutHelper', f'Failed to fetch Twitch access token when potentially trying to time out {chatterUserName}:{chatterUserId} for copying a message from aniv')
            return False

        twitchChannelAccessToken = await self.__twitchTokensRepository.getAccessTokenById(twitchChannelId)
        if not utils.isValidStr(twitchChannelAccessToken):
            self.__timber.log('MostRecentAnivMessageTimeoutHelper', f'Failed to fetch Twitch channel access token when potentially trying to time out {chatterUserName}:{chatterUserId} for copying a message from aniv ({twitchChannelId=})')
            return False

        timeoutData = await self.__determineTimeout(user)
        if timeoutData is None:
            self.__timber.log('MostRecentAnivMessageTimeoutHelper', f'User {chatterUserName}:{chatterUserId} got away with copying a message from aniv!')

            await self.__anivCopyMessageTimeoutScoreRepository.incrementDodgeScore(
                chatterUserId = chatterUserId,
                chatterUserName = chatterUserName,
                twitchChannel = user.getHandle(),
                twitchChannelId = twitchChannelId
            )

            return False

        timeoutResult = await self.__twitchTimeoutHelper.timeout(
            durationSeconds = timeoutData.durationSeconds,
            reason = f'{timeoutData.durationSecondsStr}s timeout for copying an aniv message',
            twitchAccessToken = twitchAccessToken,
            twitchChannelAccessToken = twitchChannelAccessToken,
            twitchChannelId = twitchChannelId,
            userIdToTimeout = chatterUserId,
            user = user
        )

        if timeoutResult is not TwitchTimeoutResult.SUCCESS:
            self.__timber.log('MostRecentAnivMessageTimeoutHelper', f'Failed to timeout user {chatterUserName}:{chatterUserId} after they copied a message from aniv ({timeoutResult=})')
            return False

        timeoutScore = await self.__anivCopyMessageTimeoutScoreRepository.incrementTimeoutScore(
            timeoutDurationSeconds = timeoutData.durationSeconds,
            chatterUserId = chatterUserId,
            chatterUserName = chatterUserName,
            twitchChannel = user.getHandle(),
            twitchChannelId = twitchChannelId
        )

        self.__timber.log('MostRecentAnivMessageTimeoutHelper', f'User {chatterUserName}:{chatterUserId} was timed out for copying a message from aniv')

        await self.__ripBozoInChat(
            timeoutScore = timeoutScore,
            timeoutData = timeoutData,
            chatterUserName = chatterUserName,
            user = user
        )

        return True

    async def __determineExpirationTime(
        self,
        anivMessage: MostRecentAnivMessage,
        user: UserInterface
    ) -> datetime:
        maxAgeSeconds = user.anivMessageCopyMaxAgeSeconds
        if not utils.isValidInt(maxAgeSeconds):
            maxAgeSeconds = await self.__anivSettingsRepository.getCopyMessageMaxAgeSeconds()

        return anivMessage.dateTime + timedelta(seconds = maxAgeSeconds)

    async def __determineTimeout(self, user: UserInterface) -> AnivTimeoutData | None:
        if not isinstance(user, UserInterface):
            raise TypeError(f'user argument is malformed: \"{user}\"')

        timeoutProbability = user.anivMessageCopyTimeoutProbability
        if not utils.isValidNum(timeoutProbability):
            timeoutProbability = await self.__anivSettingsRepository.getCopyMessageTimeoutProbability()

        randomNumber = random.random()
        if randomNumber > timeoutProbability:
            return None

        minDurationSeconds = user.anivMessageCopyTimeoutMinSeconds
        if not utils.isValidInt(minDurationSeconds):
            minDurationSeconds = await self.__anivSettingsRepository.getCopyMessageTimeoutSeconds()

        maxDurationSeconds = user.anivMessageCopyTimeoutMaxSeconds
        if not utils.isValidInt(maxDurationSeconds):
            maxDurationSeconds = await self.__anivSettingsRepository.getCopyMessageTimeoutMaxSeconds()

        timeoutScale: float | None
        durationSeconds: int

        if await self.__anivSettingsRepository.isRandomTimeoutScalingEnabled():
            minFloat = float(minDurationSeconds)
            maxFloat = float(maxDurationSeconds)
            timeoutScale = random.random()
            durationSeconds = int(round(pow(timeoutScale, 9) * (maxFloat - minFloat) + minFloat))
        else:
            timeoutScale = None
            durationSeconds = minDurationSeconds

        return AnivTimeoutData(
            randomNumber = randomNumber,
            timeoutScale = timeoutScale,
            timeoutProbability = timeoutProbability,
            durationSeconds = durationSeconds
        )

    async def __ripBozoInChat(
        self,
        timeoutScore: AnivCopyMessageTimeoutScore,
        timeoutData: AnivTimeoutData,
        chatterUserName: str,
        user: UserInterface
    ):
        if not user.isAnivMessageCopyTimeoutChatReportingEnabled:
            return

        twitchChannelProvider = self.__twitchChannelProvider

        if twitchChannelProvider is None:
            return

        emote = await self.__trollmojiHelper.getGottemEmoteOrBackup()
        twitchChannel = await twitchChannelProvider.getTwitchChannel(user.getHandle())
        timeoutScoreString = await self.__timeoutScoreToString(timeoutScore)
        msg = f'@{chatterUserName} {emote} {timeoutData.durationSecondsStr}s {emote} {timeoutScoreString}'

        await self.__twitchUtils.safeSend(
            messageable = twitchChannel,
            message = msg
        )

    def setTwitchChannelProvider(self, provider: TwitchChannelProvider | None):
        if provider is not None and not isinstance(provider, TwitchChannelProvider):
            raise TypeError(f'provider argument is malformed: \"{provider}\"')

        self.__twitchChannelProvider = provider

    async def __timeoutScoreToString(self, timeoutScore: AnivCopyMessageTimeoutScore) -> str:
        statsString = f'{timeoutScore.dodgeScoreStr}D-{timeoutScore.timeoutScoreStr}T'

        dodgePercentString: str
        if timeoutScore.dodgeScore == 0:
            dodgePercentString = f'0% dodge rate'
        elif timeoutScore.timeoutScore == 0:
            dodgePercentString = f'100% dodge rate'
        else:
            totalDodgesAndTimeouts = timeoutScore.dodgeScore + timeoutScore.timeoutScore
            dodgePercent = round((float(timeoutScore.dodgeScore) / float(totalDodgesAndTimeouts)) * float(100), 2)
            dodgePercentString = f'{dodgePercent}% dodge rate'

        return f'({statsString}, {dodgePercentString})'
