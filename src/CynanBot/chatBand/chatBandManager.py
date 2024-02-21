from datetime import timedelta
from typing import Any, Dict, Optional

import CynanBot.misc.utils as utils
from CynanBot.chatBand.chatBandInstrument import ChatBandInstrument
from CynanBot.chatBand.chatBandManagerInterface import ChatBandManagerInterface
from CynanBot.chatBand.chatBandMember import ChatBandMember
from CynanBot.misc.timedDict import TimedDict
from CynanBot.storage.jsonReaderInterface import JsonReaderInterface
from CynanBot.timber.timberInterface import TimberInterface
from CynanBot.websocketConnection.websocketConnectionServerInterface import \
    WebsocketConnectionServerInterface


class ChatBandManager(ChatBandManagerInterface):

    def __init__(
        self,
        settingsJsonReader: JsonReaderInterface,
        timber: TimberInterface,
        websocketConnectionServer: WebsocketConnectionServerInterface,
        websocketEventType: str = 'chatBand',
        eventCooldown: timedelta = timedelta(minutes = 5),
        memberCacheTimeToLive: timedelta = timedelta(minutes = 15)
    ):
        assert isinstance(settingsJsonReader, JsonReaderInterface), f"malformed {settingsJsonReader=}"
        assert isinstance(timber, TimberInterface), f"malformed {timber=}"
        assert isinstance(websocketConnectionServer, WebsocketConnectionServerInterface), f"malformed {websocketConnectionServer=}"
        if not utils.isValidStr(websocketEventType):
            raise ValueError(f'websocketEventType argument is malformed: \"{websocketEventType}\"')
        assert isinstance(eventCooldown, timedelta), f"malformed {eventCooldown=}"
        assert isinstance(memberCacheTimeToLive, timedelta), f"malformed {memberCacheTimeToLive=}"

        self.__settingsJsonReader: JsonReaderInterface = settingsJsonReader
        self.__timber: TimberInterface = timber
        self.__websocketConnectionServer: WebsocketConnectionServerInterface = websocketConnectionServer
        self.__websocketEventType: str = websocketEventType

        self.__stubChatBandMember = ChatBandMember(
            isEnabled = False,
            instrument = ChatBandInstrument.BASS,
            author = 'stub',
            keyPhrase = 'stub'
        )

        self.__jsonCache: Optional[Dict[str, Any]] = None
        self.__chatBandMemberCache: TimedDict = TimedDict(memberCacheTimeToLive)
        self.__lastChatBandMessageTimes: TimedDict = TimedDict(eventCooldown)

    async def clearCaches(self):
        self.__lastChatBandMessageTimes.clear()
        self.__chatBandMemberCache.clear()
        self.__jsonCache = None
        self.__timber.log('ChatBandManager', 'Caches cleared')

    async def __findChatBandMember(
        self,
        twitchChannel: str,
        author: str,
        message: str
    ) -> Optional[ChatBandMember]:
        if not utils.isValidStr(twitchChannel):
            raise ValueError(f'twitchChannel argument is malformed: \"{twitchChannel}\"')
        if not utils.isValidStr(author):
            raise ValueError(f'author argument is malformed: \"{author}\"')
        if not utils.isValidStr(message):
            raise ValueError(f'message argument is malformed: \"{message}\"')

        isDebugLoggingEnabled = await self.__isDebugLoggingEnabled()
        chatBandMember = self.__chatBandMemberCache[self.__getCooldownKey(twitchChannel, author)]

        if chatBandMember is None:
            jsonContents = await self.__readJsonForTwitchChannel(twitchChannel)

            if utils.hasItems(jsonContents):
                for key in jsonContents:
                    if key.lower() == author.lower():
                        chatBandMemberJson = jsonContents[key]

                        chatBandMember = ChatBandMember(
                            isEnabled = utils.getBoolFromDict(chatBandMemberJson, 'isEnabled', fallback = True),
                            instrument = ChatBandInstrument.fromStr(utils.getStrFromDict(chatBandMemberJson, 'instrument')),
                            author = key,
                            keyPhrase = utils.getStrFromDict(chatBandMemberJson, 'keyPhrase')
                        )

                        self.__chatBandMemberCache[self.__getCooldownKey(twitchChannel, author)] = chatBandMember

                        if isDebugLoggingEnabled:
                            self.__timber.log('ChatBandManager', f'Saving \"{twitchChannel}\" chat band member in cache: {self.__toEventData(chatBandMember)}')

                        break

        if chatBandMember is None:
            self.__chatBandMemberCache[self.__getCooldownKey(twitchChannel, author)] = self.__stubChatBandMember

        if chatBandMember is not None and chatBandMember is not self.__stubChatBandMember and chatBandMember.isEnabled() and chatBandMember.getKeyPhrase() == message:
            if isDebugLoggingEnabled:
                self.__timber.log('ChatBandManager', f'Found corresponding \"{twitchChannel}\" chat band member for given message: {self.__toEventData(chatBandMember)}')

            return chatBandMember
        else:
            return None

    def __getCooldownKey(self, twitchChannel: str, author: str) -> str:
        if not utils.isValidStr(twitchChannel):
            raise ValueError(f'twitchChannel argument is malformed: \"{twitchChannel}\"')
        if not utils.isValidStr(author):
            raise ValueError(f'author argument is malformed: \"{author}\"')

        return f'{twitchChannel.lower()}:{author.lower()}'

    async def __isDebugLoggingEnabled(self) -> bool:
        jsonContents = await self.__readAllJson()
        return utils.getBoolFromDict(jsonContents, 'debugLoggingEnabled', fallback = False)

    async def playInstrumentForMessage(self, twitchChannel: str, author: str, message: str) -> bool:
        if not utils.isValidStr(twitchChannel):
            raise ValueError(f'twitchChannel argument is malformed: \"{twitchChannel}\"')
        if not utils.isValidStr(author):
            raise ValueError(f'author argument is malformed: \"{author}\"')
        if not utils.isValidStr(message):
            raise ValueError(f'message argument is malformed: \"{message}\"')

        chatBandMember = await self.__findChatBandMember(
            twitchChannel = twitchChannel,
            author = author,
            message = message
        )

        if chatBandMember is None:
            return False
        elif chatBandMember is self.__stubChatBandMember:
            return False
        elif not self.__lastChatBandMessageTimes.isReadyAndUpdate(self.__getCooldownKey(twitchChannel, author)):
            return False

        eventData = self.__toEventData(chatBandMember)

        if await self.__isDebugLoggingEnabled():
            self.__timber.log('ChatBandManager', f'New \"{twitchChannel}\" Chat Band event: {eventData}')

        await self.__websocketConnectionServer.sendEvent(
            twitchChannel = twitchChannel,
            eventType = self.__websocketEventType,
            eventData = eventData
        )

        return True

    async def __readAllJson(self) -> Dict[str, Any]:
        if self.__jsonCache is not None:
            return self.__jsonCache

        if not await self.__settingsJsonReader.fileExistsAsync():
            raise FileNotFoundError(f'Chat Band file not found: \"{self.__settingsJsonReader}\"')

        jsonContents = await self.__settingsJsonReader.readJsonAsync()

        if jsonContents is None:
            raise IOError(f'Error reading from Chat Band file: \"{self.__settingsJsonReader}\"')
        if len(jsonContents) == 0:
            raise ValueError(f'JSON contents of Chat Band file \"{self.__settingsJsonReader}\" is empty')

        self.__jsonCache = jsonContents
        return jsonContents

    async def __readJsonForTwitchChannel(self, twitchChannel: str) -> Optional[Dict[str, Any]]:
        if not utils.isValidStr(twitchChannel):
            raise ValueError(f'twitchChannel argument is malformed: \"{twitchChannel}\"')

        jsonContents = await self.__readAllJson()
        twitchChannelsJson: Optional[Dict[str, Any]] = jsonContents.get('twitchChannels')
        if not utils.hasItems(twitchChannelsJson):
            raise ValueError(f'\"twitchChannels\" JSON contents of Chat Band file \"{self.__settingsJsonReader}\" is missing/empty')

        twitchChannel = twitchChannel.lower()

        for key in twitchChannelsJson:
            if key.lower() == twitchChannel:
                return twitchChannelsJson[key]

        return None

    def __toEventData(self, chatBandMember: ChatBandMember) -> Dict[str, Any]:
        assert isinstance(chatBandMember, ChatBandMember), f"malformed {chatBandMember=}"

        return {
            'author': chatBandMember.getAuthor(),
            'instrument': chatBandMember.getInstrument().toStr(),
            'keyPhrase': chatBandMember.getKeyPhrase()
        }
