import asyncio
import locale
import random
from dataclasses import dataclass
from typing import Any

from frozendict import frozendict

from .airStrikeCheerAction import AirStrikeCheerAction
from .airStrikeCheerActionHelperInterface import AirStrikeCheerActionHelperInterface
from ..absCheerAction import AbsCheerAction
from ..timeout.timeoutCheerActionMapper import TimeoutCheerActionMapper
from ...misc import utils as utils
from ...misc.backgroundTaskHelperInterface import BackgroundTaskHelperInterface
from ...recentGrenadeAttacks.helper.recentGrenadeAttacksHelperInterface import RecentGrenadeAttacksHelperInterface
from ...soundPlayerManager.provider.soundPlayerManagerProviderInterface import SoundPlayerManagerProviderInterface
from ...soundPlayerManager.soundAlert import SoundAlert
from ...timber.timberInterface import TimberInterface
from ...timeout.settings.timeoutActionSettingsInterface import TimeoutActionSettingsInterface
from ...timeout.timeoutActionData import TimeoutActionData
from ...timeout.timeoutActionHelperInterface import TimeoutActionHelperInterface
from ...timeout.timeoutActionType import TimeoutActionType
from ...trollmoji.trollmojiHelperInterface import TrollmojiHelperInterface
from ...twitch.activeChatters.activeChatter import ActiveChatter
from ...twitch.activeChatters.activeChattersRepositoryInterface import ActiveChattersRepositoryInterface
from ...twitch.configuration.twitchChannelProvider import TwitchChannelProvider
from ...twitch.timeout.timeoutImmuneUserIdsRepositoryInterface import TimeoutImmuneUserIdsRepositoryInterface
from ...twitch.twitchMessageStringUtilsInterface import TwitchMessageStringUtilsInterface
from ...twitch.twitchUtilsInterface import TwitchUtilsInterface
from ...users.userInterface import UserInterface


