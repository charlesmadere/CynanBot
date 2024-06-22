import traceback

import CynanBot.misc.utils as utils
from CynanBot.chatActions.absChatAction import AbsChatAction
from CynanBot.cheerActions.cheerActionBitRequirement import \
    CheerActionBitRequirement
from CynanBot.cheerActions.cheerActionJsonMapperInterface import \
    CheerActionJsonMapperInterface
from CynanBot.cheerActions.cheerActionsRepositoryInterface import \
    CheerActionsRepositoryInterface
from CynanBot.cheerActions.cheerActionStreamStatusRequirement import \
    CheerActionStreamStatusRequirement
from CynanBot.cheerActions.cheerActionsWizardInterface import \
    CheerActionsWizardInterface
from CynanBot.cheerActions.cheerActionType import CheerActionType
from CynanBot.cheerActions.wizards.soundAlertStep import SoundAlertStep
from CynanBot.cheerActions.wizards.soundAlertWizard import SoundAlertWizard
from CynanBot.cheerActions.wizards.stepResult import StepResult
from CynanBot.cheerActions.wizards.timeoutStep import TimeoutStep
from CynanBot.cheerActions.wizards.timeoutWizard import TimeoutWizard
from CynanBot.mostRecentChat.mostRecentChat import MostRecentChat
from CynanBot.timber.timberInterface import TimberInterface
from CynanBot.twitch.configuration.twitchMessage import TwitchMessage
from CynanBot.twitch.twitchUtilsInterface import TwitchUtilsInterface
from CynanBot.users.userInterface import UserInterface


