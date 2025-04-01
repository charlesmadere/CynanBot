import asyncio
import locale
import random
from dataclasses import dataclass
from typing import Any

from frozendict import frozendict

from .tntCheerAction import TntCheerAction
from .tntCheerActionHelperInterface import TntCheerActionHelperInterface
from ..absCheerAction import AbsCheerAction
from ..timeout.timeoutCheerActionMapper import TimeoutCheerActionMapper
from ...misc import utils as utils
from ...misc.backgroundTaskHelperInterface import BackgroundTaskHelperInterface
from ...recentGrenadeAttacks.helper.recentGrenadeAttacksHelperInterface import RecentGrenadeAttacksHelperInterface
from ...soundPlayerManager.provider.soundPlayerManagerProviderInterface import SoundPlayerManagerProviderInterface
from ...soundPlayerManager.soundAlert import SoundAlert
from ...timber.timberInterface import TimberInterface
from ...timeout.timeoutActionData import TimeoutActionData
from ...timeout.timeoutActionHelperInterface import TimeoutActionHelperInterface
from ...timeout.timeoutActionSettingsRepositoryInterface import TimeoutActionSettingsRepositoryInterface
from ...timeout.timeoutActionType import TimeoutActionType
from ...trollmoji.trollmojiHelperInterface import TrollmojiHelperInterface
from ...twitch.activeChatters.activeChatter import ActiveChatter
from ...twitch.activeChatters.activeChattersRepositoryInterface import ActiveChattersRepositoryInterface
from ...twitch.configuration.twitchChannelProvider import TwitchChannelProvider
from ...twitch.timeout.timeoutImmuneUserIdsRepositoryInterface import TimeoutImmuneUserIdsRepositoryInterface
from ...twitch.twitchMessageStringUtilsInterface import TwitchMessageStringUtilsInterface
from ...twitch.twitchUtilsInterface import TwitchUtilsInterface
from ...users.userInterface import UserInterface


