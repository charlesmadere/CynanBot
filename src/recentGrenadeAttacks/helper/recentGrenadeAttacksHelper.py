from datetime import datetime, timedelta
from typing import Final

from .recentGrenadeAttacksHelperInterface import RecentGrenadeAttacksHelperInterface
from ..repository.recentGrenadeAttacksRepositoryInterface import RecentGrenadeAttacksRepositoryInterface
from ..settings.recentGrenadeAttacksSettingsRepositoryInterface import RecentGrenadeAttacksSettingsRepositoryInterface
from ...location.timeZoneRepositoryInterface import TimeZoneRepositoryInterface
from ...misc import utils as utils
from ...users.usersRepositoryInterface import UsersRepositoryInterface


class RecentGrenadeAttacksHelper(RecentGrenadeAttacksHelperInterface):

    def __init__(
        self,
        recentGrenadeAttacksRepository: RecentGrenadeAttacksRepositoryInterface,
        recentGrenadeAttacksSettingsRepository: RecentGrenadeAttacksSettingsRepositoryInterface,
        timeZoneRepository: TimeZoneRepositoryInterface,
        usersRepository: UsersRepositoryInterface
    ):
        if not isinstance(recentGrenadeAttacksRepository, RecentGrenadeAttacksRepositoryInterface):
            raise TypeError(f'recentGrenadeAttacksRepository argument is malformed: \"{recentGrenadeAttacksRepository}\"')
        elif not isinstance(recentGrenadeAttacksSettingsRepository, RecentGrenadeAttacksSettingsRepositoryInterface):
            raise TypeError(f'recentGrenadeAttacksSettingsRepository argument is malformed: \"{recentGrenadeAttacksSettingsRepository}\"')
        elif not isinstance(timeZoneRepository, TimeZoneRepositoryInterface):
            raise TypeError(f'timeZoneRepository argument is malformed: \"{timeZoneRepository}\"')
        elif not isinstance(usersRepository, UsersRepositoryInterface):
            raise TypeError(f'usersRepository argument is malformed: \"{usersRepository}\"')

        self.__recentGrenadeAttacksRepository: Final[RecentGrenadeAttacksRepositoryInterface] = recentGrenadeAttacksRepository
        self.__recentGrenadeAttacksSettingsRepository: Final[RecentGrenadeAttacksSettingsRepositoryInterface] = recentGrenadeAttacksSettingsRepository
        self.__timeZoneRepository: Final[TimeZoneRepositoryInterface] = timeZoneRepository
        self.__usersRepository: Final[UsersRepositoryInterface] = usersRepository

    async def canThrowGrenade(
        self,
        attackerUserId: str,
        twitchChannel: str,
        twitchChannelId: str
    ) -> bool:
        if not utils.isValidStr(attackerUserId):
            raise TypeError(f'attackerUserId argument is malformed: \"{attackerUserId}\"')
        elif not utils.isValidStr(twitchChannel):
            raise TypeError(f'twitchChannel argument is malformed: \"{twitchChannel}\"')
        elif not utils.isValidStr(twitchChannelId):
            raise TypeError(f'twitchChannelId argument is malformed: \"{twitchChannelId}\"')

        availableGrenades = await self.fetchAvailableGrenades(
            attackerUserId = attackerUserId,
            twitchChannel = twitchChannel,
            twitchChannelId = twitchChannelId
        )

        return availableGrenades is None or availableGrenades > 0

    async def fetchAvailableGrenades(
        self,
        attackerUserId: str,
        twitchChannel: str,
        twitchChannelId: str
    ) -> int | None:
        if not utils.isValidStr(attackerUserId):
            raise TypeError(f'attackerUserId argument is malformed: \"{attackerUserId}\"')
        elif not utils.isValidStr(twitchChannel):
            raise TypeError(f'twitchChannel argument is malformed: \"{twitchChannel}\"')
        elif not utils.isValidStr(twitchChannelId):
            raise TypeError(f'twitchChannelId argument is malformed: \"{twitchChannelId}\"')

        user = await self.__usersRepository.getUserAsync(twitchChannel)
        maximumGrenadesWithinCooldown = user.maximumGrenadesWithinCooldown

        if maximumGrenadesWithinCooldown is None:
            return None

        recentGrenadeAttackData = await self.__recentGrenadeAttacksRepository.get(
            attackerUserId = attackerUserId,
            twitchChannelId = twitchChannelId
        )

        now = datetime.now(self.__timeZoneRepository.getDefault())
        grenadeCooldownSeconds = await self.__recentGrenadeAttacksSettingsRepository.getGrenadeCooldownSeconds()
        grenadeCooldownTimeDelta = timedelta(seconds = grenadeCooldownSeconds)
        grenadesInCooldown = 0

        for grenadeAttack in recentGrenadeAttackData.grenadeAttacks:
            if now - grenadeAttack.attackedDateTime <= grenadeCooldownTimeDelta:
                grenadesInCooldown += 1

        return max(maximumGrenadesWithinCooldown - grenadesInCooldown, 0)

    async def throwGrenade(
        self,
        attackedUserId: str,
        attackerUserId: str,
        twitchChannel: str,
        twitchChannelId: str
    ) -> int | None:
        if not utils.isValidStr(attackedUserId):
            raise TypeError(f'attackedUserId argument is malformed: \"{attackedUserId}\"')
        elif not utils.isValidStr(attackerUserId):
            raise TypeError(f'attackerUserId argument is malformed: \"{attackerUserId}\"')
        elif not utils.isValidStr(twitchChannel):
            raise TypeError(f'twitchChannel argument is malformed: \"{twitchChannel}\"')
        elif not utils.isValidStr(twitchChannelId):
            raise TypeError(f'twitchChannelId argument is malformed: \"{twitchChannelId}\"')

        user = await self.__usersRepository.getUserAsync(twitchChannel)

        await self.__recentGrenadeAttacksRepository.add(
            maximumGrenades = user.maximumGrenadesWithinCooldown,
            attackedUserId = attackedUserId,
            attackerUserId = attackerUserId,
            twitchChannelId = twitchChannelId
        )

        return await self.fetchAvailableGrenades(
            attackerUserId = attackerUserId,
            twitchChannel = twitchChannel,
            twitchChannelId = twitchChannelId
        )
