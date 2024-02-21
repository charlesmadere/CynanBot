import locale
from typing import Optional

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
        gameId: Optional[str] = None,
        gameName: Optional[str] = None,
        language: Optional[str] = None,
        thumbnailUrl: Optional[str] = None,
        title: Optional[str] = None,
        streamType: TwitchStreamType = TwitchStreamType.UNKNOWN
    ):
        if not utils.isValidBool(isMature):
            raise ValueError(f'isMature argument is malformed: \"{isMature}\"')
        if not utils.isValidInt(viewerCount):
            raise ValueError(f'viewerCount argument is malformed: \"{viewerCount}\"')
        if viewerCount < 0 or viewerCount > utils.getIntMaxSafeSize():
            raise ValueError(f'viewerCount argument is out of bounds: {viewerCount}')
        if not utils.isValidStr(streamId):
            raise ValueError(f'streamId argument is malformed: \"{streamId}\"')
        if not utils.isValidStr(userId):
            raise ValueError(f'userId argument is malformed: \"{userId}\"')
        if not utils.isValidStr(userLogin):
            raise ValueError(f'userLogin argument is malformed: \"{userLogin}\"')
        if not utils.isValidStr(userName):
            raise ValueError(f'userName argument is malformed: \"{userName}\"')
        assert gameId is None or isinstance(gameId, str), f"malformed {gameId=}"
        assert gameName is None or isinstance(gameName, str), f"malformed {gameName=}"
        assert language is None or isinstance(language, str), f"malformed {language=}"
        assert thumbnailUrl is None or isinstance(thumbnailUrl, str), f"malformed {thumbnailUrl=}"
        assert title is None or isinstance(title, str), f"malformed {title=}"
        assert isinstance(streamType, TwitchStreamType), f"malformed {streamType=}"

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
