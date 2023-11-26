from abc import ABC, abstractmethod
from datetime import timedelta

import CynanBot.misc.utils as utils
from CynanBot.chatBand.chatBandManagerInterface import ChatBandManagerInterface
from CynanBot.chatLogger.chatLoggerInterface import ChatLoggerInterface
from CynanBot.generalSettingsRepository import GeneralSettingsRepository
from CynanBot.misc.timedDict import TimedDict
from CynanBot.timber.timberInterface import TimberInterface
from CynanBot.twitch.twitchMessage import TwitchMessage
from CynanBot.twitch.twitchUtils import TwitchUtils
from CynanBot.users.user import User


class AbsMessage(ABC):

    @abstractmethod
    async def handleMessage(self, twitchUser: User, message: TwitchMessage) -> bool:
        pass


class CatJamMessage(AbsMessage):

    def __init__(
        self,
        generalSettingsRepository: GeneralSettingsRepository,
        timber: TimberInterface,
        twitchUtils: TwitchUtils,
        catJamMessage: str = 'catJAM',
        cooldown: timedelta = timedelta(minutes = 20)
    ):
        if not isinstance(generalSettingsRepository, GeneralSettingsRepository):
            raise ValueError(f'generalSettingsRepository argument is malformed: \"{generalSettingsRepository}\"')
        elif not isinstance(timber, TimberInterface):
            raise ValueError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(twitchUtils, TwitchUtils):
            raise ValueError(f'twitchUtils argument is malformed: \"{twitchUtils}\"')
        elif not utils.isValidStr(catJamMessage):
            raise ValueError(f'catJamMessage argument is malformed: \"{catJamMessage}\"')
        elif not isinstance(cooldown, timedelta):
            raise ValueError(f'cooldown argument is malformed: \"{cooldown}\"')

        self.__generalSettingsRepository: GeneralSettingsRepository = generalSettingsRepository
        self.__timber: TimberInterface = timber
        self.__twitchUtils: TwitchUtils = twitchUtils
        self.__catJamMessage: str = catJamMessage
        self.__lastCatJamMessageTimes: TimedDict = TimedDict(cooldown)

    async def handleMessage(self, twitchUser: User, message: TwitchMessage) -> bool:
        generalSettings = await self.__generalSettingsRepository.getAllAsync()

        if not generalSettings.isCatJamMessageEnabled():
            return False
        elif not twitchUser.isCatJamMessageEnabled():
            return False

        splits = utils.getCleanedSplits(message.getContent())

        if self.__catJamMessage in splits and self.__lastCatJamMessageTimes.isReadyAndUpdate(twitchUser.getHandle()):
            await self.__twitchUtils.safeSend(message.getChannel(), self.__catJamMessage)
            self.__timber.log('CatJamMessage', f'Handled catJAM message for {message.getAuthorName()}:{message.getAuthorId()} in {twitchUser.getHandle()}')
            return True

        return False


class ChatBandMessage(AbsMessage):

    def __init__(
        self,
        chatBandManager: ChatBandManagerInterface,
        generalSettingsRepository: GeneralSettingsRepository,
        timber: TimberInterface
    ):
        if not isinstance(chatBandManager, ChatBandManagerInterface):
            raise ValueError(f'chatBandManager argument is malformed: \"{chatBandManager}\"')
        elif not isinstance(generalSettingsRepository, GeneralSettingsRepository):
            raise ValueError(f'generalSettingsRepository argument is malformed: \"{generalSettingsRepository}\"')
        elif not isinstance(timber, TimberInterface):
            raise ValueError(f'timber argument is malformed: \"{timber}\"')

        self.__chatBandManager: ChatBandManagerInterface = chatBandManager
        self.__generalSettingsRepository: GeneralSettingsRepository = generalSettingsRepository
        self.__timber: TimberInterface = timber

    async def handleMessage(self, twitchUser: User, message: TwitchMessage) -> bool:
        generalSettings = await self.__generalSettingsRepository.getAllAsync()

        if not generalSettings.isChatBandEnabled():
            return False
        elif not twitchUser.isChatBandEnabled():
            return False

        if await self.__chatBandManager.playInstrumentForMessage(
            twitchChannel = twitchUser.getHandle(),
            author = message.getAuthorName(),
            message = utils.cleanStr(message.getContent())
        ):
            self.__timber.log('ChatBandMessage', f'Handled chat band message for {message.getAuthorName()}:{message.getAuthorId()} in {twitchUser.getHandle()}')
            return True

        return False


