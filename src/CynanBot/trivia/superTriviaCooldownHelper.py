from collections import defaultdict
from datetime import datetime, timedelta, timezone
from typing import Dict, Set

import misc.utils as utils
from trivia.superTriviaCooldownHelperInterface import \
    SuperTriviaCooldownHelperInterface
from trivia.triviaSettingsRepositoryInterface import \
    TriviaSettingsRepositoryInterface


class SuperTriviaCooldownHelper(SuperTriviaCooldownHelperInterface):

    def __init__(
        self,
        triviaSettingsRepository: TriviaSettingsRepositoryInterface,
        timeZone: timezone = timezone.utc
    ):
        if not isinstance(triviaSettingsRepository, TriviaSettingsRepositoryInterface):
            raise ValueError(f'triviaSettingsRepository argument is malformed: \"{triviaSettingsRepository}\"')
        elif not isinstance(timeZone, timezone):
            raise ValueError(f'timeZone argument is malformed: \"{timeZone}\"')

        self.__triviaSettingsRepository: TriviaSettingsRepositoryInterface = triviaSettingsRepository
        self.__timeZone: timezone = timeZone

        self.__values: Dict[str, datetime] = defaultdict(lambda: datetime.now(timeZone) - timedelta(days = 1))

    async def getTwitchChannelsInCooldown(self) -> Set[str]:
        twitchChannels: Set[str] = set()
        now = datetime.now(self.__timeZone)

        for twitchChannel, cooldown in self.__values.items():
            if cooldown > now:
                twitchChannels.add(twitchChannel.lower())

        return twitchChannels

    def isTwitchChannelInCooldown(self, twitchChannel: str) -> bool:
        if not utils.isValidStr(twitchChannel):
            raise ValueError(f'twitchChannel argument is malformed: \"{twitchChannel}\"')

        now = datetime.now(self.__timeZone)
        return now <= self.__values[twitchChannel.lower()]

    async def update(self, twitchChannel: str):
        if not utils.isValidStr(twitchChannel):
            raise ValueError(f'twitchChannel argument is malformed: \"{twitchChannel}\"')

        cooldownSeconds = await self.__triviaSettingsRepository.getSuperTriviaCooldownSeconds()
        cooldown = timedelta(seconds = cooldownSeconds)
        now = datetime.now(self.__timeZone)

        self.__values[twitchChannel.lower()] = now + cooldown
