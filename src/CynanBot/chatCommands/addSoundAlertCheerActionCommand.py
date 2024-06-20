import traceback

import CynanBot.misc.utils as utils
from CynanBot.administratorProviderInterface import \
    AdministratorProviderInterface
from CynanBot.chatCommands.absChatCommand import AbsChatCommand
from CynanBot.cheerActions.cheerAction import CheerAction
from CynanBot.cheerActions.cheerActionBitRequirement import \
    CheerActionBitRequirement
from CynanBot.cheerActions.cheerActionsRepositoryInterface import \
    CheerActionsRepositoryInterface
from CynanBot.cheerActions.cheerActionStreamStatusRequirement import \
    CheerActionStreamStatusRequirement
from CynanBot.cheerActions.cheerActionType import CheerActionType
from CynanBot.cheerActions.exceptions import (
    CheerActionAlreadyExistsException, TooManyCheerActionsException)
from CynanBot.timber.timberInterface import TimberInterface
from CynanBot.twitch.configuration.twitchContext import TwitchContext
from CynanBot.twitch.twitchUtilsInterface import TwitchUtilsInterface
from CynanBot.users.usersRepositoryInterface import UsersRepositoryInterface


class AddSoundAlertCheerActionCommand(AbsChatCommand):

    def __init__(
        self,
        administratorProvider: AdministratorProviderInterface,
        cheerActionsRepository: CheerActionsRepositoryInterface,
        timber: TimberInterface,
        twitchUtils: TwitchUtilsInterface,
        usersRepository: UsersRepositoryInterface
    ):
        if not isinstance(administratorProvider, AdministratorProviderInterface):
            raise TypeError(f'administratorProvider argument is malformed: \"{administratorProvider}\"')
        elif not isinstance(cheerActionsRepository, CheerActionsRepositoryInterface):
            raise TypeError(f'cheerActionsRepository argument is malformed: \"{cheerActionsRepository}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(twitchUtils, TwitchUtilsInterface):
            raise TypeError(f'twitchUtils argument is malformed: \"{twitchUtils}\"')
        elif not isinstance(usersRepository, UsersRepositoryInterface):
            raise TypeError(f'usersRepository argument is malformed: \"{usersRepository}\"')

        self.__administratorProvider: AdministratorProviderInterface = administratorProvider
        self.__cheerActionsRepository: CheerActionsRepositoryInterface = cheerActionsRepository
        self.__timber: TimberInterface = timber
        self.__twitchUtils: TwitchUtilsInterface = twitchUtils
        self.__usersRepository: UsersRepositoryInterface = usersRepository

    async def __actionToStr(self, action: CheerAction) -> str:
        if not isinstance(action, CheerAction):
            raise TypeError(f'action argument is malformed: \"{action}\"')

        cheerActionString = f'id={action.actionId}, actionType={action.actionType}, amount={action.amount}, bitRequirement={action.bitRequirement}, duration={action.durationSeconds}, streamStatus={action.streamStatusRequirement}'
        return f'ⓘ Your new timeout cheer action — {cheerActionString}'

    async def handleChatCommand(self, ctx: TwitchContext):
        user = await self.__usersRepository.getUserAsync(ctx.getTwitchChannelName())
        userId = await ctx.getTwitchChannelId()
        administrator = await self.__administratorProvider.getAdministratorUserId()

        if userId != ctx.getAuthorId() and administrator != ctx.getAuthorId():
            self.__timber.log('AddSoundAlertCheerActionCommand', f'{ctx.getAuthorName()}:{ctx.getAuthorId()} in {user.getHandle()} tried using this command!')
            return
        elif not user.areCheerActionsEnabled():
            return

        splits = utils.getCleanedSplits(ctx.getMessageContent())
        if len(splits) < 2:
            self.__timber.log('AddSoundAlertCheerActionCommand', f'Less than 2 arguments given by {ctx.getAuthorName()}:{ctx.getAuthorId()} in {user.getHandle()}')
            await self.__twitchUtils.safeSend(ctx, f'⚠ Two arguments are necessary (first bits, then a tag) for the !addsoundalertcheeraction command. Example: !addsoundalertcheeraction 50 good (50 bits, \"good\" tag)')
            return

        bitsString: str | None = splits[1]
        bits: int | None = None
        try:
            bits = int(bitsString)
        except Exception as e:
            self.__timber.log('AddSoundAlertCheerActionCommand', f'Failed to parse bitsString (\"{bitsString}\") into bits int: {e}', e, traceback.format_exc())

        # we use the tag as a path, so let's clean it before using it further
        tag: str | None = utils.cleanPath(splits[2])

        if not utils.isValidInt(bits):
            self.__timber.log('AddSoundAlertCheerActionCommand', f'The bitsString value (\"{bitsString}\") or tag value (\"{tag}\") given by {ctx.getAuthorName()}:{ctx.getAuthorId()} in {user.getHandle()} failed to parse into an int')
            await self.__twitchUtils.safeSend(ctx, f'⚠ Failed to parse your bits amount for the !addsoundalertcheeraction command. Example: !addsoundalertcheeraction 50 good (50 bits, \"good\" tag)')
            return
        elif bits < 1 or bits > utils.getIntMaxSafeSize():
            self.__timber.log('AddSoundAlertCheerActionCommand', f'The bitsString value (\"{bitsString}\") given by {ctx.getAuthorName()}:{ctx.getAuthorId()} in {user.getHandle()} is out of bounds: {bitsString}')
            await self.__twitchUtils.safeSend(ctx, f'⚠ Failed to parse either your bits amount for the !addsoundalertcheeraction command. Example: !addsoundalertcheeraction 50 good (50 bits, \"good\" tag)')
            return
        elif not utils.isValidStr(tag):
            self.__timber.log('AddSoundAlertCheerActionCommand', f'The tag value (\"{tag}\") given by {ctx.getAuthorName()}:{ctx.getAuthorId()} in {user.getHandle()} is invalid')
            await self.__twitchUtils.safeSend(ctx, f'⚠ Failed to parse either your bits amount or your tag for the !addsoundalertcheeraction command. Example: !addsoundalertcheeraction 50 good (50 bits, \"good\" tag)')
            return

        try:
            action = await self.__cheerActionsRepository.addAction(
                bitRequirement = CheerActionBitRequirement.EXACT,
                streamStatusRequirement = CheerActionStreamStatusRequirement.ONLINE,
                actionType = CheerActionType.SOUND_ALERT,
                amount = bits,
                durationSeconds = None,
                tag = tag,
                userId = userId
            )
        except CheerActionAlreadyExistsException as e:
            self.__timber.log('AddSoundAlertCheerActionCommand', f'Failed to add new cheer action for {ctx.getAuthorName()}:{ctx.getAuthorId()} in {user.getHandle()} due to this cheer action already existing: {e}', e, traceback.format_exc())
            await self.__twitchUtils.safeSend(ctx, f'⚠ Failed to add new cheer action as you already have one with these same attributes')
            return
        except TooManyCheerActionsException as e:
            self.__timber.log('AddSoundAlertCheerActionCommand', f'Failed to add new cheer action for {ctx.getAuthorName()}:{ctx.getAuthorId()} in {user.getHandle()} due to this user having the maximum number of cheer actions: {e}', e, traceback.format_exc())
            await self.__twitchUtils.safeSend(ctx, f'⚠ Failed to add new cheer action as you already have the maximum number of cheer actions')
            return
        except Exception as e:
            self.__timber.log('AddSoundAlertCheerActionCommand', f'Failed to add new cheer action for {ctx.getAuthorName()}:{ctx.getAuthorId()} in {user.getHandle()}: {e}', e, traceback.format_exc())
            await self.__twitchUtils.safeSend(ctx, f'⚠ Failed to add new cheer action. Example: !addsoundalertcheeraction 50 good (50 bits, \"good\" tag)')
            return

        await self.__twitchUtils.safeSend(ctx, await self.__actionToStr(action))
        self.__timber.log('AddSoundAlertCheerActionCommand', f'Handled !addsoundalertcheeraction command for {ctx.getAuthorName()}:{ctx.getAuthorId()} in {user.getHandle()}')
