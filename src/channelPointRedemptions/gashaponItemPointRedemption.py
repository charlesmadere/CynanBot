from typing import Final

from .absChannelPointsRedemption2 import AbsChannelPointRedemption2
from .pointsRedemptionResult import PointsRedemptionResult
from ..chatterInventory.models.chatterItemType import ChatterItemType
from ..chatterInventory.settings.chatterInventorySettingsInterface import ChatterInventorySettingsInterface
from ..soundPlayerManager.provider.soundPlayerManagerProviderInterface import SoundPlayerManagerProviderInterface
from ..twitch.chatMessenger.twitchChatMessengerInterface import TwitchChatMessengerInterface
from ..twitch.localModels.twitchChannelPointsRedemption import TwitchChannelPointsRedemption
from ..users.userInterface import UserInterface


class GashaponItemPointRedemption(AbsChannelPointRedemption2):

    def __init__(
        self,
        chatterInventorySettings: ChatterInventorySettingsInterface,
        soundPlayerManagerProvider: SoundPlayerManagerProviderInterface | None,
        twitchChatMessenger: TwitchChatMessengerInterface,
    ):
        if not isinstance(chatterInventorySettings, ChatterInventorySettingsInterface):
            raise TypeError(f'chatterInventorySettings argument is malformed: \"{chatterInventorySettings}\"')
        if soundPlayerManagerProvider is not None and not isinstance(soundPlayerManagerProvider, SoundPlayerManagerProviderInterface):
            raise TypeError(f'soundPlayerManagerProvider argument is malformed: \"{soundPlayerManagerProvider}\"')
        elif not isinstance(twitchChatMessenger, TwitchChatMessengerInterface):
            raise TypeError(f'twitchChatMessenger argument is malformed: \"{twitchChatMessenger}\"')

        self.__chatterInventorySettings: Final[ChatterInventorySettingsInterface] = chatterInventorySettings
        self.__soundPlayerManagerProvider: Final[SoundPlayerManagerProviderInterface | None] = soundPlayerManagerProvider
        self.__twitchChatMessenger: Final[TwitchChatMessengerInterface] = twitchChatMessenger

    async def handlePointsRedemption(
        self,
        pointsRedemption: TwitchChannelPointsRedemption,
    ) -> PointsRedemptionResult:
        if not pointsRedemption.twitchUser.isChatterInventoryEnabled:
            return PointsRedemptionResult.IGNORED
        elif ChatterItemType.GASHAPON not in await self.__chatterInventorySettings.getEnabledItemTypes():
            return PointsRedemptionResult.IGNORED

        # TODO
        return PointsRedemptionResult.IGNORED

    @property
    def pointsRedemptionName(self) -> str:
        return 'GashaponItemPointRedemption'

    def relevantRewardIds(
        self,
        twitchUser: UserInterface,
    ) -> frozenset[str]:
        # TODO
        return frozenset()