class AirStrikeCheerActionHelper(AirStrikeCheerActionHelperInterface):

    @dataclass(frozen = True)
    class AirStrikeTarget:
        userId: str
        userName: str

        def __eq__(self, value: Any) -> bool:
            if isinstance(value, AirStrikeCheerActionHelper.AirStrikeTarget):
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
        timeoutActionSettings: TimeoutActionSettingsInterface,
        timeoutCheerActionMapper: TimeoutCheerActionMapper,
        timeoutImmuneUserIdsRepository: TimeoutImmuneUserIdsRepositoryInterface,
        trollmojiHelper: TrollmojiHelperInterface,
        twitchMessageStringUtils: TwitchMessageStringUtilsInterface,
        twitchUtils: TwitchUtilsInterface,
        grenadeAlertSleepTimeSeconds: float = 0.60,
        launchAirStrikeAlertSleepTimeSeconds: float = 2.00,
        airStrikeAlertSleepTimeSeconds: float = 0.50
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
        elif not isinstance(timeoutActionSettings, TimeoutActionSettingsInterface):
            raise TypeError(f'timeoutActionSettings argument is malformed: \"{timeoutActionSettings}\"')
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
        elif not utils.isValidNum(launchAirStrikeAlertSleepTimeSeconds):
            raise TypeError(f'launchAirStrikeAlertSleepTimeSeconds argument is malformed: \"{launchAirStrikeAlertSleepTimeSeconds}\"')
        elif launchAirStrikeAlertSleepTimeSeconds < 0.125 or launchAirStrikeAlertSleepTimeSeconds > 8:
            raise ValueError(f'launchAirStrikeAlertSleepTimeSeconds argument is out of bounds: {launchAirStrikeAlertSleepTimeSeconds}')
        elif not utils.isValidNum(airStrikeAlertSleepTimeSeconds):
            raise TypeError(f'airStrikeAlertSleepTimeSeconds argument is malformed: \"{airStrikeAlertSleepTimeSeconds}\"')
        elif airStrikeAlertSleepTimeSeconds < 0.125 or airStrikeAlertSleepTimeSeconds > 8:
            raise ValueError(f'airStrikeAlertSleepTimeSeconds argument is out of bounds: {airStrikeAlertSleepTimeSeconds}')

        self.__activeChattersRepository: ActiveChattersRepositoryInterface = activeChattersRepository
        self.__backgroundTaskHelper: BackgroundTaskHelperInterface = backgroundTaskHelper
        self.__recentGrenadeAttacksHelper: RecentGrenadeAttacksHelperInterface = recentGrenadeAttacksHelper
        self.__soundPlayerManagerProvider: SoundPlayerManagerProviderInterface = soundPlayerManagerProvider
        self.__timber: TimberInterface = timber
        self.__timeoutActionHelper: TimeoutActionHelperInterface = timeoutActionHelper
        self.__timeoutActionSettings: TimeoutActionSettingsInterface = timeoutActionSettings
        self.__timeoutCheerActionMapper: TimeoutCheerActionMapper = timeoutCheerActionMapper
        self.__timeoutImmuneUserIdsRepository: TimeoutImmuneUserIdsRepositoryInterface = timeoutImmuneUserIdsRepository
        self.__trollmojiHelper: TrollmojiHelperInterface = trollmojiHelper
        self.__twitchUtils: TwitchUtilsInterface = twitchUtils
        self.__grenadeAlertSleepTimeSeconds: float = grenadeAlertSleepTimeSeconds
        self.__launchAirStrikeAlertSleepTimeSeconds: float = launchAirStrikeAlertSleepTimeSeconds
        self.__airStrikeAlertSleepTimeSeconds: float = airStrikeAlertSleepTimeSeconds

        self.__twitchChannelProvider: TwitchChannelProvider | None = None

    async def __alertViaTwitchChat(
        self,
        airStrikeTargets: frozenset[AirStrikeTarget],
        durationSeconds: int,
        cheerUserId: str,
        cheerUserName: str,
        twitchChannelId: str,
        twitchChatMessageId: str | None,
        user: UserInterface
    ):
        if len(airStrikeTargets) == 0:
            return

        twitchChannelProvider = self.__twitchChannelProvider

        if twitchChannelProvider is None:
            return

        userNames: list[str] = list()

        for airStrikeTarget in airStrikeTargets:
            userNames.append(f'@{airStrikeTarget.userName}')

        durationSecondsString = locale.format_string("%d", durationSeconds, grouping = True)
        peopleCountString = locale.format_string("%d", len(airStrikeTargets), grouping = True)

        peoplePluralityString: str
        if len(airStrikeTargets) == 1:
            peoplePluralityString = f'{peopleCountString} chatter was hit'
        else:
            peoplePluralityString = f'{peopleCountString} chatters hit'

        userNames.sort(key = lambda userName: userName.casefold())
        userNamesString = ', '.join(userNames)

        explodedEmote = await self.__trollmojiHelper.getExplodedEmoteOrBackup()
        bombEmote = await self.__trollmojiHelper.getBombEmoteOrBackup()
        twitchChannel = await twitchChannelProvider.getTwitchChannel(user.handle)
        message = f'{explodedEmote} BOOM! {peoplePluralityString} by @{cheerUserName} with a {durationSecondsString}s timeout! {userNamesString} {bombEmote}'

        await self.__twitchUtils.safeSend(
            messageable = twitchChannel,
            message = message,
            replyMessageId = twitchChatMessageId
        )

    async def __chooseRandomGrenadeSoundAlert(self) -> SoundAlert:
        soundAlerts: list[SoundAlert] = [
            SoundAlert.GRENADE_1,
            SoundAlert.GRENADE_2,
            SoundAlert.GRENADE_3,
        ]

        return random.choice(soundAlerts)

    async def __determineAirStrikeTargets(
        self,
        airStrikeAction: AirStrikeCheerAction,
        cheerUserId: str,
        cheerUserName: str,
        twitchChannelId: str,
    ) -> frozenset[AirStrikeTarget]:
        airStrikeTargets: set[AirStrikeCheerActionHelper.AirStrikeTarget] = set()

        additionalReverseProbability = await self.__timeoutActionSettings.getGrenadeAdditionalReverseProbability()
        randomReverseNumber = random.random()

        if randomReverseNumber <= additionalReverseProbability:
            airStrikeTargets.add(AirStrikeCheerActionHelper.AirStrikeTarget(
                userId = cheerUserId,
                userName = cheerUserName
            ))

        activeChatters = await self.__activeChattersRepository.get(
            twitchChannelId = twitchChannelId
        )

        vulnerableChatters: dict[str, ActiveChatter] = dict(activeChatters)
        vulnerableChatters.pop(twitchChannelId, None)

        allImmuneUserIds = await self.__timeoutImmuneUserIdsRepository.getAllUserIds()

        for immuneUserId in allImmuneUserIds:
            vulnerableChatters.pop(immuneUserId, None)

        airStrikeTargetCount = random.randint(airStrikeAction.minTimeoutChatters, airStrikeAction.maxTimeoutChatters)
        vulnerableChattersList: list[ActiveChatter] = list(vulnerableChatters.values())

        while len(airStrikeTargets) < airStrikeTargetCount and len(vulnerableChattersList) >= 1:
            randomChatterIndex = random.randint(0, len(vulnerableChattersList) - 1)
            randomChatter = vulnerableChattersList[randomChatterIndex]
            del vulnerableChattersList[randomChatterIndex]

            airStrikeTargets.add(AirStrikeCheerActionHelper.AirStrikeTarget(
                userId = randomChatter.chatterUserId,
                userName = randomChatter.chatterUserName
            ))

        frozenAirStrikeTargets: frozenset[AirStrikeCheerActionHelper.AirStrikeTarget] = frozenset(airStrikeTargets)

        for airStrikeTarget in frozenAirStrikeTargets:
            await self.__activeChattersRepository.remove(
                chatterUserId = airStrikeTarget.userId,
                twitchChannelId = twitchChannelId
            )

        self.__timber.log('AirStrikeCheerActionHelper', f'Selected target(s) ({airStrikeAction=}) ({additionalReverseProbability=}) ({randomReverseNumber=}) ({airStrikeTargetCount=}) ({frozenAirStrikeTargets=})')

        return frozenAirStrikeTargets

    async def handleAirStrikeCheerAction(
        self,
        actions: frozendict[int, AbsCheerAction],
        bits: int,
        cheerUserId: str,
        cheerUserName: str,
        message: str,
        moderatorTwitchAccessToken: str,
        moderatorUserId: str,
        twitchChannelId: str,
        twitchChatMessageId: str | None,
        userTwitchAccessToken: str,
        user: UserInterface,
    ) -> bool:
        if not isinstance(actions, frozendict):
            raise TypeError(f'actions argument is malformed: \"{actions}\"')
        elif not utils.isValidInt(bits):
            raise TypeError(f'bits argument is malformed: \"{bits}\"')
        elif bits < 1 or bits > utils.getIntMaxSafeSize():
            raise ValueError(f'bits argument is out of bounds: {bits}')
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
        elif not utils.isValidStr(twitchChannelId):
            raise TypeError(f'twitchChannelId argument is malformed: \"{twitchChannelId}\"')
        elif twitchChatMessageId is not None and not isinstance(twitchChatMessageId, str):
            raise TypeError(f'twitchChatMessageId argument is malformed: \"{twitchChatMessageId}\"')
        elif not utils.isValidStr(userTwitchAccessToken):
            raise TypeError(f'userTwitchAccessToken argument is malformed: \"{userTwitchAccessToken}\"')
        elif not isinstance(user, UserInterface):
            raise TypeError(f'user argument is malformed: \"{user}\"')

        action = actions.get(bits, None)

        if not isinstance(action, AirStrikeCheerAction) or not action.isEnabled:
            return False
        elif not await self.__recentGrenadeAttacksHelper.canThrowGrenade(
            attackerUserId = cheerUserId,
            twitchChannel = user.handle,
            twitchChannelId = twitchChannelId
        ):
            self.__timber.log('AirStrikeCheerActionHelper', f'No grenades available for this user ({cheerUserId=}) ({cheerUserName=}) ({user=}) ({action=})')
            return False

        airStrikeTargets = await self.__determineAirStrikeTargets(
            airStrikeAction = action,
            cheerUserId = cheerUserId,
            cheerUserName = cheerUserName,
            twitchChannelId = twitchChannelId,
        )

        if len(airStrikeTargets) == 0:
            self.__timber.log('AirStrikeCheerActionHelper', f'Unable to find any vulnerable targets ({cheerUserId=}) ({cheerUserName=}) ({user=}) ({action=}) ({airStrikeTargets=})')
            return False

        remainingGrenades = await self.__noteGrenadeThrow(
            airStrikeTargets = airStrikeTargets,
            cheerUserId = cheerUserId,
            twitchChannelId = twitchChannelId,
            user = user
        )

        streamStatusRequirement = await self.__timeoutCheerActionMapper.toTimeoutActionDataStreamStatusRequirement(
            streamStatusRequirement = action.streamStatusRequirement
        )

        self.__backgroundTaskHelper.createTask(self.__playSoundAlerts(
            airStrikeTargets = airStrikeTargets,
            user = user
        ))

        durationSeconds = random.randint(action.minDurationSeconds, action.maxDurationSeconds)

        self.__backgroundTaskHelper.createTask(self.__alertViaTwitchChat(
            airStrikeTargets= airStrikeTargets,
            durationSeconds = durationSeconds,
            cheerUserId = cheerUserId,
            cheerUserName = cheerUserName,
            twitchChannelId = twitchChannelId,
            twitchChatMessageId = twitchChatMessageId,
            user = user
        ))

        for airStrikeTarget in airStrikeTargets:
            self.__timeoutActionHelper.submitTimeout(TimeoutActionData(
                isRandomChanceEnabled = False,
                bits = bits,
                durationSeconds = durationSeconds,
                remainingGrenades = remainingGrenades,
                chatMessage = message,
                instigatorUserId = cheerUserId,
                instigatorUserName = cheerUserName,
                moderatorTwitchAccessToken = moderatorTwitchAccessToken,
                moderatorUserId = moderatorUserId,
                pointRedemptionEventId = None,
                pointRedemptionMessage = None,
                pointRedemptionRewardId = None,
                timeoutTargetUserId = airStrikeTarget.userId,
                timeoutTargetUserName = airStrikeTarget.userName,
                twitchChannelId = twitchChannelId,
                twitchChatMessageId = twitchChatMessageId,
                userTwitchAccessToken = userTwitchAccessToken,
                actionType = TimeoutActionType.AIR_STRIKE,
                streamStatusRequirement = streamStatusRequirement,
                user = user
            ))

        return True

    async def __noteGrenadeThrow(
        self,
        airStrikeTargets: frozenset[AirStrikeTarget],
        cheerUserId: str,
        twitchChannelId: str,
        user: UserInterface
    ) -> int | None:
        randomTarget = random.choice(list(airStrikeTargets))

        return await self.__recentGrenadeAttacksHelper.throwGrenade(
            attackedUserId = randomTarget.userId,
            attackerUserId = cheerUserId,
            twitchChannel = user.handle,
            twitchChannelId = twitchChannelId
        )

    async def __playSoundAlerts(
        self,
        airStrikeTargets: frozenset[AirStrikeTarget],
        user: UserInterface
    ):
        if not user.areSoundAlertsEnabled:
            return
        elif len(airStrikeTargets) == 0:
            return

        soundPlayerManager = self.__soundPlayerManagerProvider.constructNewInstance()
        self.__backgroundTaskHelper.createTask(soundPlayerManager.playSoundAlert(SoundAlert.LAUNCH_AIR_STRIKE))
        await asyncio.sleep(self.__launchAirStrikeAlertSleepTimeSeconds)

        soundPlayerManager = self.__soundPlayerManagerProvider.constructNewInstance()
        self.__backgroundTaskHelper.createTask(soundPlayerManager.playSoundAlert(SoundAlert.AIR_STRIKE))
        await asyncio.sleep(self.__airStrikeAlertSleepTimeSeconds)

        index = 0
        numberOfSounds = len(airStrikeTargets)

        while index < numberOfSounds:
            soundAlert = await self.__chooseRandomGrenadeSoundAlert()
            soundPlayerManager = self.__soundPlayerManagerProvider.constructNewInstance()
            self.__backgroundTaskHelper.createTask(soundPlayerManager.playSoundAlert(soundAlert))
            index += 1

            await asyncio.sleep(self.__grenadeAlertSleepTimeSeconds)

        soundPlayerManager = self.__soundPlayerManagerProvider.constructNewInstance()
        self.__backgroundTaskHelper.createTask(soundPlayerManager.playSoundAlert(SoundAlert.SPLAT))

    def setTwitchChannelProvider(self, provider: TwitchChannelProvider | None):
        if provider is not None and not isinstance(provider, TwitchChannelProvider):
            raise TypeError(f'provider argument is malformed: \"{provider}\"')

        self.__twitchChannelProvider = provider