class ChatLogMessage(AbsMessage):

    def __init__(
        self,
        chatLogger: ChatLoggerInterface
    ):
        if not isinstance(chatLogger, ChatLoggerInterface):
            raise ValueError(f'chatLogger argument is malformed: \"{chatLogger}\"')

        self.__chatLogger: ChatLoggerInterface = chatLogger

    async def handleMessage(self, twitchUser: User, message: TwitchMessage) -> bool:
        if not twitchUser.isChatLoggingEnabled():
            return False

        self.__chatLogger.logMessage(
            twitchChannel = twitchUser.getHandle(),
            userId = message.getAuthorId(),
            userName = message.getAuthorName(),
            msg = utils.cleanStr(message.getContent())
        )

        return True


class DeerForceMessage(AbsMessage):

    def __init__(
        self,
        generalSettingsRepository: GeneralSettingsRepository,
        timber: TimberInterface,
        twitchUtils: TwitchUtils,
        deerForceMessage: str = 'D e e R F o r C e',
        cooldown: timedelta = timedelta(minutes = 30)
    ):
        if not isinstance(generalSettingsRepository, GeneralSettingsRepository):
            raise ValueError(f'generalSettingsRepository argument is malformed: \"{generalSettingsRepository}\"')
        elif not isinstance(timber, TimberInterface):
            raise ValueError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(twitchUtils, TwitchUtils):
            raise ValueError(f'twitchUtils argument is malformed: \"{twitchUtils}\"')
        elif not utils.isValidStr(deerForceMessage):
            raise ValueError(f'deerForceMessage argument is malformed: \"{deerForceMessage}\"')
        elif not isinstance(cooldown, timedelta):
            raise ValueError(f'cooldown argument is malformed: \"{cooldown}\"')

        self.__generalSettingsRepository: GeneralSettingsRepository = generalSettingsRepository
        self.__timber: TimberInterface = timber
        self.__twitchUtils: TwitchUtils = twitchUtils
        self.__deerForceMessage: str = deerForceMessage
        self.__lastDeerForceMessageTimes: TimedDict = TimedDict(cooldown)

    async def handleMessage(self, twitchUser: User, message: TwitchMessage) -> bool:
        generalSettings = await self.__generalSettingsRepository.getAllAsync()

        if not generalSettings.isDeerForceMessageEnabled():
            return False
        elif not twitchUser.isDeerForceMessageEnabled():
            return False

        text = utils.cleanStr(message.getContent())

        if text.lower() == self.__deerForceMessage.lower() and self.__lastDeerForceMessageTimes.isReadyAndUpdate(twitchUser.getHandle()):
            await self.__twitchUtils.safeSend(message.getChannel(), self.__deerForceMessage)
            self.__timber.log('DeerForceMessage', f'Handled Deer Force message for {message.getAuthorName()}:{message.getAuthorId()} in {twitchUser.getHandle()}')
            return True

        return False


