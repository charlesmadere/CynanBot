import random
import traceback

from .absChatCommand import AbsChatCommand
from ..misc import utils as utils
from ..timber.timberInterface import TimberInterface
from ..twitch.configuration.twitchContext import TwitchContext
from ..twitch.twitchUtilsInterface import TwitchUtilsInterface
from ..users.exceptions import BadModifyUserValueException
from ..users.userJsonConstant import UserJsonConstant
from ..users.usersRepositoryInterface import UsersRepositoryInterface


class ChangeUserSettingChatCommand(AbsChatCommand):

    def __init__(
        self,
        timber: TimberInterface,
        twitchUtils: TwitchUtilsInterface,
        usersRepository: UsersRepositoryInterface
    ):
        if not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(twitchUtils, TwitchUtilsInterface):
            raise TypeError(f'twitchUtils argument is malformed: \"{twitchUtils}\"')
        elif not isinstance(usersRepository, UsersRepositoryInterface):
            raise TypeError(f'usersRepository argument is malformed: \"{usersRepository}\"')

        self.__timber: TimberInterface = timber
        self.__twitchUtils: TwitchUtilsInterface = twitchUtils
        self.__usersRepository: UsersRepositoryInterface = usersRepository

    async def __getRandomJsonConstant(self) -> UserJsonConstant:
        constants: list[UserJsonConstant] = [
            UserJsonConstant.ANIV_MESSAGE_COPY_TIMEOUT_ENABLED
        ]

        return random.choice(constants)

    async def handleChatCommand(self, ctx: TwitchContext):
        user = await self.__usersRepository.getUserAsync(ctx.getTwitchChannelName())
        randomJsonConstant = await self.__getRandomJsonConstant()
        randomBoolean = str(utils.randomBool()).lower()

        splits = utils.getCleanedSplits(ctx.getMessageContent())
        if len(splits) < 2:
            self.__timber.log('ChangeUserSettingChatCommand', f'Attempted to handle command for {ctx.getAuthorName()}:{ctx.getAuthorId()} in {user.getHandle()}, but no arguments were supplied')
            await self.__twitchUtils.safeSend(ctx, f'⚠ Unable to change user setting as no key argument was given. Example: !changeusersetting {randomJsonConstant.jsonKey.lower()} {randomBoolean}')
            return
        elif len(splits) < 3:
            self.__timber.log('ChangeUserSettingChatCommand', f'Attempted to handle command for {ctx.getAuthorName()}:{ctx.getAuthorId()} in {user.getHandle()}, but no value argument was supplied')
            await self.__twitchUtils.safeSend(ctx, f'⚠ Unable to change user setting as no value argument was given. Example: !changeusersetting {randomJsonConstant.jsonKey.lower()} {randomBoolean}')
            return

        jsonConstantString: str | None = splits[1]
        jsonConstant = await self.__stringToUserJsonConstant(jsonConstantString)

        if jsonConstant is None:
            self.__timber.log('ChangeUserSettingChatCommand', f'Attempted to handle command for {ctx.getAuthorName()}:{ctx.getAuthorId()} in {user.getHandle()}, but an invalid key argument was supplied')
            await self.__twitchUtils.safeSend(ctx, f'⚠ Unable to change user setting as an invalid key argument was given. Example: !changeusersetting {randomJsonConstant.jsonKey.lower()} {randomBoolean}')
            return

        value: str | None = splits[2]

        try:
            await self.__usersRepository.modifyUserValue(
                handle = user.getHandle(),
                jsonConstant = jsonConstant,
                value = value
            )
        except BadModifyUserValueException as e:
            self.__timber.log('ChangeUserSettingChatCommand', f'Attempted to handle command for {ctx.getAuthorName()}:{ctx.getAuthorId()} in {user.getHandle()}, but an invalid value argument was supplied: {e}', e, traceback.format_exc())
            await self.__twitchUtils.safeSend(ctx, f'⚠ Unable to change user setting as an invalid value argument was given. Example: !changeusersetting {randomJsonConstant.jsonKey.lower()} {randomBoolean}')
            return

        self.__timber.log('ChangeUserSettingChatCommand', f'Handled command for {ctx.getAuthorName()}:{ctx.getAuthorId()} in {user.getHandle()} ({jsonConstant=})')

    async def __stringToUserJsonConstant(self, jsonConstantString: str | None) -> UserJsonConstant | None:
        if not utils.isValidStr(jsonConstantString):
            return None

        stringToUserJsonConstantsDictionary: dict[str, UserJsonConstant] = dict()

        for jsonConstant in UserJsonConstant:
            stringToUserJsonConstantsDictionary[jsonConstant.jsonKey.casefold()] = jsonConstant

        return stringToUserJsonConstantsDictionary.get(jsonConstantString.casefold(), None)
