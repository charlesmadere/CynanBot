import random
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Final

from .mostRecentAnivMessageTimeoutHelperInterface import MostRecentAnivMessageTimeoutHelperInterface
from .whichAnivUserHelperInterface import WhichAnivUserHelperInterface
from ..models.anivCopyMessageTimeoutScore import AnivCopyMessageTimeoutScore
from ..models.anivTimeoutData import AnivTimeoutData
from ..models.mostRecentAnivMessage import MostRecentAnivMessage
from ..repositories.anivCopyMessageTimeoutScoreRepositoryInterface import \
    AnivCopyMessageTimeoutScoreRepositoryInterface
from ..repositories.mostRecentAnivMessageRepositoryInterface import MostRecentAnivMessageRepositoryInterface
from ..settings.anivSettingsRepositoryInterface import AnivSettingsRepositoryInterface
from ...language.languageEntry import LanguageEntry
from ...location.timeZoneRepositoryInterface import TimeZoneRepositoryInterface
from ...misc import utils as utils
from ...timber.timberInterface import TimberInterface
from ...trollmoji.trollmojiHelperInterface import TrollmojiHelperInterface
from ...twitch.channelEditors.twitchChannelEditorsRepositoryInterface import TwitchChannelEditorsRepositoryInterface
from ...twitch.configuration.twitchChannelProvider import TwitchChannelProvider
from ...twitch.timeout.timeoutImmuneUserIdsRepositoryInterface import TimeoutImmuneUserIdsRepositoryInterface
from ...twitch.timeout.twitchTimeoutHelperInterface import TwitchTimeoutHelperInterface
from ...twitch.timeout.twitchTimeoutResult import TwitchTimeoutResult
from ...twitch.tokens.twitchTokensRepositoryInterface import TwitchTokensRepositoryInterface
from ...twitch.twitchHandleProviderInterface import TwitchHandleProviderInterface
from ...twitch.twitchUtilsInterface import TwitchUtilsInterface
from ...users.aniv.whichAnivUser import WhichAnivUser
from ...users.userInterface import UserInterface