class CheerActionsWizardChatAction(AbsChatAction):

    def __init__(
        self,
        cheerActionJsonMapper: CheerActionJsonMapperInterface,
        cheerActionsRepository: CheerActionsRepositoryInterface,
        cheerActionsWizard: CheerActionsWizardInterface,
        timber: TimberInterface,
        twitchUtils: TwitchUtilsInterface
    ):
        if not isinstance(cheerActionJsonMapper, CheerActionJsonMapperInterface):
            raise TypeError(f'cheerActionJsonMapper argument is malformed: \"{cheerActionJsonMapper}\"')
        elif not isinstance(cheerActionsRepository, CheerActionsRepositoryInterface):
            raise TypeError(f'cheerActionsRepository argument is malformed: \"{cheerActionsRepository}\"')
        elif not isinstance(cheerActionsWizard, CheerActionsWizardInterface):
            raise TypeError(f'cheerActionsWizard argument is malformed: \"{cheerActionsWizard}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(twitchUtils, TwitchUtilsInterface):
            raise TypeError(f'twitchUtils argument is malformed: \"{twitchUtils}\"')

        self.__cheerActionJsonMapper: CheerActionJsonMapperInterface = cheerActionJsonMapper
        self.__cheerActionsRepository: CheerActionsRepositoryInterface = cheerActionsRepository
        self.__cheerActionsWizard: CheerActionsWizardInterface = cheerActionsWizard
        self.__timber: TimberInterface = timber
        self.__twitchUtils: TwitchUtilsInterface = twitchUtils

    async def __configureSoundAlertWizard(
        self,
        content: str,
        wizard: SoundAlertWizard,
        message: TwitchMessage
    ) -> bool:
        channel = message.getChannel()
        steps = wizard.getSteps()
        step = steps.getStep()

        match step:
            case SoundAlertStep.BITS:
                try:
                    bits = int(content)
                    wizard.setBits(bits)
                except Exception as e:
                    self.__timber.log('CheerActionsWizardChatAction', f'Unable to parse/set bits value for Sound Alert wizard ({wizard=}) ({content=}): {e}', e, traceback.format_exc())
                    await self.__twitchUtils.safeSend(channel, f'⚠ The Sound Alert wizard encountered an error, please try again')
                    await self.__cheerActionsWizard.complete(wizard.twitchChannelId)
                    return True

            case SoundAlertStep.TAG:
                try:
                    wizard.setTag(content)
                except Exception as e:
                    self.__timber.log('CheerActionsWizardChatAction', f'Unable to set tag value for Sound Alert wizard ({wizard=}) ({content=}): {e}', e, traceback.format_exc())
                    await self.__twitchUtils.safeSend(channel, f'⚠ The Sound Alert wizard encountered an error, please try again')
                    await self.__cheerActionsWizard.complete(wizard.twitchChannelId)
                    return True

            case _:
                self.__timber.log('CheerActionsWizardChatAction', f'The Sound Alert wizard is in an invalid state ({wizard=})')
                await self.__twitchUtils.safeSend(channel, f'⚠ The Sound Alert wizard is in an invalid state, please try again')
                await self.__cheerActionsWizard.complete(wizard.twitchChannelId)
                return True

        stepResult = steps.stepForward()

        match stepResult:
            case StepResult.DONE:
                await self.__cheerActionsWizard.complete(wizard.twitchChannelId)

                await self.__cheerActionsRepository.addAction(
                    bitRequirement = CheerActionBitRequirement.EXACT,
                    streamStatusRequirement = CheerActionStreamStatusRequirement.ONLINE,
                    actionType = CheerActionType.SOUND_ALERT,
                    amount = wizard.requireBits(),
                    durationSeconds = None,
                    tag = wizard.requireTag(),
                    userId = wizard.twitchChannelId
                )

                self.__timber.log('CheerActionsWizardChatAction', f'Finished configuring Sound Alert wizard ({message.getAuthorId()=}) ({message.getAuthorName()=}) ({message.getTwitchChannelName()=})')
                await self.__twitchUtils.safeSend(channel, f'ⓘ Finished configuring Sound Alert ({wizard.printOut()})')
                return True

            case StepResult.NEXT:
                # this is intentionally empty
                pass

            case _:
                self.__timber.log('CheerActionsWizardChatAction', f'The Sound Alert wizard is in an invalid state ({wizard=})')
                await self.__twitchUtils.safeSend(channel, f'⚠ The Sound Alert wizard is in an invalid state, please try again')
                await self.__cheerActionsWizard.complete(wizard.twitchChannelId)
                return True

        match steps.getStep():
            case SoundAlertStep.BITS:
                self.__timber.log('CheerActionsWizardChatAction', f'The Sound Alert wizard is in an invalid state ({wizard=})')
                await self.__twitchUtils.safeSend(channel, f'⚠ The Sound Alert wizard is in an invalid state, please try again')
                await self.__cheerActionsWizard.complete(wizard.twitchChannelId)
                return True

            case SoundAlertStep.TAG:
                await self.__twitchUtils.safeSend(channel, f'ⓘ Next, please specify the Sound Alert\'s tag. This value must be some text.')
                return True

            case _:
                self.__timber.log('CheerActionsWizardChatAction', f'The Sound Alert wizard is in an invalid state ({wizard=})')
                await self.__twitchUtils.safeSend(channel, f'⚠ The Sound Alert wizard is in an invalid state, please try again')
                await self.__cheerActionsWizard.complete(wizard.twitchChannelId)
                return True

    async def __configureTimeoutWizard(
        self,
        content: str,
        wizard: TimeoutWizard,
        message: TwitchMessage
    ) -> bool:
        channel = message.getChannel()
        steps = wizard.getSteps()
        step = steps.getStep()

        match step:
            case TimeoutStep.BITS:
                try:
                    bits = int(content)
                    wizard.setBits(bits)
                except Exception as e:
                    self.__timber.log('CheerActionsWizardChatAction', f'Unable to parse/set bits value for Timeout wizard ({wizard=}) ({content=}): {e}', e, traceback.format_exc())
                    await self.__twitchUtils.safeSend(channel, f'⚠ The Timeout wizard encountered an error, please try again')
                    await self.__cheerActionsWizard.complete(wizard.twitchChannelId)
                    return True

            case TimeoutStep.DURATION_SECONDS:
                try:
                    durationSeconds = int(content)
                    wizard.setDurationSeconds(durationSeconds)
                except Exception as e:
                    self.__timber.log('CheerActionsWizardChatAction', f'Unable to parse/set durationSeconds value for Timeout wizard ({wizard=}) ({content=}): {e}', e, traceback.format_exc())
                    await self.__twitchUtils.safeSend(channel, f'⚠ The Timeout wizard encountered an error, please try again')
                    await self.__cheerActionsWizard.complete(wizard.twitchChannelId)
                    return True

            case TimeoutStep.STREAM_STATUS:
                try:
                    streamStatus = await self.__cheerActionJsonMapper.requireCheerActionStreamStatusRequirement(content)
                    wizard.setStreamStatus(streamStatus)
                except Exception as e:
                    self.__timber.log('CheerActionsWizardChatAction', f'Unable to parse/set stream status value for Timeout wizard ({wizard=}) ({content=}): {e}', e, traceback.format_exc())
                    await self.__twitchUtils.safeSend(channel, f'⚠ The Timeout wizard encountered an error, please try again')
                    await self.__cheerActionsWizard.complete(wizard.twitchChannelId)
                    return True

            case _:
                self.__timber.log('CheerActionsWizardChatAction', f'The Timeout wizard is in an invalid state ({wizard=})')
                await self.__twitchUtils.safeSend(channel, f'⚠ The Timeout wizard is in an invalid state, please try again')
                await self.__cheerActionsWizard.complete(wizard.twitchChannelId)
                return True

        stepResult = steps.stepForward()

        match stepResult:
            case StepResult.DONE:
                await self.__cheerActionsWizard.complete(wizard.twitchChannelId)

                await self.__cheerActionsRepository.addAction(
                    bitRequirement = CheerActionBitRequirement.EXACT,
                    streamStatusRequirement = wizard.requireStreamStatus(),
                    actionType = CheerActionType.TIMEOUT,
                    amount = wizard.requireBits(),
                    durationSeconds = wizard.requireDurationSeconds(),
                    tag = None,
                    userId = wizard.twitchChannelId
                )

                self.__timber.log('CheerActionsWizardChatAction', f'Finished configuring Timeout wizard ({message.getAuthorId()=}) ({message.getAuthorName()=}) ({message.getTwitchChannelName()=})')
                await self.__twitchUtils.safeSend(channel, f'ⓘ Finished configuring Timeout ({wizard.printOut()})')
                return True

            case StepResult.NEXT:
                # this is intentionally empty
                pass

            case _:
                self.__timber.log('CheerActionsWizardChatAction', f'The Timeout wizard is in an invalid state ({wizard=})')
                await self.__twitchUtils.safeSend(channel, f'⚠ The Timeout wizard is in an invalid state, please try again')
                await self.__cheerActionsWizard.complete(wizard.twitchChannelId)
                return True

        match steps.getStep():
            case TimeoutStep.BITS:
                self.__timber.log('CheerActionsWizardChatAction', f'The Timeout wizard is in an invalid state ({wizard=})')
                await self.__twitchUtils.safeSend(channel, f'⚠ The Timeout wizard is in an invalid state, please try again')
                await self.__cheerActionsWizard.complete(wizard.twitchChannelId)
                return True

            case TimeoutStep.DURATION_SECONDS:
                await self.__twitchUtils.safeSend(channel, f'ⓘ Next, please specify the Timeout\'s duration (in seconds)')
                return True

            case TimeoutStep.STREAM_STATUS:
                streamStatusStrings: list[str] = list()

                for streamStatus in list(CheerActionStreamStatusRequirement):
                    string = await self.__cheerActionJsonMapper.serializeCheerActionStreamStatusRequirement(streamStatus)
                    streamStatusStrings.append(f'\"{string}\"')

                streamStatusString = ', '.join(streamStatusStrings)
                await self.__twitchUtils.safeSend(channel, f'ⓘ Next, please specify the Timeout\'s required stream status. The value must be one of the following: {streamStatusString}.')
                return True

            case _:
                self.__timber.log('CheerActionsWizardChatAction', f'The Timeout wizard is in an invalid state ({wizard=})')
                await self.__twitchUtils.safeSend(channel, f'⚠ The Timeout wizard is in an invalid state, please try again')
                await self.__cheerActionsWizard.complete(wizard.twitchChannelId)
                return True

    async def handleChat(
        self,
        mostRecentChat: MostRecentChat | None,
        message: TwitchMessage,
        user: UserInterface
    ) -> bool:
        content = message.getContent()
        twitchChannelId = await message.getTwitchChannelId()
        wizard = await self.__cheerActionsWizard.get(twitchChannelId)

        if not utils.isValidStr(content) or twitchChannelId != message.getAuthorId() or wizard is None:
            return False

        if isinstance(wizard, SoundAlertWizard):
            return await self.__configureSoundAlertWizard(
                content = content,
                wizard = wizard,
                message = message
            )
        elif isinstance(wizard, TimeoutWizard):
            return await self.__configureTimeoutWizard(
                content = content,
                wizard = wizard,
                message = message
            )
        else:
            self.__timber.log('CheerActionsWizardChatAction', f'Received unknown AbsWizard type: \"{wizard}\" ({message.getAuthorName()=}) ({message.getAuthorName()=}) ({twitchChannelId=}) ({message.getTwitchChannelName()=})')
            return False
