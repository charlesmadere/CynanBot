from typing import Any

from .ttsMonsterPrivateApiJsonMapperInterface import TtsMonsterPrivateApiJsonMapperInterface
from ..models.ttsMonsterPrivateApiTtsData import TtsMonsterPrivateApiTtsData
from ..models.ttsMonsterPrivateApiTtsResponse import TtsMonsterPrivateApiTtsResponse
from ...misc import utils as utils
from ...timber.timberInterface import TimberInterface


class TtsMonsterPrivateApiJsonMapper(TtsMonsterPrivateApiJsonMapperInterface):

    def __init__(self, timber: TimberInterface):
        if not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')

        self.__timber: TimberInterface = timber

    async def parseTtsData(
        self,
        jsonContents: dict[str, Any] | Any | None
    ) -> TtsMonsterPrivateApiTtsData | None:
        if not isinstance(jsonContents, dict) or len(jsonContents) == 0:
            return None

        link = utils.getStrFromDict(jsonContents, 'link')

        warning: str | None = None
        if 'warning' in jsonContents and utils.isValidStr(jsonContents.get('warning', None)):
            warning = utils.getStrFromDict(jsonContents, 'warning')

        return TtsMonsterPrivateApiTtsData(
            link = link,
            warning = warning
        )

    async def parseTtsResponse(
        self,
        jsonContents: dict[str, Any] | Any | None
    ) -> TtsMonsterPrivateApiTtsResponse | None:
        if not isinstance(jsonContents, dict) or len(jsonContents) == 0:
            return None

        status = utils.getIntFromDict(jsonContents, 'status')

        data = await self.parseTtsData(jsonContents.get('data'))
        if data is None:
            return None

        return TtsMonsterPrivateApiTtsResponse(
            status = status,
            data = data
        )
