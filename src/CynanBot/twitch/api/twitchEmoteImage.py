import CynanBot.misc.utils as utils
from CynanBot.twitch.api.twitchEmoteImageScale import TwitchEmoteImageScale


class TwitchEmoteImage():

    def __init__(self, url: str, imageScale: TwitchEmoteImageScale):
        if not utils.isValidUrl(url):
            raise ValueError(f'url argument is malformed: \"{url}\"')
        assert isinstance(imageScale, TwitchEmoteImageScale), f"malformed {imageScale=}"

        self.__url: str = url
        self.__imageScale: TwitchEmoteImageScale = imageScale

    def getImageScale(self) -> TwitchEmoteImageScale:
        return self.__imageScale

    def getUrl(self) -> str:
        return self.__url
