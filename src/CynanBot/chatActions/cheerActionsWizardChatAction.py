import CynanBot.misc.utils as utils
from CynanBot.chatActions.absChatAction import AbsChatAction
from CynanBot.cheerActions.cheerActionsRepositoryInterface import \
    CheerActionsRepositoryInterface
from CynanBot.cheerActions.cheerActionsWizardInterface import \
    CheerActionsWizardInterface
from CynanBot.cheerActions.wizards.soundAlertWizard import SoundAlertWizard
from CynanBot.cheerActions.wizards.timeoutWizard import TimeoutWizard
from CynanBot.mostRecentChat.mostRecentChat import MostRecentChat
from CynanBot.timber.timberInterface import TimberInterface
from CynanBot.twitch.configuration.twitchMessage import TwitchMessage
from CynanBot.twitch.twitchUtilsInterface import TwitchUtilsInterface
from CynanBot.users.userInterface import UserInterface


class CheerActionsWizardChatAction(AbsChatAction):

    def __init__(
        self,
        cheerActionsRepository: CheerActionsRepositoryInterface,
        cheerActionsWizard: CheerActionsWizardInterface,
        timber: TimberInterface,
        twitchUtils: TwitchUtilsInterface
    ):
        if not isinstance(cheerActionsRepository, CheerActionsRepositoryInterface):
            raise TypeError(f'cheerActionsRepository argument is malformed: \"{cheerActionsRepository}\"')
        elif not isinstance(cheerActionsWizard, CheerActionsWizardInterface):
            raise TypeError(f'cheerActionsWizard argument is malformed: \"{cheerActionsWizard}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(twitchUtils, TwitchUtilsInterface):
            raise TypeError(f'twitchUtils argument is malformed: \"{twitchUtils}\"')

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

        # TODO
        return False

    async def __configureTimeoutWizard(
        self,
        content: str,
        wizard: TimeoutWizard,
        message: TwitchMessage
    ) -> bool:
        channel = message.getChannel()
        steps = wizard.getSteps()
        step = steps.getStep()

        # TODO
        return False

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
