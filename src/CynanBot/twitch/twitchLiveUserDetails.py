import locale
from typing import Optional

import CynanBot.misc.utils as utils
from CynanBot.twitch.twitchStreamType import TwitchStreamType


class TwitchLiveUserDetails():

    def __init__(
        self,
        isMature: bool,
        viewerCount: int,
        streamId: str,
        userId: str,
        userLogin: str,
        userName: str,
        gameId: Optional[str] = None,
        gameName: Optional[str] = None,
        language: Optional[str] = None,
        thumbnailUrl: Optional[str] = None,
        title: Optional[str] = None,
        streamType: TwitchStreamType = TwitchStreamType.UNKNOWN
    ):
        if not utils.isValidBool(isMature):
            raise ValueError(f'isMature argument is malformed: \"{isMature}\"')
        elif not utils.isValidInt(viewerCount):
            raise ValueError(f'viewerCount argument is malformed: \"{viewerCount}\"')
        elif viewerCount < 0 or viewerCount > utils.getIntMaxSafeSize():
            raise ValueError(f'viewerCount argument is out of bounds: {viewerCount}')
        elif not utils.isValidStr(streamId):
            raise ValueError(f'streamId argument is malformed: \"{streamId}\"')
        elif not utils.isValidStr(userId):
            raise ValueError(f'userId argument is malformed: \"{userId}\"')
        elif not utils.isValidStr(userLogin):
            raise ValueError(f'userLogin argument is malformed: \"{userLogin}\"')
        elif not utils.isValidStr(userName):
            raise ValueError(f'userName argument is malformed: \"{userName}\"')
        elif gameId is not None and not isinstance(gameId, str):
            raise ValueError(f'gameId argument is malformed: \"{gameId}\"')
        elif gameName is not None and not isinstance(gameName, str):
            raise ValueError(f'gameName argument is malformed: \"{gameName}\"')
        elif language is not None and not isinstance(language, str):
            raise ValueError(f'language argument is malformed: \"{language}\"')
        elif thumbnailUrl is not None and not isinstance(thumbnailUrl, str):
            raise ValueError(f'thumbnailUrl argument is malformed: \"{thumbnailUrl}\"')
        elif title is not None and not isinstance(title, str):
            raise ValueError(f'title argument is malformed: \"{title}\"')
        elif not isinstance(streamType, TwitchStreamType):
            raise ValueError(f'streamType argument is malformed: \"{streamType}\"')

        self.__isMature: bool = isMature
        self.__viewerCount: int = viewerCount
        self.__streamId: str = streamId
        self.__userId: str = userId
        self.__userLogin: str = userLogin
        self.__userName: str = userName
        self.__gameId: Optional[str] = gameId
        self.__gameName: Optional[str] = gameName
        self.__language: Optional[str] = language
        self.__thumbnailUrl: Optional[str] = thumbnailUrl
        self.__title: Optional[str] = title
        self.__streamType: TwitchStreamType = streamType

    def getGameId(self) -> Optional[str]:
        return self.__gameId

    def getGameName(self) -> Optional[str]:
        return self.__gameName

    def getLanguage(self) -> Optional[str]:
        return self.__language

    def getStreamId(self) -> str:
        return self.__streamId

    def getStreamType(self) -> TwitchStreamType:
        return self.__streamType

    def getThumbnailUrl(self) -> Optional[str]:
        return self.__thumbnailUrl

    def getTitle(self) -> Optional[str]:
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

    def hasGameId(self) -> bool:
        return utils.isValidStr(self.__gameId)

    def hasGameName(self) -> bool:
        return utils.isValidStr(self.__gameName)

    def hasLanguage(self) -> bool:
        return utils.isValidStr(self.__language)

    def hasThumbnailUrl(self) -> bool:
        return utils.isValidUrl(self.__thumbnailUrl)

    def hasTitle(self) -> bool:
        return utils.isValidStr(self.__title)

    def isMature(self) -> bool:
        return self.__isMature
