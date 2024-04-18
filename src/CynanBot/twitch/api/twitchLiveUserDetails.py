import locale

import CynanBot.misc.utils as utils
from CynanBot.twitch.api.twitchStreamType import TwitchStreamType


class TwitchLiveUserDetails():

    def __init__(
        self,
        isMature: bool,
        viewerCount: int,
        streamId: str,
        userId: str,
        userLogin: str,
        userName: str,
        gameId: str | None = None,
        gameName: str | None = None,
        language: str | None = None,
        thumbnailUrl: str |  None = None,
        title: str | None = None,
        streamType: TwitchStreamType = TwitchStreamType.UNKNOWN
    ):
        if not utils.isValidBool(isMature):
            raise TypeError(f'isMature argument is malformed: \"{isMature}\"')
        elif not utils.isValidInt(viewerCount):
            raise TypeError(f'viewerCount argument is malformed: \"{viewerCount}\"')
        elif viewerCount < 0 or viewerCount > utils.getIntMaxSafeSize():
            raise ValueError(f'viewerCount argument is out of bounds: {viewerCount}')
        elif not utils.isValidStr(streamId):
            raise TypeError(f'streamId argument is malformed: \"{streamId}\"')
        elif not utils.isValidStr(userId):
            raise TypeError(f'userId argument is malformed: \"{userId}\"')
        elif not utils.isValidStr(userLogin):
            raise TypeError(f'userLogin argument is malformed: \"{userLogin}\"')
        elif not utils.isValidStr(userName):
            raise TypeError(f'userName argument is malformed: \"{userName}\"')
        elif gameId is not None and not isinstance(gameId, str):
            raise TypeError(f'gameId argument is malformed: \"{gameId}\"')
        elif gameName is not None and not isinstance(gameName, str):
            raise TypeError(f'gameName argument is malformed: \"{gameName}\"')
        elif language is not None and not isinstance(language, str):
            raise TypeError(f'language argument is malformed: \"{language}\"')
        elif thumbnailUrl is not None and not isinstance(thumbnailUrl, str):
            raise TypeError(f'thumbnailUrl argument is malformed: \"{thumbnailUrl}\"')
        elif title is not None and not isinstance(title, str):
            raise TypeError(f'title argument is malformed: \"{title}\"')
        elif not isinstance(streamType, TwitchStreamType):
            raise TypeError(f'streamType argument is malformed: \"{streamType}\"')

        self.__isMature: bool = isMature
        self.__viewerCount: int = viewerCount
        self.__streamId: str = streamId
        self.__userId: str = userId
        self.__userLogin: str = userLogin
        self.__userName: str = userName
        self.__gameId: str | None = gameId
        self.__gameName: str | None = gameName
        self.__language: str | None = language
        self.__thumbnailUrl: str | None = thumbnailUrl
        self.__title: str | None = title
        self.__streamType: TwitchStreamType = streamType

    def getGameId(self) -> str | None:
        return self.__gameId

    def getGameName(self) -> str | None:
        return self.__gameName

    def getLanguage(self) -> str | None:
        return self.__language

    def getStreamId(self) -> str:
        return self.__streamId

    def getStreamType(self) -> TwitchStreamType:
        return self.__streamType

    def getThumbnailUrl(self) -> str | None:
        return self.__thumbnailUrl

    def getTitle(self) -> str | None:
        return self.__title

    def getUserId(self) -> str:
        return self.__userId

    def getUserLogin(self) -> str:
        return self.__userLogin

    def getUserName(self) -> str:
        return self.__userName

    def getViewerCount(self) -> int:
        return self.__viewerCount

    def getViewerCountStr(self) -> str:
        return locale.format_string("%d", self.__viewerCount, grouping = True)

    def isMature(self) -> bool:
        return self.__isMature