class EyesMessage(AbsMessage):

    def __init__(
        self,
        generalSettingsRepository: GeneralSettingsRepository,
        timber: TimberInterface,
        twitchUtils: TwitchUtils,
        eyesMessage: str = '👀',
        cooldown: timedelta = timedelta(minutes = 20)
    ):
        if not isinstance(generalSettingsRepository, GeneralSettingsRepository):
            raise ValueError(f'generalSettingsRepository argument is malformed: \"{generalSettingsRepository}\"')
        elif not isinstance(timber, TimberInterface):
            raise ValueError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(twitchUtils, TwitchUtils):
            raise ValueError(f'twitchUtils argument is malformed: \"{twitchUtils}\"')
        elif not utils.isValidStr(eyesMessage):
            raise ValueError(f'eyesMessage argument is malformed: \"{eyesMessage}\"')
        elif not isinstance(cooldown, timedelta):
            raise ValueError(f'cooldown argument is malformed: \"{cooldown}\"')

        self.__generalSettingsRepository: GeneralSettingsRepository = generalSettingsRepository
        self.__timber: TimberInterface = timber
        self.__twitchUtils: TwitchUtils = twitchUtils
        self.__eyesMessage: str = eyesMessage
        self.__lastEyesMessageTimes: TimedDict = TimedDict(cooldown)

    async def handleMessage(self, twitchUser: User, message: TwitchMessage) -> bool:
        generalSettings = await self.__generalSettingsRepository.getAllAsync()

        if not generalSettings.isEyesMessageEnabled():
            return False
        elif not twitchUser.isEyesMessageEnabled():
            return False

        splits = utils.getCleanedSplits(message.getContent())

        if self.__eyesMessage in splits and self.__lastEyesMessageTimes.isReadyAndUpdate(twitchUser.getHandle()):
            await self.__twitchUtils.safeSend(message.getChannel(), self.__eyesMessage)
            self.__timber.log('EyesMessage', f'Handled eyes message for {message.getAuthorName()}:{message.getAuthorId()} in {twitchUser.getHandle()}')
            return True

        return False


class ImytSlurpMessage(AbsMessage):

    def __init__(
        self,
        generalSettingsRepository: GeneralSettingsRepository,
        timber: TimberInterface,
        twitchUtils: TwitchUtils,
        imytSlurpMessage: str = 'imytSlurp',
        cooldown: timedelta = timedelta(minutes = 20)
    ):
        if not isinstance(generalSettingsRepository, GeneralSettingsRepository):
            raise ValueError(f'generalSettingsRepository argument is malformed: \"{generalSettingsRepository}\"')
        elif not isinstance(timber, TimberInterface):
            raise ValueError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(twitchUtils, TwitchUtils):
            raise ValueError(f'twitchUtils argument is malformed: \"{twitchUtils}\"')
        elif not utils.isValidStr(imytSlurpMessage):
            raise ValueError(f'imytSlurpMessage argument is malformed: \"{imytSlurpMessage}\"')
        elif not isinstance(cooldown, timedelta):
            raise ValueError(f'cooldown argument is malformed: \"{cooldown}\"')

        self.__generalSettingsRepository: GeneralSettingsRepository = generalSettingsRepository
        self.__timber: TimberInterface = timber
        self.__twitchUtils: TwitchUtils = twitchUtils
        self.__imytSlurpMessage: str = imytSlurpMessage
        self.__lastImytSlurpMessageTimes: TimedDict = TimedDict(cooldown)

    async def handleMessage(self, twitchUser: User, message: TwitchMessage) -> bool:
        generalSettings = await self.__generalSettingsRepository.getAllAsync()

        if not generalSettings.isImytSlurpMessageEnabled():
            return False
        elif not twitchUser.isImytSlurpMessageEnabled():
            return False

        splits = utils.getCleanedSplits(message.getContent())

        if self.__imytSlurpMessage in splits and self.__lastImytSlurpMessageTimes.isReadyAndUpdate(twitchUser.getHandle()):
            await self.__twitchUtils.safeSend(message.getChannel(), self.__imytSlurpMessage)
            self.__timber.log('ImytSlurpMessage', f'Handled imytSlurp message for {message.getAuthorName()}:{message.getAuthorId()} in {twitchUser.getHandle()}')
            return True

        return False


