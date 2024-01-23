from CynanBot.vlcHelper.vlcHelperInterface import VlcHelperInterface
import traceback
from typing import Optional
import CynanBot.misc.utils as utils
import vlc
from CynanBot.timber.timberInterface import TimberInterface


class VlcHelper(VlcHelperInterface):

    def __init__(self, timber: TimberInterface):
        if not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')

        self.__timber: TimberInterface = timber

    async def play(self, filePath: str):
        if not utils.isValidStr(filePath):
            self.__timber.log('VlcHelper', f'filePath argument is invalid: \"{filePath}\"')
            return

        exception: Optional[Exception] = None

        try:
            player = vlc.MediaPlayer(filePath)
            player.play()
        except Exception as e:
            exception = e

        if exception is None:
            self.__timber.log('VlcHelper', f'Played media using VLC ({filePath=})')
        else:
            self.__timber.log('VlcHelper', f'Attempted to play media using VLC ({filePath=}) but encountered an exception: {exception}', exception, traceback.format_exc())
