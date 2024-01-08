from typing import Any, Dict

import CynanBot.misc.utils as utils


class TwitchWebsocketPollChoice():

    def __init__(
        self,
        channelPointsVotes: int,
        votes: int,
        choiceId: str,
        title: str
    ):
        if not utils.isValidInt(channelPointsVotes):
            raise ValueError(f'channelPointsVotes argument is malformed: \"{channelPointsVotes}\"')
        elif channelPointsVotes < 0 or channelPointsVotes > utils.getIntMaxSafeSize():
            raise ValueError(f'channelPointsVotes argument is out of bounds: {channelPointsVotes}')
        elif not utils.isValidInt(votes):
            raise ValueError(f'votes argument is malformed: \"{votes}\"')
        elif votes < 0 or votes > utils.getIntMaxSafeSize():
            raise ValueError(f'votes argument is out of bounds: {votes}')
        elif not utils.isValidStr(choiceId):
            raise ValueError(f'choiceId argument is malformed: \"{choiceId}\"')
        elif not utils.isValidStr(title):
            raise ValueError(f'title argument is malformed: \"{title}\"')

        self.__channelPointsVotes: int = channelPointsVotes
        self.__votes: int = votes
        self.__choiceId: str = choiceId
        self.__title: str = title

    def getChannelPointsVotes(self) -> int:
        return self.__channelPointsVotes

    def getChoiceId(self) -> str:
        return self.__choiceId

    def getTitle(self) -> str:
        return self.__title

    def getVotes(self) -> int:
        return self.__votes

    def __repr__(self) -> str:
        dictionary = self.toDictionary()
        return str(dictionary)

    def toDictionary(self) -> Dict[str, Any]:
        return {
            'channelPointsVotes': self.__channelPointsVotes,
            'choiceId': self.__choiceId,
            'title': self.__title,
            'votes': self.__votes
        }