class JamCatMessage(AbsMessage):

    def __init__(
        self,
        generalSettingsRepository: GeneralSettingsRepository,
        timber: TimberInterface,
        twitchUtils: TwitchUtils,
        jamCatMessage: str = 'jamCAT',
        cooldown: timedelta = timedelta(minutes = 20)
    ):
        if not isinstance(generalSettingsRepository, GeneralSettingsRepository):
            raise ValueError(f'generalSettingsRepository argument is malformed: \"{generalSettingsRepository}\"')
        elif not isinstance(timber, TimberInterface):
            raise ValueError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(twitchUtils, TwitchUtils):
            raise ValueError(f'twitchUtils argument is malformed: \"{twitchUtils}\"')
        elif not utils.isValidStr(jamCatMessage):
            raise ValueError(f'jamCatMessage argument is malformed: \"{jamCatMessage}\"')
        elif not isinstance(cooldown, timedelta):
            raise ValueError(f'cooldown argument is malformed: \"{cooldown}\"')

        self.__generalSettingsRepository: GeneralSettingsRepository = generalSettingsRepository
        self.__timber: TimberInterface = timber
        self.__twitchUtils: TwitchUtils = twitchUtils
        self.__jamCatMessage: str = jamCatMessage
        self.__lastCatJamMessageTimes: TimedDict = TimedDict(cooldown)

    async def handleMessage(self, twitchUser: User, message: TwitchMessage) -> bool:
        generalSettings = await self.__generalSettingsRepository.getAllAsync()

        if not generalSettings.isJamCatMessageEnabled():
            return False
        elif not twitchUser.isJamCatMessageEnabled():
            return False

        splits = utils.getCleanedSplits(message.getContent())

        if self.__jamCatMessage in splits and self.__lastCatJamMessageTimes.isReadyAndUpdate(twitchUser.getHandle()):
            await self.__twitchUtils.safeSend(message.getChannel(), self.__jamCatMessage)
            self.__timber.log('JamCatMessage', f'Handled jamCAT message for {message.getAuthorName()}:{message.getAuthorId()} in {twitchUser.getHandle()}')
            return True

        return False


class RatJamMessage(AbsMessage):

    def __init__(
        self,
        generalSettingsRepository: GeneralSettingsRepository,
        timber: TimberInterface,
        twitchUtils: TwitchUtils,
        ratJamMessage: str = 'ratJAM',
        cooldown: timedelta = timedelta(minutes = 20)
    ):
        if not isinstance(generalSettingsRepository, GeneralSettingsRepository):
            raise ValueError(f'generalSettingsRepository argument is malformed: \"{generalSettingsRepository}\"')
        elif not isinstance(timber, TimberInterface):
            raise ValueError(f'timber argument is malformed: \"{timber}\"')
        elif not utils.isValidStr(ratJamMessage):
            raise ValueError(f'ratJamMessage argument is malformed: \"{ratJamMessage}\"')
        elif not isinstance(cooldown, timedelta):
            raise ValueError(f'cooldown argument is malformed: \"{cooldown}\"')

        self.__generalSettingsRepository: GeneralSettingsRepository = generalSettingsRepository
        self.__timber: TimberInterface = timber
        self.__twitchUtils: TwitchUtils = twitchUtils
        self.__ratJamMessage: str = ratJamMessage
        self.__lastRatJamMessageTimes: TimedDict = TimedDict(cooldown)

    async def handleMessage(self, twitchUser: User, message: TwitchMessage) -> bool:
        generalSettings = await self.__generalSettingsRepository.getAllAsync()

        if not generalSettings.isRatJamMessageEnabled():
            return False
        elif not twitchUser.isRatJamMessageEnabled():
            return False

        splits = utils.getCleanedSplits(message.getContent())

        if self.__ratJamMessage in splits and self.__lastRatJamMessageTimes.isReadyAndUpdate(twitchUser.getHandle()):
            await self.__twitchUtils.safeSend(message.getChannel(), self.__ratJamMessage)
            self.__timber.log('RatJamMessage', f'Handled ratJAM message for {message.getAuthorName()}:{message.getAuthorId()} in {twitchUser.getHandle()}')
            return True

        return False