class MostRecentAnivMessageTimeoutHelper(MostRecentAnivMessageTimeoutHelperInterface):

    @dataclass(frozen = True)
    class AnivUserData:
        userId: str
        whichAnivUser: WhichAnivUser

    def __init__(
        self,
        anivCopyMessageTimeoutScoreRepository: AnivCopyMessageTimeoutScoreRepositoryInterface,
        anivSettingsRepository: AnivSettingsRepositoryInterface,
        mostRecentAnivMessageRepository: MostRecentAnivMessageRepositoryInterface,
        timber: TimberInterface,
        timeoutImmuneUserIdsRepository: TimeoutImmuneUserIdsRepositoryInterface,
        timeZoneRepository: TimeZoneRepositoryInterface,
        trollmojiHelper: TrollmojiHelperInterface,
        twitchChannelEditorsRepository: TwitchChannelEditorsRepositoryInterface,
        twitchHandleProvider: TwitchHandleProviderInterface,
        twitchTimeoutHelper: TwitchTimeoutHelperInterface,
        twitchTokensRepository: TwitchTokensRepositoryInterface,
        twitchUtils: TwitchUtilsInterface,
        whichAnivUserHelper: WhichAnivUserHelperInterface,
    ):
        if not isinstance(anivCopyMessageTimeoutScoreRepository, AnivCopyMessageTimeoutScoreRepositoryInterface):
            raise TypeError(f'anivCopyMessageTimeoutScoreRepository argument is malformed: \"{anivCopyMessageTimeoutScoreRepository}\"')
        elif not isinstance(anivSettingsRepository, AnivSettingsRepositoryInterface):
            raise TypeError(f'anivSettingsRepository argument is malformed: \"{anivSettingsRepository}\"')
        elif not isinstance(mostRecentAnivMessageRepository, MostRecentAnivMessageRepositoryInterface):
            raise TypeError(f'mostRecentAnivMessageRepository argument is malformed: \"{mostRecentAnivMessageRepository}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(timeoutImmuneUserIdsRepository, TimeoutImmuneUserIdsRepositoryInterface):
            raise TypeError(f'timeoutImmuneUserIdsRepository argument is malformed: \"{timeoutImmuneUserIdsRepository}\"')
        elif not isinstance(timeZoneRepository, TimeZoneRepositoryInterface):
            raise TypeError(f'timeZoneRepository argument is malformed: \"{timeZoneRepository}\"')
        elif not isinstance(trollmojiHelper, TrollmojiHelperInterface):
            raise TypeError(f'trollmojiHelper argument is malformed: \"{trollmojiHelper}\"')
        elif not isinstance(twitchChannelEditorsRepository, TwitchChannelEditorsRepositoryInterface):
            raise TypeError(f'twitchChannelEditorsRepository argument is malformed: \"{twitchChannelEditorsRepository}\"')
        elif not isinstance(twitchHandleProvider, TwitchHandleProviderInterface):
            raise TypeError(f'twitchHandleProvider argument is malformed: \"{twitchHandleProvider}\"')
        elif not isinstance(twitchTimeoutHelper, TwitchTimeoutHelperInterface):
            raise TypeError(f'twitchTimeoutHelper argument is malformed: \"{twitchTimeoutHelper}\"')
        elif not isinstance(twitchTokensRepository, TwitchTokensRepositoryInterface):
            raise TypeError(f'twitchTokensRepository argument is malformed: \"{twitchTokensRepository}\"')
        elif not isinstance(twitchUtils, TwitchUtilsInterface):
            raise TypeError(f'twitchUtils argument is malformed: \"{twitchUtils}\"')
        elif not isinstance(whichAnivUserHelper, WhichAnivUserHelperInterface):
            raise TypeError(f'whichAnivUserHelper argument is malformed: \"{whichAnivUserHelper}\"')

        self.__anivCopyMessageTimeoutScoreRepository: Final[AnivCopyMessageTimeoutScoreRepositoryInterface] = anivCopyMessageTimeoutScoreRepository
        self.__anivSettingsRepository: Final[AnivSettingsRepositoryInterface] = anivSettingsRepository
        self.__mostRecentAnivMessageRepository: Final[MostRecentAnivMessageRepositoryInterface] = mostRecentAnivMessageRepository
        self.__timber: Final[TimberInterface] = timber
        self.__timeoutImmuneUserIdsRepository: Final[TimeoutImmuneUserIdsRepositoryInterface] = timeoutImmuneUserIdsRepository
        self.__timeZoneRepository: Final[TimeZoneRepositoryInterface] = timeZoneRepository
        self.__trollmojiHelper: Final[TrollmojiHelperInterface] = trollmojiHelper
        self.__twitchChannelEditorsRepository: Final[TwitchChannelEditorsRepositoryInterface] = twitchChannelEditorsRepository
        self.__twitchHandleProvider: Final[TwitchHandleProviderInterface] = twitchHandleProvider
        self.__twitchTimeoutHelper: Final[TwitchTimeoutHelperInterface] = twitchTimeoutHelper
        self.__twitchTokensRepository: Final[TwitchTokensRepositoryInterface] = twitchTokensRepository
        self.__twitchUtils: Final[TwitchUtilsInterface] = twitchUtils
        self.__whichAnivUserHelper: Final[WhichAnivUserHelperInterface] = whichAnivUserHelper

        self.__twitchChannelProvider: TwitchChannelProvider | None = None

    async def checkMessageAndMaybeTimeout(
        self,
        chatterMessage: str | None,
        chatterUserId: str,
        chatterUserName: str,
        twitchChannelId: str,
        user: UserInterface
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

        if not user.isAnivMessageCopyTimeoutEnabled:
            return False

        anivUser = await self.__whichAnivUserHelper.getAnivUser(
            twitchChannelId = twitchChannelId,
            whichAnivUser = user.whichAnivUser,
        )

        if anivUser is None or anivUser.userId == chatterUserId or twitchChannelId == chatterUserId:
            return False

        chatterMessage = utils.cleanStr(chatterMessage)

        anivMessage = await self.__mostRecentAnivMessageRepository.get(
            twitchChannelId = twitchChannelId
        )

        if not utils.isValidStr(chatterMessage) or anivMessage is None or not utils.isValidStr(anivMessage.message):
            return False

        now = datetime.now(self.__timeZoneRepository.getDefault())
        expirationTime = await self.__determineExpirationTime(anivMessage, user)

        if chatterMessage != anivMessage.message or expirationTime < now:
            return False

        if await self.__isImmuneChatter(
            chatterUserId = chatterUserId,
            twitchChannelId = twitchChannelId,
        ):
            self.__timber.log('MostRecentAnivMessageTimeoutHelper', f'In {user.handle}, not proceeding with potentially timing out {chatterUserId}:{chatterUserId}, as they are an immune editor ({twitchChannelId=})')
            return False

        twitchHandle = await self.__twitchHandleProvider.getTwitchHandle()
        twitchAccessToken = await self.__twitchTokensRepository.getAccessToken(twitchHandle)
        if not utils.isValidStr(twitchAccessToken):
            self.__timber.log('MostRecentAnivMessageTimeoutHelper', f'In {user.handle}, failed to fetch Twitch access token when potentially trying to time out {chatterUserName}:{chatterUserId} for copying a message from aniv ({twitchChannelId=})')
            return False

        twitchChannelAccessToken = await self.__twitchTokensRepository.getAccessTokenById(twitchChannelId)
        if not utils.isValidStr(twitchChannelAccessToken):
            self.__timber.log('MostRecentAnivMessageTimeoutHelper', f'In {user.handle}, failed to fetch Twitch channel access token when potentially trying to time out {chatterUserName}:{chatterUserId} for copying a message from aniv ({twitchChannelId=})')
            return False

        timeoutData = await self.__determineTimeoutData(user)

        if timeoutData is None:
            self.__timber.log('MostRecentAnivMessageTimeoutHelper', f'In {user.handle}, {chatterUserName}:{chatterUserId} got away with copying a message from aniv ({twitchChannelId=})')

            await self.__anivCopyMessageTimeoutScoreRepository.incrementDodgeScore(
                chatterUserId = chatterUserId,
                chatterUserName = chatterUserName,
                twitchChannel = user.handle,
                twitchChannelId = twitchChannelId,
            )

            return False

        reason = await self.__determineTimeoutReason(
            timeoutData = timeoutData,
            user = user,
            anivUser = anivUser,
        )

        timeoutResult = await self.__twitchTimeoutHelper.timeout(
            durationSeconds = timeoutData.durationSeconds,
            reason = reason,
            twitchAccessToken = twitchAccessToken,
            twitchChannelAccessToken = twitchChannelAccessToken,
            twitchChannelId = twitchChannelId,
            userIdToTimeout = chatterUserId,
            user = user,
        )

        if timeoutResult is not TwitchTimeoutResult.SUCCESS:
            self.__timber.log('MostRecentAnivMessageTimeoutHelper', f'In {user.handle}, failed to timeout {chatterUserName}:{chatterUserId} for copying a message from aniv ({timeoutResult=})')
            return False

        timeoutScore = await self.__anivCopyMessageTimeoutScoreRepository.incrementTimeoutScore(
            timeoutDurationSeconds = timeoutData.durationSeconds,
            chatterUserId = chatterUserId,
            chatterUserName = chatterUserName,
            twitchChannel = user.handle,
            twitchChannelId = twitchChannelId
        )

        self.__timber.log('MostRecentAnivMessageTimeoutHelper', f'In {user.handle}, {chatterUserName}:{chatterUserId} was timed out for copying a message from aniv')

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

    async def __determineTimeoutData(self, user: UserInterface) -> AnivTimeoutData | None:
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

    async def __determineTimeoutReason(
        self,
        timeoutData: AnivTimeoutData,
        user: UserInterface,
        anivUser: WhichAnivUserHelperInterface.Result,
    ) -> str:
        match user.defaultLanguage:
            case LanguageEntry.SPANISH:
                return f'{timeoutData.durationSecondsStr} de suspension por copiar un mensaje de {anivUser.userName}'

            case _:
                return f'{timeoutData.durationSecondsStr}s timeout for copying an {anivUser.userName} message'

    async def __isImmuneChatter(
        self,
        chatterUserId: str,
        twitchChannelId: str
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
        twitchChannel = await twitchChannelProvider.getTwitchChannel(user.handle)
        timeoutScoreString = await self.__timeoutScoreToString(timeoutScore)
        msg = f'@{chatterUserName} {emote} {timeoutData.durationSecondsStr}s {emote} {timeoutScoreString}'

        await self.__twitchUtils.safeSend(
            messageable = twitchChannel,
            message = msg,
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
