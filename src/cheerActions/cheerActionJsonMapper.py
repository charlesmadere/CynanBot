import json
import re
from typing import Any, Collection, Final, Pattern

from frozendict import frozendict
from frozenlist import FrozenList

from .absCheerAction import AbsCheerAction
from .cheerActionJsonMapperInterface import CheerActionJsonMapperInterface
from .cheerActionStreamStatusRequirement import CheerActionStreamStatusRequirement
from .cheerActionType import CheerActionType
from .crowdControl.crowdControlButtonPressCheerAction import CrowdControlButtonPressCheerAction
from .crowdControl.crowdControlGameShuffleCheerAction import CrowdControlGameShuffleCheerAction
from .itemUse.itemUseCheerAction import ItemUseCheerAction
from .soundAlert.soundAlertCheerAction import SoundAlertCheerAction
from ..chatterInventory.mappers.chatterInventoryMapperInterface import ChatterInventoryMapperInterface
from ..misc import utils as utils


class CheerActionJsonMapper(CheerActionJsonMapperInterface):

    def __init__(
        self,
        chatterInventoryMapper: ChatterInventoryMapperInterface,
    ):
        if not isinstance(chatterInventoryMapper, ChatterInventoryMapperInterface):
            raise TypeError(f'chatterInventoryMapper argument is malformed: \"{chatterInventoryMapper}\"')

        self.__chatterInventoryMapper: Final[ChatterInventoryMapperInterface] = chatterInventoryMapper

        self.__cheerActionTypeRegExes: Final[frozendict[CheerActionType, Collection[Pattern]]] = self.__createCheerActionTypeRegExes()

    def __createCheerActionTypeRegExes(self) -> frozendict[CheerActionType, FrozenList[Pattern]]:
        adge: FrozenList[Pattern] = FrozenList()
        adge.append(re.compile(r'\s*ads?\s*$', re.IGNORECASE))
        adge.append(re.compile(r'\s*adge\s*$', re.IGNORECASE))
        adge.append(re.compile(r'\s*ad\s*$', re.IGNORECASE))
        adge.append(re.compile(r'\s*adverts?\s*$', re.IGNORECASE))
        adge.freeze()

        airStrike: FrozenList[Pattern] = FrozenList()
        airStrike.append(re.compile(r'\s*air(?:\s+|_|-)?strike\s*$', re.IGNORECASE))
        airStrike.append(re.compile(r'\s*tnt\s*$', re.IGNORECASE))
        airStrike.freeze()

        crowdControl: FrozenList[Pattern] = FrozenList()
        crowdControl.append(re.compile(r'\s*crowd(?:\s+|_|-)?control\s*$', re.IGNORECASE))
        crowdControl.freeze()

        gameShuffle: FrozenList[Pattern] = FrozenList()
        gameShuffle.append(re.compile(r'\s*game(?:\s+|_|-)?shuffle\s*$', re.IGNORECASE))
        gameShuffle.freeze()

        itemUse: FrozenList[Pattern] = FrozenList()
        itemUse.append(re.compile(r'\s*item\s*$', re.IGNORECASE))
        itemUse.append(re.compile(r'\s*item(?:\s+|_|-)?use\s*$', re.IGNORECASE))
        itemUse.append(re.compile(r'\s*use(?:\s+|_|-)?item\s*$', re.IGNORECASE))
        itemUse.freeze()

        soundAlert: FrozenList[Pattern] = FrozenList()
        soundAlert.append(re.compile(r'\s*sound\s*$', re.IGNORECASE))
        soundAlert.append(re.compile(r'\s*sound(?:\s+|_|-)?alert\s*$', re.IGNORECASE))
        soundAlert.freeze()

        timeout: FrozenList[Pattern] = FrozenList()
        timeout.append(re.compile(r'\s*timeout\s*$', re.IGNORECASE))
        timeout.freeze()

        voicemail: FrozenList[Pattern] = FrozenList()
        voicemail.append(re.compile(r'\s*voicemails?\s*$', re.IGNORECASE))
        voicemail.freeze()

        return frozendict({
            CheerActionType.CROWD_CONTROL: crowdControl,
            CheerActionType.GAME_SHUFFLE: gameShuffle,
            CheerActionType.ITEM_USE: itemUse,
            CheerActionType.SOUND_ALERT: soundAlert,
        })

    async def parseCheerActionStreamStatusRequirement(
        self,
        jsonString: str | Any | None,
    ) -> CheerActionStreamStatusRequirement | None:
        if not utils.isValidStr(jsonString):
            return None

        jsonString = jsonString.lower()

        match jsonString:
            case 'any': return CheerActionStreamStatusRequirement.ANY
            case 'offline': return CheerActionStreamStatusRequirement.OFFLINE
            case 'online': return CheerActionStreamStatusRequirement.ONLINE
            case _: return None

    async def parseCheerActionType(
        self,
        jsonString: str | Any | None,
    ) -> CheerActionType | None:
        if not utils.isValidStr(jsonString):
            return None

        for cheerActionType, regExes in self.__cheerActionTypeRegExes.items():
            for regEx in regExes:
                if regEx.fullmatch(jsonString):
                    return cheerActionType

        return None

    async def parseCrowdControlButtonPressCheerAction(
        self,
        isEnabled: bool,
        streamStatusRequirement: CheerActionStreamStatusRequirement,
        bits: int,
        jsonString: str | None,
        twitchChannelId: str,
    ) -> CrowdControlButtonPressCheerAction | None:
        if not utils.isValidStr(jsonString):
            return None

        return CrowdControlButtonPressCheerAction(
            enabled = isEnabled,
            streamStatusRequirement = streamStatusRequirement,
            bits = bits,
            twitchChannelId = twitchChannelId,
        )

    async def parseCrowdControlGameShuffleCheerAction(
        self,
        isEnabled: bool,
        streamStatusRequirement: CheerActionStreamStatusRequirement,
        bits: int,
        jsonString: str | None,
        twitchChannelId: str,
    ) -> CrowdControlGameShuffleCheerAction | None:
        if not utils.isValidStr(jsonString):
            return None

        jsonContents: dict[str, Any] = json.loads(jsonString)

        gigaShuffleChance: int | None = None
        if 'gigaShuffleChance' in jsonContents and utils.isValidInt(jsonContents.get('gigaShuffleChance')):
            gigaShuffleChance = utils.getIntFromDict(jsonContents, 'gigaShuffleChance')

        return CrowdControlGameShuffleCheerAction(
            enabled = isEnabled,
            streamStatusRequirement = streamStatusRequirement,
            bits = bits,
            gigaShuffleChance = gigaShuffleChance,
            twitchChannelId = twitchChannelId,
        )

    async def parseItemUseCheerAction(
        self,
        isEnabled: bool,
        streamStatusRequirement: CheerActionStreamStatusRequirement,
        bits: int,
        jsonString: str | None,
        twitchChannelId: str,
    ) -> ItemUseCheerAction | None:
        if not utils.isValidStr(jsonString):
            return None

        jsonContents: dict[str, Any] = json.loads(jsonString)

        itemType = await self.__chatterInventoryMapper.requireItemType(
            itemType = utils.getStrFromDict(jsonContents, 'itemType'),
        )

        return ItemUseCheerAction(
            enabled = isEnabled,
            itemType = itemType,
            streamStatusRequirement = streamStatusRequirement,
            bits = bits,
            twitchChannelId = twitchChannelId,
        )

    async def parseSoundAlertCheerAction(
        self,
        isEnabled: bool,
        streamStatusRequirement: CheerActionStreamStatusRequirement,
        bits: int,
        jsonString: str | None,
        twitchChannelId: str,
    ) -> SoundAlertCheerAction | None:
        if not utils.isValidStr(jsonString):
            return None

        jsonContents: dict[str, Any] = json.loads(jsonString)

        directory = utils.getStrFromDict(jsonContents, 'directory')

        return SoundAlertCheerAction(
            enabled = isEnabled,
            streamStatusRequirement = streamStatusRequirement,
            bits = bits,
            directory = directory,
            twitchChannelId = twitchChannelId,
        )

    async def requireCheerActionStreamStatusRequirement(
        self,
        jsonString: str | Any | None,
    ) -> CheerActionStreamStatusRequirement:
        streamStatusRequirement = await self.parseCheerActionStreamStatusRequirement(jsonString)

        if streamStatusRequirement is None:
            raise ValueError(f'Unable to parse \"{jsonString}\" into CheerActionStreamStatusRequirement value!')

        return streamStatusRequirement

    async def requireCheerActionType(
        self,
        jsonString: str | Any | None,
    ) -> CheerActionType:
        actionType = await self.parseCheerActionType(jsonString)

        if actionType is None:
            raise ValueError(f'Unable to parse \"{jsonString}\" into CheerActionType value!')

        return actionType

    async def requireCrowdControlButtonPressCheerAction(
        self,
        isEnabled: bool,
        streamStatusRequirement: CheerActionStreamStatusRequirement,
        bits: int,
        jsonString: str | None,
        twitchChannelId: str,
    ) -> CrowdControlButtonPressCheerAction:
        action = await self.parseCrowdControlButtonPressCheerAction(
            isEnabled = isEnabled,
            streamStatusRequirement = streamStatusRequirement,
            bits = bits,
            jsonString = jsonString,
            twitchChannelId = twitchChannelId,
        )

        if action is None:
            raise ValueError(f'Unable to create CrowdControlButtonPressCheerAction! ({isEnabled=}) ({streamStatusRequirement=}) ({bits=}) ({jsonString=}) ({twitchChannelId=})')

        return action

    async def requireCrowdControlGameShuffleCheerAction(
        self,
        isEnabled: bool,
        streamStatusRequirement: CheerActionStreamStatusRequirement,
        bits: int,
        jsonString: str | None,
        twitchChannelId: str,
    ) -> CrowdControlGameShuffleCheerAction:
        action = await self.parseCrowdControlGameShuffleCheerAction(
            isEnabled = isEnabled,
            streamStatusRequirement = streamStatusRequirement,
            bits = bits,
            jsonString = jsonString,
            twitchChannelId = twitchChannelId,
        )

        if action is None:
            raise ValueError(f'Unable to create CrowdControlGameShuffleCheerAction! ({isEnabled=}) ({streamStatusRequirement=}) ({bits=}) ({jsonString=}) ({twitchChannelId=})')

        return action

    async def requireItemUseCheerAction(
        self,
        isEnabled: bool,
        streamStatusRequirement: CheerActionStreamStatusRequirement,
        bits: int,
        jsonString: str | None,
        twitchChannelId: str,
    ) -> ItemUseCheerAction:
        action = await self.parseItemUseCheerAction(
            isEnabled = isEnabled,
            streamStatusRequirement = streamStatusRequirement,
            bits = bits,
            jsonString = jsonString,
            twitchChannelId = twitchChannelId,
        )

        if action is None:
            raise ValueError(f'Unable to create ItemUseCheerAction! ({isEnabled=}) ({streamStatusRequirement=}) ({bits=}) ({jsonString=}) ({twitchChannelId=})')

        return action

    async def requireSoundAlertCheerAction(
        self,
        isEnabled: bool,
        streamStatusRequirement: CheerActionStreamStatusRequirement,
        bits: int,
        jsonString: str | None,
        twitchChannelId: str,
    ) -> SoundAlertCheerAction:
        action = await self.parseSoundAlertCheerAction(
            isEnabled = isEnabled,
            streamStatusRequirement = streamStatusRequirement,
            bits = bits,
            jsonString = jsonString,
            twitchChannelId = twitchChannelId,
        )

        if action is None:
            raise ValueError(f'Unable to create SoundAlertCheerAction! ({isEnabled=}) ({streamStatusRequirement=}) ({bits=}) ({jsonString=}) ({twitchChannelId=})')

        return action

    async def serializeAbsCheerAction(
        self,
        cheerAction: AbsCheerAction,
    ) -> str:
        if not isinstance(cheerAction, AbsCheerAction):
            raise TypeError(f'cheerAction argument is malformed: \"{cheerAction}\"')

        if isinstance(cheerAction, CrowdControlButtonPressCheerAction):
            return await self.__serializeCrowdControlButtonPressCheerAction(cheerAction)

        elif isinstance(cheerAction, CrowdControlGameShuffleCheerAction):
            return await self.__serializeCrowdControlGameShuffleCheerAction(cheerAction)

        elif isinstance(cheerAction, ItemUseCheerAction):
            return await self.__serializeItemUseCheerAction(cheerAction)

        elif isinstance(cheerAction, SoundAlertCheerAction):
            return await self.__serializeSoundAlertCheerAction(cheerAction)

        else:
            raise RuntimeError(f'Encountered unknown AbsCheerAction type ({cheerAction=})')

    async def serializeCheerActionStreamStatusRequirement(
        self,
        streamStatusRequirement: CheerActionStreamStatusRequirement,
    ) -> str:
        if not isinstance(streamStatusRequirement, CheerActionStreamStatusRequirement):
            raise TypeError(f'streamStatusRequirement argument is malformed: \"{streamStatusRequirement}\"')

        match streamStatusRequirement:
            case CheerActionStreamStatusRequirement.ANY: return 'any'
            case CheerActionStreamStatusRequirement.OFFLINE: return 'offline'
            case CheerActionStreamStatusRequirement.ONLINE: return 'online'
            case _: raise ValueError(f'The given CheerActionStreamStatusRequirement value is unknown: \"{streamStatusRequirement}\"')

    async def serializeCheerActionType(
        self,
        actionType: CheerActionType,
    ) -> str:
        if not isinstance(actionType, CheerActionType):
            raise TypeError(f'actionType argument is malformed: \"{actionType}\"')

        match actionType:
            case CheerActionType.CROWD_CONTROL: return 'crowd_control'
            case CheerActionType.GAME_SHUFFLE: return 'game_shuffle'
            case CheerActionType.ITEM_USE: return 'item_use'
            case CheerActionType.SOUND_ALERT: return 'sound_alert'
            case _: raise ValueError(f'The given CheerActionType value is unknown: \"{actionType}\"')

    async def __serializeCrowdControlButtonPressCheerAction(
        self,
        cheerAction: CrowdControlButtonPressCheerAction,
    ) -> str:
        if not isinstance(cheerAction, CrowdControlButtonPressCheerAction):
            raise TypeError(f'cheerAction argument is malformed: \"{cheerAction}\"')

        jsonContents: dict[str, Any] = dict()
        return json.dumps(jsonContents)

    async def __serializeCrowdControlGameShuffleCheerAction(
        self,
        cheerAction: CrowdControlGameShuffleCheerAction,
    ) -> str:
        if not isinstance(cheerAction, CrowdControlGameShuffleCheerAction):
            raise TypeError(f'cheerAction argument is malformed: \"{cheerAction}\"')

        jsonContents: dict[str, Any] = dict()

        if utils.isValidInt(cheerAction.gigaShuffleChance):
            jsonContents['gigaShuffleChance'] = cheerAction.gigaShuffleChance

        return json.dumps(jsonContents)

    async def __serializeItemUseCheerAction(
        self,
        cheerAction: ItemUseCheerAction,
    ) -> str:
        if not isinstance(cheerAction, ItemUseCheerAction):
            raise TypeError(f'cheerAction argument is malformed: \"{cheerAction}\"')

        itemTypeString = await self.__chatterInventoryMapper.serializeItemType(
            itemType = cheerAction.itemType,
        )

        jsonContents: dict[str, Any] = {
            'itemType': itemTypeString,
        }

        return json.dumps(jsonContents)

    async def __serializeSoundAlertCheerAction(
        self,
        cheerAction: SoundAlertCheerAction,
    ) -> str:
        if not isinstance(cheerAction, SoundAlertCheerAction):
            raise TypeError(f'cheerAction argument is malformed: \"{cheerAction}\"')

        jsonContents: dict[str, Any] = {
            'directory': cheerAction.directory,
        }

        return json.dumps(jsonContents)
