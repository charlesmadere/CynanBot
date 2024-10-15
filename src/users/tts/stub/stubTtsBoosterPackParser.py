from typing import Any

from frozendict import frozendict

from ..ttsBoosterPack import TtsBoosterPack
from ..ttsBoosterPackParserInterface import TtsBoosterPackParserInterface


class StubTtsBoosterPackParser(TtsBoosterPackParserInterface):

    def parseBoosterPack(self, jsonContents: dict[str, Any]) -> TtsBoosterPack:
        # this method is intentionally empty
        raise RuntimeError()

    def parseBoosterPacks(
        self,
        jsonContents: list[dict[str, Any]] | Any | None
    ) -> frozendict[int, TtsBoosterPack] | None:
        return None
