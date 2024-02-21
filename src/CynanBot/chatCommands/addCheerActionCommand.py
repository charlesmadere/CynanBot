from typing import Optional

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
    CheerActionAlreadyExistsException, TimeoutDurationSecondsTooLongException,
    TooManyCheerActionsException)
from CynanBot.timber.timberInterface import TimberInterface
from CynanBot.twitch.configuration.twitchContext import TwitchContext
from CynanBot.twitch.twitchUtilsInterface import TwitchUtilsInterface
from CynanBot.users.userIdsRepositoryInterface import \
    UserIdsRepositoryInterface
from CynanBot.users.usersRepositoryInterface import UsersRepositoryInterface


class AddCheerActionCommand(AbsChatCommand):

    def __init__(
        self,
        administratorProvider: AdministratorProviderInterface,
        cheerActionsRepository: CheerActionsRepositoryInterface,
        timber: TimberInterface,
        twitchUtils: TwitchUtilsInterface,
        userIdsRepository: UserIdsRepositoryInterface,
        usersRepository: UsersRepositoryInterface
    ):
        assert isinstance(administratorProvider, AdministratorProviderInterface), f"malformed {administratorProvider=}"
        assert isinstance(cheerActionsRepository, CheerActionsRepositoryInterface), f"malformed {cheerActionsRepository=}"
        assert isinstance(timber, TimberInterface), f"malformed {timber=}"
        assert isinstance(twitchUtils, TwitchUtilsInterface), f"malformed {twitchUtils=}"
        assert isinstance(userIdsRepository, UserIdsRepositoryInterface), f"malformed {userIdsRepository=}"
        assert isinstance(usersRepository, UsersRepositoryInterface), f"malformed {usersRepository=}"

        self.__administratorProvider: AdministratorProviderInterface = administratorProvider
        self.__cheerActionsRepository: CheerActionsRepositoryInterface = cheerActionsRepository
        self.__timber: TimberInterface = timber
        self.__twitchUtils: TwitchUtilsInterface = twitchUtils
        self.__userIdsRepository: UserIdsRepositoryInterface = userIdsRepository
        self.__usersRepository: UsersRepositoryInterface = usersRepository

    async def __actionToStr(self, action: CheerAction) -> str:
        assert isinstance(action, CheerAction), f"malformed {action=}"

        cheerActionString = f'id={action.getActionId()}, amount={action.getAmount()}, duration={action.getDurationSeconds()}, streamStatus={action.getStreamStatusRequirement()}'
        return f'ⓘ Your new cheer action — {cheerActionString}'

    async def handleChatCommand(self, ctx: TwitchContext):
        user = await self.__usersRepository.getUserAsync(ctx.getTwitchChannelName())
        userId = await self.__userIdsRepository.requireUserId(user.getHandle())
        administrator = await self.__administratorProvider.getAdministratorUserId()

        if userId != ctx.getAuthorId() and administrator != ctx.getAuthorId():
            self.__timber.log('AddCheerActionCommand', f'{ctx.getAuthorName()}:{ctx.getAuthorId()} in {user.getHandle()} tried using this command!')
            return
        elif not user.areCheerActionsEnabled():
            return

        splits = utils.getCleanedSplits(ctx.getMessageContent())
        if len(splits) < 3:
            self.__timber.log('AddCheerActionCommand', f'Less than 2 arguments given by {ctx.getAuthorName()}:{ctx.getAuthorId()} in {user.getHandle()}')
            await self.__twitchUtils.safeSend(ctx, f'⚠ Two arguments are necessary (first bits, then timeout duration in seconds) for the !addcheeraction command. Example: !addcheeraction 50 120 (50 bits, 120 second timeout)')
            return

        bitsString = splits[1]
        bits: Optional[int] = None
        try:
            bits = int(bitsString)
        except Exception as e:
            self.__timber.log('AddCheerActionCommand', f'Failed to parse bitsString (\"{bitsString}\") into bits int: {e}', e, traceback.format_exc())

        durationSecondsString = splits[2]
        durationSeconds: Optional[int] = None
        try:
            durationSeconds = int(durationSecondsString)
        except Exception as e:
            self.__timber.log('AddCheerActionCommand', f'Failed to parse durationSecondsString (\"{durationSecondsString}\") into durationSeconds int: {e}', e, traceback.format_exc())

        if not utils.isValidInt(bits) or not utils.isValidInt(durationSeconds):
            self.__timber.log('AddCheerActionCommand', f'The bitsString value (\"{bitsString}\") or durationSeconds value (\"{durationSeconds}\") given by {ctx.getAuthorName()}:{ctx.getAuthorId()} in {user.getHandle()} failed to parse into an int')
            await self.__twitchUtils.safeSend(ctx, f'⚠ Failed to parse either your bits amount or your duration seconds amount for the !addcheeraction command. Example: !addcheeraction 50 120 (50 bits, 120 second timeout)')
            return
        elif bits < 1 or bits > utils.getIntMaxSafeSize():
            self.__timber.log('AddCheerActionCommand', f'The bitsString value (\"{bitsString}\") given by {ctx.getAuthorName()}:{ctx.getAuthorId()} in {user.getHandle()} is out of bounds: {bitsString}')
            await self.__twitchUtils.safeSend(ctx, f'⚠ Failed to parse either your bits amount or your duration seconds amount for the !addcheeraction command. Example: !addcheeraction 50 120 (50 bits, 120 second timeout)')
            return
        elif durationSeconds < 1 or durationSeconds > 1209600:
            self.__timber.log('AddCheerActionCommand', f'The durationString value (\"{durationSecondsString}\") given by {ctx.getAuthorName()}:{ctx.getAuthorId()} in {user.getHandle()} is out of bounds: {durationSeconds}')
            await self.__twitchUtils.safeSend(ctx, f'⚠ Failed to parse either your bits amount or your duration seconds amount for the !addcheeraction command. Example: !addcheeraction 50 120 (50 bits, 120 second timeout)')
            return

        streamStatus = CheerActionStreamStatusRequirement.ANY
        if len(splits) >= 3:
            streamStatusString = splits[3]
            try:
                streamStatus = CheerActionStreamStatusRequirement.fromStr(streamStatusString)
            except Exception as e:
                self.__timber.log('AddCheerActionCommand', f'The streamStatus value (\"{streamStatusString}\") given by {ctx.getAuthorName()}:{ctx.getAuthorId()} in {user.getHandle()} is malformed/invalid: {e}', e, traceback.format_exc())

        try:
            action = await self.__cheerActionsRepository.addAction(
                bitRequirement = CheerActionBitRequirement.EXACT,
                streamStatusRequirement = streamStatus,
                actionType = CheerActionType.TIMEOUT,
                amount = bits,
                durationSeconds = durationSeconds,
                userId = userId
            )
        except CheerActionAlreadyExistsException as e:
            self.__timber.log('AddCheerActionCommand', f'Failed to add new cheer action for {ctx.getAuthorName()}:{ctx.getAuthorId()} in {user.getHandle()} due to this cheer action already existing: {e}', e, traceback.format_exc())
            await self.__twitchUtils.safeSend(ctx, f'⚠ Failed to add new cheer action as you already have one with these same attributes')
            return
        except TimeoutDurationSecondsTooLongException as e:
            self.__timber.log('AddCheerActionCommand', f'Failed to add new cheer action for {ctx.getAuthorName()}:{ctx.getAuthorId()} in {user.getHandle()} due to the timeout duration seconds being too long: {e}', e, traceback.format_exc())
            await self.__twitchUtils.safeSend(ctx, f'⚠ Failed to add new cheer action as the given timeout duration is too long')
            return
        except TooManyCheerActionsException as e:
            self.__timber.log('AddCheerActionCommand', f'Failed to add new cheer action for {ctx.getAuthorName()}:{ctx.getAuthorId()} in {user.getHandle()} due to this user having the maximum number of cheer actions: {e}', e, traceback.format_exc())
            await self.__twitchUtils.safeSend(ctx, f'⚠ Failed to add new cheer action as you already have the maximum number of cheer actions')
            return
        except Exception as e:
            self.__timber.log('AddCheerActionCommand', f'Failed to add new cheer action for {ctx.getAuthorName()}:{ctx.getAuthorId()} in {user.getHandle()}: {e}', e, traceback.format_exc())
            await self.__twitchUtils.safeSend(ctx, f'⚠ Failed to add new cheer action. Example: !addcheeraction 50 120 (50 bits, 120 second timeout)')
            return

        await self.__twitchUtils.safeSend(ctx, await self.__actionToStr(action))
        self.__timber.log('AddCheerActionCommand', f'Handled !addcheeraction command for {ctx.getAuthorName()}:{ctx.getAuthorId()} in {user.getHandle()}')
