import random
import re
import traceback
from typing import Collection, Final, Pattern

from .absChatCommand2 import AbsChatCommand2
from .chatCommandResult import ChatCommandResult
from ..misc import utils as utils
from ..misc.administratorProviderInterface import AdministratorProviderInterface
from ..timber.timberInterface import TimberInterface
from ..twitch.chatMessenger.twitchChatMessengerInterface import TwitchChatMessengerInterface
from ..twitch.localModels.twitchChatMessage import TwitchChatMessage
from ..users.exceptions import BadModifyUserValueException
from ..users.userJsonConstant import UserJsonConstant
from ..users.usersRepositoryInterface import UsersRepositoryInterface


class ChangeUserSettingChatCommand(AbsChatCommand2):

    def __init__(
        self,
        administratorProvider: AdministratorProviderInterface,
        timber: TimberInterface,
        twitchChatMessenger: TwitchChatMessengerInterface,
        usersRepository: UsersRepositoryInterface,
    ):
        if not isinstance(administratorProvider, AdministratorProviderInterface):
            raise TypeError(f'administratorProvider argument is malformed: \"{administratorProvider}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(twitchChatMessenger, TwitchChatMessengerInterface):
            raise TypeError(f'twitchChatMessenger argument is malformed: \"{twitchChatMessenger}\"')
        elif not isinstance(usersRepository, UsersRepositoryInterface):
            raise TypeError(f'usersRepository argument is malformed: \"{usersRepository}\"')

        self.__administratorProvider: Final[AdministratorProviderInterface] = administratorProvider
        self.__timber: Final[TimberInterface] = timber
        self.__twitchChatMessenger: Final[TwitchChatMessengerInterface] = twitchChatMessenger
        self.__usersRepository: Final[UsersRepositoryInterface] = usersRepository

        self.__commandPatterns: Final[Collection[Pattern]] = frozenset({
            re.compile(r'^\s*!change(?:user)?setting\b', re.IGNORECASE),
        })

    @property
    def commandName(self) -> str:
        return 'ChangeUserSettingChatCommand'

    @property
    def commandPatterns(self) -> Collection[Pattern]:
        return self.__commandPatterns

    async def __getRandomJsonConstant(self) -> UserJsonConstant:
        jsonConstants: list[UserJsonConstant] = [
            UserJsonConstant.ANIV_MESSAGE_COPY_TIMEOUT_ENABLED,
            UserJsonConstant.ECCO_ENABLED,
            UserJsonConstant.RECURRING_ACTIONS_ENABLED,
            UserJsonConstant.TTS_ENABLED,
        ]

        return random.choice(jsonConstants)

    async def handleChatCommand(self, chatMessage: TwitchChatMessage) -> ChatCommandResult:
        if not await self.__hasPermissions(chatMessage):
            return ChatCommandResult.IGNORED

        randomJsonConstant = await self.__getRandomJsonConstant()
        randomBoolean = str(utils.randomBool()).lower()

        splits = utils.getCleanedSplits(chatMessage.text)
        if len(splits) < 2:
            self.__timber.log(self.commandName, f'Attempted to handle command, but no arguments were supplied ({splits=}) ({chatMessage=})')
            self.__twitchChatMessenger.send(
                text = f'⚠ Unable to change user setting as no key argument was given. Example: !changeusersetting {randomJsonConstant.jsonKey.lower()} {randomBoolean}',
                twitchChannelId = chatMessage.twitchChannelId,
                replyMessageId = chatMessage.twitchChatMessageId,
            )
            return ChatCommandResult.CONSUMED
        elif len(splits) < 3:
            self.__timber.log(self.commandName, f'Attempted to handle command, but no value argument was supplied ({splits=}) ({chatMessage=})')
            self.__twitchChatMessenger.send(
                text = f'⚠ Unable to change user setting as no value argument was given. Example: !changeusersetting {randomJsonConstant.jsonKey.lower()} {randomBoolean}',
                twitchChannelId = chatMessage.twitchChannelId,
                replyMessageId = chatMessage.twitchChatMessageId,
            )
            return ChatCommandResult.CONSUMED

        jsonConstantString: str | None = splits[1]

        jsonConstant = await self.__stringToUserJsonConstant(
            jsonConstantString = jsonConstantString,
        )

        if jsonConstant is None:
            self.__timber.log('ChangeUserSettingChatCommand', f'Attempted to handle command, but an invalid key argument was supplied ({jsonConstant=}) ({jsonConstantString=}) ({splits=}) ({chatMessage=})')
            self.__twitchChatMessenger.send(
                text = f'⚠ Unable to change user setting as an invalid key argument was given. Example: !changeusersetting {randomJsonConstant.jsonKey.lower()} {randomBoolean}',
                twitchChannelId = chatMessage.twitchChannelId,
                replyMessageId = chatMessage.twitchChatMessageId,
            )
            return ChatCommandResult.CONSUMED

        value: str | None = splits[2]

        try:
            await self.__usersRepository.modifyUserValue(
                handle = chatMessage.twitchUser.handle,
                jsonConstant = jsonConstant,
                value = value,
            )
        except BadModifyUserValueException as e:
            self.__timber.log('ChangeUserSettingChatCommand', f'Attempted to handle command, but an invalid value argument was supplied ({value=}) ({jsonConstant=}) ({jsonConstantString=}) ({splits=}) ({chatMessage=})', e, traceback.format_exc())
            self.__twitchChatMessenger.send(
                text = f'⚠ Unable to change user setting as an invalid value argument was given. Example: !changeusersetting {randomJsonConstant.jsonKey.lower()} {randomBoolean}',
                twitchChannelId = chatMessage.twitchChannelId,
                replyMessageId = chatMessage.twitchChatMessageId,
            )
            return ChatCommandResult.CONSUMED

        self.__twitchChatMessenger.send(
            text = f'ⓘ Updated user setting {jsonConstant.jsonKey.lower()}',
            twitchChannelId = chatMessage.twitchChannelId,
            replyMessageId = chatMessage.twitchChatMessageId,
        )

        self.__timber.log(self.commandName, f'Handled ({jsonConstant=}) ({chatMessage=})')
        return ChatCommandResult.CONSUMED

    async def __hasPermissions(self, chatMessage: TwitchChatMessage) -> bool:
        isStreamer = chatMessage.chatterUserId == chatMessage.twitchChannelId
        isAdministrator = chatMessage.chatterUserId == await self.__administratorProvider.getAdministratorUserId()
        return isStreamer or isAdministrator

    async def __stringToUserJsonConstant(self, jsonConstantString: str | None) -> UserJsonConstant | None:
        if not utils.isValidStr(jsonConstantString):
            return None

        stringToUserJsonConstantsDictionary: dict[str, UserJsonConstant] = dict()

        for jsonConstant in UserJsonConstant:
            stringToUserJsonConstantsDictionary[jsonConstant.jsonKey.casefold()] = jsonConstant

        return stringToUserJsonConstantsDictionary.get(jsonConstantString.casefold(), None)