class TntCheerActionHelper(TntCheerActionHelperInterface):

    @dataclass(frozen = True)
    class TntTarget:
        userId: str
        userName: str

        def __eq__(self, value: Any) -> bool:
            if isinstance(value, TntCheerActionHelper.TntTarget):
                return self.userId == value.userId
            else:
                return False

        def __hash__(self) -> int:
            return hash(self.userId)

    def __init__(
        self,
        activeChattersRepository: ActiveChattersRepositoryInterface,
        backgroundTaskHelper: BackgroundTaskHelperInterface,
        recentGrenadeAttacksHelper: RecentGrenadeAttacksHelperInterface,
        soundPlayerManagerProvider: SoundPlayerManagerProviderInterface,
        timber: TimberInterface,
        timeoutActionHelper: TimeoutActionHelperInterface,
        timeoutActionSettingsRepository: TimeoutActionSettingsRepositoryInterface,
        timeoutCheerActionMapper: TimeoutCheerActionMapper,
        timeoutImmuneUserIdsRepository: TimeoutImmuneUserIdsRepositoryInterface,
        trollmojiHelper: TrollmojiHelperInterface,
        twitchMessageStringUtils: TwitchMessageStringUtilsInterface,
        twitchUtils: TwitchUtilsInterface,
        grenadeAlertSleepTimeSeconds: float = 0.60,
        launchTntAlertSleepTimeSeconds: float = 2.00,
        tntAlertSleepTimeSeconds: float = 0.50
    ):
        if not isinstance(activeChattersRepository, ActiveChattersRepositoryInterface):
            raise TypeError(f'activeChattersRepository argument is malformed: \"{activeChattersRepository}\"')
        elif not isinstance(backgroundTaskHelper, BackgroundTaskHelperInterface):
            raise TypeError(f'backgroundTaskHelper argument is malformed: \"{backgroundTaskHelper}\"')
        elif not isinstance(recentGrenadeAttacksHelper, RecentGrenadeAttacksHelperInterface):
            raise TypeError(f'recentGrenadeAttacksHelper argument is malformed: \"{recentGrenadeAttacksHelper}\"')
        elif not isinstance(soundPlayerManagerProvider, SoundPlayerManagerProviderInterface):
            raise TypeError(f'soundPlayerManagerProvider argument is malformed: \"{soundPlayerManagerProvider}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(timeoutActionHelper, TimeoutActionHelperInterface):
            raise TypeError(f'timeoutActionHelper argument is malformed: \"{timeoutActionHelper}\"')
        elif not isinstance(timeoutActionSettingsRepository, TimeoutActionSettingsRepositoryInterface):
            raise TypeError(f'timeoutActionSettingsRepository argument is malformed: \"{timeoutActionSettingsRepository}\"')
        elif not isinstance(timeoutCheerActionMapper, TimeoutCheerActionMapper):
            raise TypeError(f'timeoutCheerActionMapper argument is malformed: \"{timeoutCheerActionMapper}\"')
        elif not isinstance(timeoutImmuneUserIdsRepository, TimeoutImmuneUserIdsRepositoryInterface):
            raise TypeError(f'timeoutImmuneUserIdsRepository argument is malformed: \"{timeoutImmuneUserIdsRepository}\"')
        elif not isinstance(twitchMessageStringUtils, TwitchMessageStringUtilsInterface):
            raise TypeError(f'twitchMessageStringUtils argument is malformed: \"{twitchMessageStringUtils}\"')
        elif not isinstance(trollmojiHelper, TrollmojiHelperInterface):
            raise TypeError(f'trollmojiHelper argument is malformed: \"{trollmojiHelper}\"')
        elif not isinstance(twitchUtils, TwitchUtilsInterface):
            raise TypeError(f'twitchUtils argument is malformed: \"{twitchUtils}\"')
        elif not utils.isValidNum(grenadeAlertSleepTimeSeconds):
            raise TypeError(f'grenadeAlertSleepTimeSeconds argument is malformed: \"{grenadeAlertSleepTimeSeconds}\"')
        elif grenadeAlertSleepTimeSeconds < 0.125 or grenadeAlertSleepTimeSeconds > 8:
            raise ValueError(f'soundAlertSleepTimeSeconds argument is out of bounds: {grenadeAlertSleepTimeSeconds}')
        elif not utils.isValidNum(launchTntAlertSleepTimeSeconds):
            raise TypeError(f'launchTntAlertSleepTimeSeconds argument is malformed: \"{launchTntAlertSleepTimeSeconds}\"')
        elif launchTntAlertSleepTimeSeconds < 0.125 or launchTntAlertSleepTimeSeconds > 8:
            raise ValueError(f'launchTntAlertSleepTimeSeconds argument is out of bounds: {launchTntAlertSleepTimeSeconds}')
        elif not utils.isValidNum(tntAlertSleepTimeSeconds):
            raise TypeError(f'tntAlertSleepTimeSeconds argument is malformed: \"{tntAlertSleepTimeSeconds}\"')
        elif tntAlertSleepTimeSeconds < 0.125 or tntAlertSleepTimeSeconds > 8:
            raise ValueError(f'tntAlertSleepTimeSeconds argument is out of bounds: {tntAlertSleepTimeSeconds}')

        self.__activeChattersRepository: ActiveChattersRepositoryInterface = activeChattersRepository
        self.__backgroundTaskHelper: BackgroundTaskHelperInterface = backgroundTaskHelper
        self.__recentGrenadeAttacksHelper: RecentGrenadeAttacksHelperInterface = recentGrenadeAttacksHelper
        self.__soundPlayerManagerProvider: SoundPlayerManagerProviderInterface = soundPlayerManagerProvider
        self.__timber: TimberInterface = timber
        self.__timeoutActionHelper: TimeoutActionHelperInterface = timeoutActionHelper
        self.__timeoutActionSettingsRepository: TimeoutActionSettingsRepositoryInterface = timeoutActionSettingsRepository
        self.__timeoutCheerActionMapper: TimeoutCheerActionMapper = timeoutCheerActionMapper
        self.__timeoutImmuneUserIdsRepository: TimeoutImmuneUserIdsRepositoryInterface = timeoutImmuneUserIdsRepository
        self.__trollmojiHelper: TrollmojiHelperInterface = trollmojiHelper
        self.__twitchUtils: TwitchUtilsInterface = twitchUtils
        self.__grenadeAlertSleepTimeSeconds: float = grenadeAlertSleepTimeSeconds
        self.__launchTntAlertSleepTimeSeconds: float = launchTntAlertSleepTimeSeconds
        self.__tntAlertSleepTimeSeconds: float = tntAlertSleepTimeSeconds

        self.__twitchChannelProvider: TwitchChannelProvider | None = None

    async def __alertViaTwitchChat(
        self,
        tntTargets: frozenset[TntTarget],
        durationSeconds: int,
        broadcasterUserId: str,
        cheerUserId: str,
        cheerUserName: str,
        twitchChatMessageId: str | None,
        user: UserInterface
    ):
        if len(tntTargets) == 0:
            return

        twitchChannelProvider = self.__twitchChannelProvider

        if twitchChannelProvider is None:
            return

        userNames: list[str] = list()

        for tntTarget in tntTargets:
            userNames.append(tntTarget.userName)

        durationSecondsString = locale.format_string("%d", durationSeconds, grouping = True)
        peopleCountString = locale.format_string("%d", len(tntTargets), grouping = True)

        peoplePluralityString: str
        if len(tntTargets) == 1:
            peoplePluralityString = f'{peopleCountString} person was hit'
        else:
            peoplePluralityString = f'{peopleCountString} people hit'

        userNames.sort(key = lambda userName: userName.casefold())
        userNamesString = ', '.join(userNames)

        bombEmote = await self.__trollmojiHelper.getBombEmoteOrBackup()
        twitchChannel = await twitchChannelProvider.getTwitchChannel(user.handle)
        message = f'{bombEmote} BOOM! {peoplePluralityString} with a {durationSecondsString}s timeout! {userNamesString} {bombEmote}'

        availableGrenades = await self.__recentGrenadeAttacksHelper.fetchAvailableGrenades(
            attackerUserId = cheerUserId,
            twitchChannel = user.handle,
            twitchChannelId = broadcasterUserId
        )

        if availableGrenades is not None:
            availableGrenadesString = locale.format_string("%d", availableGrenades, grouping=True)

            grenadesPluralization: str
            if availableGrenades == 1:
                grenadesPluralization = 'grenade'
            else:
                grenadesPluralization = 'grenades'

            message = f'{message} (@{cheerUserName} has {availableGrenadesString} {grenadesPluralization} remaining)'

        await self.__twitchUtils.safeSend(
            messageable = twitchChannel,
            message = message,
            replyMessageId = twitchChatMessageId
        )

    async def __chooseRandomGrenadeSoundAlert(self) -> SoundAlert:
        soundAlerts: list[SoundAlert] = [
            SoundAlert.GRENADE_1,
            SoundAlert.GRENADE_2,
            SoundAlert.GRENADE_3
        ]

        return random.choice(soundAlerts)

    async def __determineTntTargets(
        self,
        broadcasterUserId: str,
        cheerUserId: str,
        cheerUserName: str,
        tntAction: TntCheerAction
    ) -> frozenset[TntTarget]:
        tntTargets: set[TntCheerActionHelper.TntTarget] = set()

        additionalReverseProbability = await self.__timeoutActionSettingsRepository.getGrenadeAdditionalReverseProbability()
        randomReverseNumber = random.random()

        if randomReverseNumber <= additionalReverseProbability:
            tntTargets.add(TntCheerActionHelper.TntTarget(
                userId = cheerUserId,
                userName = cheerUserName
            ))

        chatters = await self.__activeChattersRepository.get(
            twitchChannelId = broadcasterUserId
        )

        eligibleChatters: dict[str, ActiveChatter] = dict()

        for chatter in chatters:
            eligibleChatters[chatter.chatterUserId] = chatter

        eligibleChatters.pop(broadcasterUserId, None)
        immuneUserIds = await self.__timeoutImmuneUserIdsRepository.getUserIds()

        for immuneUserId in immuneUserIds:
            eligibleChatters.pop(immuneUserId, None)

        tntTargetCount = random.randint(tntAction.minTimeoutChatters, tntAction.maxTimeoutChatters)
        eligibleChattersList: list[ActiveChatter] = list(eligibleChatters.values())

        while len(tntTargets) < tntTargetCount and len(eligibleChattersList) >= 1:
            randomChatterIndex = random.randint(0, len(eligibleChattersList) - 1)
            randomChatter = eligibleChattersList[randomChatterIndex]
            del eligibleChattersList[randomChatterIndex]

            tntTargets.add(TntCheerActionHelper.TntTarget(
                userId = randomChatter.chatterUserId,
                userName = randomChatter.chatterUserName
            ))

        frozenTntTargets: frozenset[TntCheerActionHelper.TntTarget] = frozenset(tntTargets)

        for tntTarget in frozenTntTargets:
            await self.__activeChattersRepository.remove(
                chatterUserId = tntTarget.userId,
                twitchChannelId = broadcasterUserId
            )

        self.__timber.log('TntCheerActionHelper', f'Selected TNT target(s) ({tntAction=}) ({additionalReverseProbability=}) ({randomReverseNumber=}) ({tntTargetCount=}) ({frozenTntTargets=})')

        return frozenTntTargets

    async def handleTntCheerAction(
        self,
        actions: frozendict[int, AbsCheerAction],
        bits: int,
        broadcasterUserId: str,
        cheerUserId: str,
        cheerUserName: str,
        message: str,
        moderatorTwitchAccessToken: str,
        moderatorUserId: str,
        twitchChatMessageId: str | None,
        userTwitchAccessToken: str,
        user: UserInterface
    ) -> bool:
        if not isinstance(actions, frozendict):
            raise TypeError(f'actions argument is malformed: \"{actions}\"')
        elif not utils.isValidInt(bits):
            raise TypeError(f'bits argument is malformed: \"{bits}\"')
        elif bits < 1 or bits > utils.getIntMaxSafeSize():
            raise ValueError(f'bits argument is out of bounds: {bits}')
        elif not utils.isValidStr(broadcasterUserId):
            raise TypeError(f'broadcasterUserId argument is malformed: \"{broadcasterUserId}\"')
        elif not utils.isValidStr(cheerUserId):
            raise TypeError(f'cheerUserId argument is malformed: \"{cheerUserId}\"')
        elif not utils.isValidStr(cheerUserName):
            raise TypeError(f'cheerUserName argument is malformed: \"{cheerUserName}\"')
        elif not utils.isValidStr(message):
            raise TypeError(f'message argument is malformed: \"{message}\"')
        elif not utils.isValidStr(moderatorTwitchAccessToken):
            raise TypeError(f'moderatorTwitchAccessToken argument is malformed: \"{moderatorTwitchAccessToken}\"')
        elif not utils.isValidStr(moderatorUserId):
            raise TypeError(f'moderatorUserId argument is malformed: \"{moderatorUserId}\"')
        elif twitchChatMessageId is not None and not isinstance(twitchChatMessageId, str):
            raise TypeError(f'twitchChatMessageId argument is malformed: \"{twitchChatMessageId}\"')
        elif not utils.isValidStr(userTwitchAccessToken):
            raise TypeError(f'userTwitchAccessToken argument is malformed: \"{userTwitchAccessToken}\"')
        elif not isinstance(user, UserInterface):
            raise TypeError(f'user argument is malformed: \"{user}\"')

        action = actions.get(bits, None)

        if not isinstance(action, TntCheerAction) or not action.isEnabled:
            return False
        elif not await self.__recentGrenadeAttacksHelper.canThrowGrenade(
            attackerUserId = cheerUserId,
            twitchChannel = user.handle,
            twitchChannelId = broadcasterUserId
        ):
            self.__timber.log('TntCheerActionHelper', f'No grenades available for this user ({cheerUserId=}) ({cheerUserName=}) ({user=}) ({action=})')
            return False

        tntTargets = await self.__determineTntTargets(
            broadcasterUserId = broadcasterUserId,
            cheerUserId = cheerUserId,
            cheerUserName = cheerUserName,
            tntAction = action
        )

        if len(tntTargets) == 0:
            return False

        await self.__noteGrenadeThrow(
            tntTargets = tntTargets,
            broadcasterUserId = broadcasterUserId,
            cheerUserId = cheerUserId,
            user = user
        )

        streamStatusRequirement = await self.__timeoutCheerActionMapper.toTimeoutActionDataStreamStatusRequirement(
            streamStatusRequirement = action.streamStatusRequirement
        )

        self.__backgroundTaskHelper.createTask(self.__playSoundAlerts(
            tntTargets = tntTargets,
            user = user
        ))

        durationSeconds = random.randint(action.minDurationSeconds, action.maxDurationSeconds)

        self.__backgroundTaskHelper.createTask(self.__alertViaTwitchChat(
            tntTargets = tntTargets,
            durationSeconds = durationSeconds,
            broadcasterUserId = broadcasterUserId,
            cheerUserId = cheerUserId,
            cheerUserName = cheerUserName,
            twitchChatMessageId = twitchChatMessageId,
            user = user
        ))

        for tntTarget in tntTargets:
            self.__timeoutActionHelper.submitTimeout(TimeoutActionData(
                isRandomChanceEnabled = False,
                bits = bits,
                durationSeconds = durationSeconds,
                chatMessage = message,
                instigatorUserId = cheerUserId,
                instigatorUserName = cheerUserName,
                moderatorTwitchAccessToken = moderatorTwitchAccessToken,
                moderatorUserId = moderatorUserId,
                pointRedemptionEventId = None,
                pointRedemptionMessage = None,
                pointRedemptionRewardId = None,
                timeoutTargetUserId = tntTarget.userId,
                timeoutTargetUserName = tntTarget.userName,
                twitchChannelId = broadcasterUserId,
                twitchChatMessageId = twitchChatMessageId,
                userTwitchAccessToken = userTwitchAccessToken,
                actionType = TimeoutActionType.TNT,
                streamStatusRequirement = streamStatusRequirement,
                user = user
            ))

        return True

    async def __noteGrenadeThrow(
        self,
        tntTargets: frozenset[TntTarget],
        broadcasterUserId: str,
        cheerUserId: str,
        user: UserInterface
    ):
        randomTntTarget = random.choice(list(tntTargets))

        await self.__recentGrenadeAttacksHelper.throwGrenade(
            attackedUserId = randomTntTarget.userId,
            attackerUserId = cheerUserId,
            twitchChannel = user.handle,
            twitchChannelId = broadcasterUserId
        )

    async def __playSoundAlerts(
        self,
        tntTargets: frozenset[TntTarget],
        user: UserInterface
    ):
        if not user.areSoundAlertsEnabled:
            return
        elif len(tntTargets) == 0:
            return

        soundPlayerManager = self.__soundPlayerManagerProvider.constructNewSoundPlayerManagerInstance()
        self.__backgroundTaskHelper.createTask(soundPlayerManager.playSoundAlert(SoundAlert.LAUNCH_TNT))
        await asyncio.sleep(self.__launchTntAlertSleepTimeSeconds)

        soundPlayerManager = self.__soundPlayerManagerProvider.constructNewSoundPlayerManagerInstance()
        self.__backgroundTaskHelper.createTask(soundPlayerManager.playSoundAlert(SoundAlert.TNT))
        await asyncio.sleep(self.__tntAlertSleepTimeSeconds)

        index = 0
        numberOfSounds = int(round(len(tntTargets) * 0.5))

        while index < numberOfSounds:
            soundAlert = await self.__chooseRandomGrenadeSoundAlert()
            soundPlayerManager = self.__soundPlayerManagerProvider.constructNewSoundPlayerManagerInstance()
            self.__backgroundTaskHelper.createTask(soundPlayerManager.playSoundAlert(soundAlert))
            index += 1

            await asyncio.sleep(self.__grenadeAlertSleepTimeSeconds)

        soundPlayerManager = self.__soundPlayerManagerProvider.constructNewSoundPlayerManagerInstance()
        self.__backgroundTaskHelper.createTask(soundPlayerManager.playSoundAlert(SoundAlert.SPLAT))

    def setTwitchChannelProvider(self, provider: TwitchChannelProvider | None):
        if provider is not None and not isinstance(provider, TwitchChannelProvider):
            raise TypeError(f'provider argument is malformed: \"{provider}\"')

        self.__twitchChannelProvider = provider
