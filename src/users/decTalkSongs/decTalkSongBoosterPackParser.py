from typing import Any

from frozendict import frozendict

from .decTalkSongBoosterPack import DecTalkSongBoosterPack
from .decTalkSongBoosterPackParserInterface import DecTalkSongBoosterPackParserInterface
from ...misc import utils as utils


class DecTalkSongBoosterPackParser(DecTalkSongBoosterPackParserInterface):

    def parseBoosterPack(
        self,
        jsonContents: dict[str, Any]
    ) -> DecTalkSongBoosterPack:
        if not isinstance(jsonContents, dict):
            raise TypeError(f'jsonContents argument is malformed: \"{jsonContents}\"')

        song = utils.getStrFromDict(jsonContents, 'song')
        rewardId = utils.getStrFromDict(jsonContents, 'rewardId')

        if not utils.isValidStr(song):
            raise ValueError(f'song argument is malformed: \"{song}\"')
        elif not utils.isValidStr(rewardId):
            raise ValueError(f'rewardId argument is malformed: \"{rewardId}\"')

        return DecTalkSongBoosterPack(
            rewardId = rewardId,
            song = song
        )

    def parseBoosterPacks(
        self,
        jsonContents: list[dict[str, Any]] | Any | None
    ) -> frozendict[str, DecTalkSongBoosterPack] | None:
        if not isinstance(jsonContents, list) or len(jsonContents) == 0:
            return None

        boosterPacks: dict[str, DecTalkSongBoosterPack] = dict()
        for boosterPackJson in jsonContents:
            boosterPack = self.parseBoosterPack(boosterPackJson)
            boosterPacks[boosterPack.rewardId] = boosterPack

        return frozendict(boosterPacks)
