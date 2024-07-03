from collections import defaultdict
from datetime import datetime, timedelta

from .superTriviaCooldownHelperInterface import SuperTriviaCooldownHelperInterface
from .triviaSettingsRepositoryInterface import TriviaSettingsRepositoryInterface
from ..location.timeZoneRepositoryInterface import TimeZoneRepositoryInterface
from ..misc import utils as utils


class SuperTriviaCooldownHelper(SuperTriviaCooldownHelperInterface):

    def __init__(
        self,
        timeZoneRepository: TimeZoneRepositoryInterface,
        triviaSettingsRepository: TriviaSettingsRepositoryInterface
    ):
        if not isinstance(timeZoneRepository, TimeZoneRepositoryInterface):
            raise TypeError(f'timeZoneRepository argument is malformed: \"{timeZoneRepository}\"')
        elif not isinstance(triviaSettingsRepository, TriviaSettingsRepositoryInterface):
            raise TypeError(f'triviaSettingsRepository argument is malformed: \"{triviaSettingsRepository}\"')

        self.__timeZoneRepository: TimeZoneRepositoryInterface = timeZoneRepository
        self.__triviaSettingsRepository: TriviaSettingsRepositoryInterface = triviaSettingsRepository

        self.__values: dict[str, datetime] = defaultdict(
            lambda: datetime.now(timeZoneRepository.getDefault()) - timedelta(weeks = 1)
        )

    async def getTwitchChannelIdsInCooldown(self) -> set[str]:
        twitchChannelIds: set[str] = set()
        now = datetime.now(self.__timeZoneRepository.getDefault())

        for twitchChannelId, cooldown in self.__values.items():
            if cooldown > now:
                twitchChannelIds.add(twitchChannelId)

        return twitchChannelIds

    def isTwitchChannelInCooldown(self, twitchChannelId: str) -> bool:
        if not utils.isValidStr(twitchChannelId):
            raise TypeError(f'twitchChannelId argument is malformed: \"{twitchChannelId}\"')

        now = datetime.now(self.__timeZoneRepository.getDefault())
        return now <= self.__values[twitchChannelId]

    async def update(self, twitchChannelId: str):
        if not utils.isValidStr(twitchChannelId):
            raise TypeError(f'twitchChannelId argument is malformed: \"{twitchChannelId}\"')

        cooldownSeconds = await self.__triviaSettingsRepository.getSuperTriviaCooldownSeconds()
        cooldown = timedelta(seconds = cooldownSeconds)
        now = datetime.now(self.__timeZoneRepository.getDefault())

        self.__values[twitchChannelId] = now + cooldown