class RoachMessage(AbsMessage):

    def __init__(
        self,
        generalSettingsRepository: GeneralSettingsRepository,
        timber: TimberInterface,
        twitchUtils: TwitchUtils,
        roachMessage: str = 'ROACH',
        cooldown: timedelta = timedelta(minutes = 20)
    ):
        if not isinstance(generalSettingsRepository, GeneralSettingsRepository):
            raise ValueError(f'generalSettingsRepository argument is malformed: \"{generalSettingsRepository}\"')
        elif not isinstance(timber, TimberInterface):
            raise ValueError(f'timber argument is malformed: \"{timber}\"')
        elif not utils.isValidStr(roachMessage):
            raise ValueError(f'roachMessage argument is malformed: \"{roachMessage}\"')
        elif not isinstance(cooldown, timedelta):
            raise ValueError(f'cooldown argument is malformed: \"{cooldown}\"')

        self.__generalSettingsRepository: GeneralSettingsRepository = generalSettingsRepository
        self.__timber: TimberInterface = timber
        self.__twitchUtils: TwitchUtils = twitchUtils
        self.__roachMessage: str = roachMessage
        self.__lastMessageTimes: TimedDict = TimedDict(cooldown)

    async def handleMessage(self, twitchUser: User, message: TwitchMessage) -> bool:
        generalSettings = await self.__generalSettingsRepository.getAllAsync()

        if not generalSettings.isRoachMessageEnabled():
            return False
        elif not twitchUser.isRoachMessageEnabled():
            return False

        splits = utils.getCleanedSplits(message.getContent())

        if self.__roachMessage in splits and self.__lastMessageTimes.isReadyAndUpdate(twitchUser.getHandle()):
            await self.__twitchUtils.safeSend(message.getChannel(), self.__roachMessage)
            self.__timber.log('RoachMessage', f'Handled {self.__roachMessage} message for {message.getAuthorName()}:{message.getAuthorId()} in {twitchUser.getHandle()}')
            return True

        return False


class SchubertWalkMessage(AbsMessage):

    def __init__(
        self,
        generalSettingsRepository: GeneralSettingsRepository,
        timber: TimberInterface,
        twitchUtils: TwitchUtils,
        schubertWalkMessage: str = 'SchubertWalk',
        cooldown: timedelta = timedelta(minutes = 20)
    ):
        if not isinstance(generalSettingsRepository, GeneralSettingsRepository):
            raise ValueError(f'generalSettingsRepository argument is malformed: \"{generalSettingsRepository}\"')
        elif not isinstance(timber, TimberInterface):
            raise ValueError(f'timber argument is malformed: \"{timber}\"')
        elif not utils.isValidStr(schubertWalkMessage):
            raise ValueError(f'schubertWalkMessage argument is malformed: \"{schubertWalkMessage}\"')
        elif not isinstance(cooldown, timedelta):
            raise ValueError(f'cooldown argument is malformed: \"{cooldown}\"')

        self.__generalSettingsRepository: GeneralSettingsRepository = generalSettingsRepository
        self.__timber: TimberInterface = timber
        self.__twitchUtils: TwitchUtils = twitchUtils
        self.__schubertWalkMessage: str = schubertWalkMessage
        self.__lastMessageTimes: TimedDict = TimedDict(cooldown)

    async def handleMessage(self, twitchUser: User, message: TwitchMessage) -> bool:
        generalSettings = await self.__generalSettingsRepository.getAllAsync()

        if not generalSettings.isSchubertWalkMessageEnabled():
            return False
        elif not twitchUser.isSchubertWalkMessageEnabled():
            return False

        splits = utils.getCleanedSplits(message.getContent())

        if self.__schubertWalkMessage in splits and self.__lastMessageTimes.isReadyAndUpdate(twitchUser.getHandle()):
            await self.__twitchUtils.safeSend(message.getChannel(), self.__schubertWalkMessage)
            self.__timber.log('SchubertWalkMessage', f'Handled {self.__schubertWalkMessage} message for {message.getAuthorName()}:{message.getAuthorId()} in {twitchUser.getHandle()}')
            return True

        return False


class StubMessage(AbsMessage):

    def __init__(self):
        pass

    async def handleMessage(self, twitchUser: User, message: TwitchMessage) -> bool:
        return False
