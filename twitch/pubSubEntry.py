import CynanBotCommon.utils as utils
from twitchio.ext.pubsub.topics import Topic


class PubSubEntry():

    def __init__(self, userId: str, userName: str, topic: Topic):
        if not utils.isValidStr(userId):
            raise ValueError(f'userId argument is malformed: \"{userId}\"')
        elif not utils.isValidStr(userName):
            raise ValueError(f'userName argument is malformed: \"{userName}\"')
        elif topic is None:
            raise ValueError(f'topic argument is malformed: \"{topic}\"')

        self.__userId: str = userId
        self.__userName: str = userName
        self.__topic: Topic = topic

    def getTopic(self) -> Topic:
        return self.__topic

    def getUserId(self) -> str:
        return self.__userId

    def getUserName(self) -> str:
        return self.__userName
