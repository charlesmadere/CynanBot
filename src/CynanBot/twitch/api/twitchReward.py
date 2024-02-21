from typing import Any, Dict, Optional

import CynanBot.misc.utils as utils


class TwitchReward():

    def __init__(
        self,
        cost: int,
        prompt: Optional[str],
        rewardId: str,
        title: str
    ):
        if not utils.isValidInt(cost):
            raise TypeError(f'cost argument is malformed: \"{cost}\"')
        assert prompt is None or isinstance(prompt, str), f"malformed {prompt=}"
        if not utils.isValidStr(rewardId):
            raise TypeError(f'rewardId argument is malformed: \"{rewardId}\"')
        if not utils.isValidStr(title):
            raise TypeError(f'title argument is malformed: \"{title}\"')

        self.__cost: int = cost
        self.__prompt: Optional[str] = prompt
        self.__rewardId: str = rewardId
        self.__title: str = title

    def getCost(self) -> int:
        return self.__cost

    def getPrompt(self) -> Optional[str]:
        return self.__prompt

    def getRewardId(self) -> str:
        return self.__rewardId

    def getTitle(self) -> str:
        return self.__title

    def __repr__(self) -> str:
        dictionary = self.toDictionary()
        return str(dictionary)

    def toDictionary(self) -> Dict[str, Any]:
        return {
            'cost': self.__cost,
            'prompt': self.__prompt,
            'rewardId': self.__rewardId,
            'title': self.__title
        }
