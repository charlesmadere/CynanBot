import traceback

from .absChatAction import AbsChatAction
from ..cheerActions.beanChanceCheerAction import BeanChanceCheerAction
from ..cheerActions.cheerActionJsonMapperInterface import CheerActionJsonMapperInterface
from ..cheerActions.cheerActionStreamStatusRequirement import CheerActionStreamStatusRequirement
from ..cheerActions.cheerActionsRepositoryInterface import CheerActionsRepositoryInterface
from ..cheerActions.cheerActionsWizardInterface import CheerActionsWizardInterface
from ..cheerActions.soundAlertCheerAction import SoundAlertCheerAction
from ..cheerActions.timeoutCheerAction import TimeoutCheerAction
from ..cheerActions.wizards.beanChanceStep import BeanChanceStep
from ..cheerActions.wizards.beanChanceWizard import BeanChanceWizard
from ..cheerActions.wizards.crowdControl.crowdControlWizard import CrowdControlWizard
from ..cheerActions.wizards.gameShuffle.gameShuffleWizard import GameShuffleWizard
from ..cheerActions.wizards.soundAlertStep import SoundAlertStep
from ..cheerActions.wizards.soundAlertWizard import SoundAlertWizard
from ..cheerActions.wizards.stepResult import StepResult
from ..cheerActions.wizards.timeoutStep import TimeoutStep
from ..cheerActions.wizards.timeoutWizard import TimeoutWizard
from ..misc import utils as utils
from ..mostRecentChat.mostRecentChat import MostRecentChat
from ..timber.timberInterface import TimberInterface
from ..twitch.configuration.twitchMessage import TwitchMessage
from ..twitch.twitchUtilsInterface import TwitchUtilsInterface
from ..users.userInterface import UserInterface


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

    async def __configureBeanChanceWizard(
        self,
        content: str,
        wizard: BeanChanceWizard,
        message: TwitchMessage
    ) -> bool:
        channel = message.getChannel()
        steps = wizard.getSteps()
        step = steps.getStep()

        match step:
            case BeanChanceStep.BITS:
                try:
                    bits = int(content)
                    wizard.setBits(bits)
                except Exception as e:
                    self.__timber.log('CheerActionsWizardChatAction', f'Unable to parse/set bits value for Bean Chance wizard ({wizard=}) ({content=}): {e}', e, traceback.format_exc())
                    await self.__twitchUtils.safeSend(channel, f'⚠ The Bean Chance wizard encountered an error, please try again')
                    await self.__cheerActionsWizard.complete(wizard.twitchChannelId)
                    return True

            case BeanChanceStep.RANDOM_CHANCE:
                try:
                    randomChance = int(content)
                    wizard.setRandomChance(randomChance)
                except Exception as e:
                    self.__timber.log('CheerActionsWizardChatAction', f'Unable to parse/set randomChance value for Bean Chance wizard ({wizard=}) ({content=}): {e}', e, traceback.format_exc())
                    await self.__twitchUtils.safeSend(channel, f'⚠ The Bean Chance wizard encountered an error, please try again')
                    await self.__cheerActionsWizard.complete(wizard.twitchChannelId)
                    return True

            case _:
                self.__timber.log('CheerActionsWizardChatAction', f'The Bean Chance wizard is in an invalid state ({wizard=})')
                await self.__twitchUtils.safeSend(channel, f'⚠ The Bean Chance wizard is in an invalid state, please try again')
                await self.__cheerActionsWizard.complete(wizard.twitchChannelId)
                return True

        stepResult = steps.stepForward()

        match stepResult:
            case StepResult.DONE:
                await self.__cheerActionsWizard.complete(wizard.twitchChannelId)

                await self.__cheerActionsRepository.setAction(BeanChanceCheerAction(
                    isEnabled = True,
                    streamStatusRequirement = CheerActionStreamStatusRequirement.ONLINE,
                    bits = wizard.requireBits(),
                    randomChance = wizard.requireRandomChance(),
                    twitchChannelId = wizard.twitchChannelId
                ))

                self.__timber.log('CheerActionsWizardChatAction', f'Finished configuring Bean Chance wizard ({message.getAuthorId()=}) ({message.getAuthorName()=}) ({message.getTwitchChannelName()=})')
                await self.__twitchUtils.safeSend(channel, f'ⓘ Finished configuring Bean Chance ({wizard.printOut()})')
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
            case BeanChanceStep.BITS:
                self.__timber.log('CheerActionsWizardChatAction', f'The Bean Chance wizard is in an invalid state ({wizard=})')
                await self.__twitchUtils.safeSend(channel, f'⚠ The Bean Chance wizard is in an invalid state, please try again')
                await self.__cheerActionsWizard.complete(wizard.twitchChannelId)
                return True

            case BeanChanceStep.RANDOM_CHANCE:
                await self.__twitchUtils.safeSend(channel, f'ⓘ Next, please specify the Bean Chance\'s random chance. This value must be an integer from 0 to 100 (decimals aren\'t allowed).')
                return True

            case _:
                self.__timber.log('CheerActionsWizardChatAction', f'The Bean Chance wizard is in an invalid state ({wizard=})')
                await self.__twitchUtils.safeSend(channel, f'⚠ The Bean Chance wizard is in an invalid state, please try again')
                await self.__cheerActionsWizard.complete(wizard.twitchChannelId)
                return True

    async def __configureCrowdControlWizard(
        self,
        content: str,
        wizard: CrowdControlWizard,
        message: TwitchMessage
    ) -> bool:
        # TODO
        return True

    async def __configureGameShuffleWizard(
        self,
        content: str,
        wizard: GameShuffleWizard,
        message: TwitchMessage
    ) -> bool:
        # TODO
        return True

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

            case SoundAlertStep.DIRECTORY:
                try:
                    wizard.setDirectory(content)
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

                await self.__cheerActionsRepository.setAction(SoundAlertCheerAction(
                    isEnabled = True,
                    streamStatusRequirement = CheerActionStreamStatusRequirement.ONLINE,
                    bits = wizard.requireBits(),
                    directory = wizard.requireDirectory(),
                    twitchChannelId = wizard.twitchChannelId
                ))

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

            case SoundAlertStep.DIRECTORY:
                await self.__twitchUtils.safeSend(channel, f'ⓘ Next, please specify the Sound Alert\'s directory. This value must be text.')
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

                await self.__cheerActionsRepository.setAction(TimeoutCheerAction(
                    isEnabled = True,
                    streamStatusRequirement = wizard.requireStreamStatus(),
                    bits = wizard.requireBits(),
                    durationSeconds = wizard.requireDurationSeconds(),
                    twitchChannelId = wizard.twitchChannelId
                ))

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

        if isinstance(wizard, BeanChanceWizard):
            return await self.__configureBeanChanceWizard(
                content = content,
                wizard = wizard,
                message = message
            )

        elif isinstance(wizard, CrowdControlWizard):
            return await self.__configureCrowdControlWizard(
                content = content,
                wizard = wizard,
                message = message
            )

        elif isinstance(wizard, GameShuffleWizard):
            return await self.__configureGameShuffleWizard(
                content = content,
                wizard = wizard,
                message = message
            )

        elif isinstance(wizard, SoundAlertWizard):
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
