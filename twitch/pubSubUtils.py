import asyncio
import queue
import traceback
from collections import defaultdict
from datetime import datetime, timedelta, timezone
from queue import SimpleQueue
from typing import Dict, List, Optional

from twitchio import Client
from twitchio.ext import pubsub
from twitchio.ext.pubsub import PubSubPool
from twitchio.ext.pubsub.models import PubSubError
from twitchio.ext.pubsub.topics import Topic

import CynanBotCommon.utils as utils
from CynanBotCommon.backgroundTaskHelper import BackgroundTaskHelper
from CynanBotCommon.network.exceptions import GenericNetworkException
from CynanBotCommon.timber.timber import Timber
from CynanBotCommon.twitch.exceptions import (
    TwitchAccessTokenMissingException, TwitchErrorException,
    TwitchJsonException, TwitchPasswordChangedException,
    TwitchRefreshTokenMissingException)
from CynanBotCommon.twitch.twitchTokensRepositoryInterface import \
    TwitchTokensRepositoryInterface
from CynanBotCommon.users.userIdsRepository import UserIdsRepository
from CynanBotCommon.users.userInterface import UserInterface
from CynanBotCommon.users.usersRepositoryInterface import \
    UsersRepositoryInterface
from generalSettingsRepository import GeneralSettingsRepository
from twitch.pubSub.cynanBotPubSubPool import CynanBotPubSubPool
from twitch.pubSub.pubSubReconnectListener import PubSubReconnectListener
from twitch.pubSubEntry import PubSubEntry


class PubSubUtils(PubSubReconnectListener):

    def __init__(
        self,
        backgroundTaskHelper: BackgroundTaskHelper,
        client: Client,
        generalSettingsRepository: GeneralSettingsRepository,
        timber: Timber,
        twitchTokensRepositoryInterface: TwitchTokensRepositoryInterface,
        userIdsRepository: UserIdsRepository,
        usersRepositoryInterface: UsersRepositoryInterface,
        maxConnectionsPerTwitchChannel: int = 5,
        maxPubSubConnectionTopics: int = utils.getIntMaxSafeSize(),
        maxPubSubPoolSize: int = utils.getIntMaxSafeSize(),
        queueTimeoutSeconds: int = 3,
        pubSubReconnectCooldown: timedelta = timedelta(minutes = 30),
        timeZone: timezone = timezone.utc
    ):
        if not isinstance(backgroundTaskHelper, BackgroundTaskHelper):
            raise ValueError(f'backgroundTaskHelper argument is malformed: \"{backgroundTaskHelper}\"')
        elif not isinstance(client, Client):
            raise ValueError(f'client argument is malformed: \"{client}\"')
        elif not isinstance(generalSettingsRepository, GeneralSettingsRepository):
            raise ValueError(f'generalSettingsRepository argument is malformed: \"{generalSettingsRepository}\"')
        elif not isinstance(timber, Timber):
            raise ValueError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(twitchTokensRepositoryInterface, TwitchTokensRepositoryInterface):
            raise ValueError(f'twitchTokensRepositoryInterface argument is malformed: \"{twitchTokensRepositoryInterface}\"')
        elif not isinstance(userIdsRepository, UserIdsRepository):
            raise ValueError(f'userIdsRepository argument is malformed: \"{userIdsRepository}\"')
        elif not isinstance(usersRepositoryInterface, UsersRepositoryInterface):
            raise ValueError(f'usersRepositoryInterface argument is malformed: \"{usersRepositoryInterface}\"')
        elif not utils.isValidInt(maxConnectionsPerTwitchChannel):
            raise ValueError(f'maxConnectionsPerTwitchChannel argument is malformed: \"{maxConnectionsPerTwitchChannel}\"')
        elif maxConnectionsPerTwitchChannel < 4 or maxConnectionsPerTwitchChannel > utils.getIntMaxSafeSize():
            raise ValueError(f'maxConnectionsPerTwitchChannel argument is out of bounds: {maxConnectionsPerTwitchChannel}')
        elif not utils.isValidInt(maxPubSubConnectionTopics):
            raise ValueError(f'maxPubSubConnectionTopics argument is malformed: \"{maxPubSubConnectionTopics}\"')
        elif maxPubSubConnectionTopics < 32 or maxPubSubConnectionTopics > utils.getIntMaxSafeSize():
            raise ValueError(f'maxPubSubConnectionTopics argument is out of bounds: {maxPubSubConnectionTopics}')
        elif not utils.isValidInt(maxPubSubPoolSize):
            raise ValueError(f'maxPubSubPoolSize argument is malformed: \"{maxPubSubPoolSize}\"')
        elif maxPubSubPoolSize < 16 or maxPubSubPoolSize > utils.getIntMaxSafeSize():
            raise ValueError(f'maxPubSubPoolSize argument is out of bounds: {maxPubSubPoolSize}')
        elif not utils.isValidNum(queueTimeoutSeconds):
            raise ValueError(f'queueTimeoutSeconds argument is malformed: \"{queueTimeoutSeconds}\"')
        elif queueTimeoutSeconds < 1 or queueTimeoutSeconds > 8:
            raise ValueError(f'queueTimeoutSeconds argument is out of bounds: {queueTimeoutSeconds}')
        elif not isinstance(pubSubReconnectCooldown, timedelta):
            raise ValueError(f'pubSubReconnectCooldown argument is malformed: \"{pubSubReconnectCooldown}\"')
        elif not isinstance(timeZone, timezone):
            raise ValueError(f'timeZone argument is malformed: \"{timeZone}\"')

        self.__backgroundTaskHelper: BackgroundTaskHelper = backgroundTaskHelper
        self.__generalSettingsRepository: GeneralSettingsRepository = generalSettingsRepository
        self.__timber: Timber = timber
        self.__twitchTokensRepositoryInterface: TwitchTokensRepositoryInterface = twitchTokensRepositoryInterface
        self.__userIdsRepository: UserIdsRepository = userIdsRepository
        self.__usersRepositoryInterface: UsersRepositoryInterface = usersRepositoryInterface
        self.__maxConnectionsPerTwitchChannel: int = maxConnectionsPerTwitchChannel
        self.__queueTimeoutSeconds: int = queueTimeoutSeconds
        self.__pubSubReconnectCooldown: timedelta = pubSubReconnectCooldown
        self.__timeZone: timezone = timeZone

        self.__isManagingPubSub: bool = False
        self.__isStarted: bool = False
        self.__pubSubEntries: Dict[str, SimpleQueue[Topic]] = defaultdict(lambda: SimpleQueue())
        self.__lastPubSubReconnect: datetime = datetime.now(timeZone)

        self.__pubSubPool: PubSubPool = CynanBotPubSubPool(
            client = client,
            maxConnectionTopics = maxPubSubConnectionTopics,
            maxPoolSize = maxPubSubPoolSize,
            pubSubReconnectListener = self,
            timber = timber
        )

    async def __addPubSubSubscriptions(self, topicsToAdd: Optional[List[Topic]]):
        if not utils.hasItems(topicsToAdd):
            return

        self.__timber.log('PubSubUtils', f'Subscribing to {len(topicsToAdd)} PubSub topic(s)...')

        try:
            await self.__pubSubPool.subscribe_topics(topicsToAdd)
            self.__timber.log('PubSubUtils', f'Finished subscribing to {len(topicsToAdd)} PubSub topic(s)')
        except PubSubError as e:
            self.__timber.log('PubSubUtils', f'Encountered PubSubError when attempting to subscribe to {len(topicsToAdd)} topic(s): {e}', e, traceback.format_exc())
        except Exception as e:
            self.__timber.log('PubSubUtils', f'Encountered Exception when attempting to subscribe to {len(topicsToAdd)} topic(s): {e}', e, traceback.format_exc())

    async def forceFullRefresh(self):
        self.__timber.log('PubSubUtils', f'Performing a full forced refresh of all PubSub connections...')
        await self.__refresh(forceFullRefresh = True)
        self.__timber.log('PubSubUtils', f'Finished performing full forced refresh of all PubSub connections')

    async def __getSubscribeReadyPubSubEntries(self, forceFullRefresh: bool) -> Optional[List[PubSubEntry]]:
        if not utils.isValidBool(forceFullRefresh):
            raise ValueError(f'forceFullRefresh argument is malformed: \"{forceFullRefresh}\"')

        twitchHandles: Optional[List[str]] = None

        if not forceFullRefresh:
            twitchHandles = await self.__twitchTokensRepositoryInterface.getExpiringTwitchChannels()

        users: Optional[List[UserInterface]] = None

        if twitchHandles is None:
            # if twitchHandles is None, then we must do a full validate and refresh
            users = await self.__usersRepositoryInterface.getUsersAsync()
        elif len(twitchHandles) == 0:
            # if twitchHandles is empty, then there is no need to do a validate or refresh of anyone
            return None
        else:
            # if twitchHandles has entries, then we will validate and refresh those specific users
            users = list()

            for twitchHandle in twitchHandles:
                users.append(await self.__usersRepositoryInterface.getUserAsync(twitchHandle))

        usersWithTwitchTokens: List[UserInterface] = list()

        for user in users:
            if user.isEnabled() and await self.__twitchTokensRepositoryInterface.hasAccessToken(user.getHandle()):
                usersWithTwitchTokens.append(user)

        if not utils.hasItems(usersWithTwitchTokens):
            return None

        usersAndTwitchTokens: Dict[UserInterface, str] = dict()

        for user in usersWithTwitchTokens:
            try:
                await self.__twitchTokensRepositoryInterface.validateAndRefreshAccessToken(user.getHandle())
                usersAndTwitchTokens[user] = await self.__twitchTokensRepositoryInterface.getAccessToken(user.getHandle())
            except GenericNetworkException as e:
                self.__timber.log('PubSubUtils', f'Failed to validate and refresh Twitch tokens for \"{user.getHandle()}\" due to generic network error: {e}', e, traceback.format_exc())
            except (TwitchAccessTokenMissingException, TwitchErrorException, TwitchJsonException, TwitchPasswordChangedException, TwitchRefreshTokenMissingException) as e:
                # if we run into one of the Twitch errors, that most likely means that this user changed their password
                self.__timber.log('PubSubUtils', f'Failed to validate and refresh Twitch tokens for \"{user.getHandle()}\": {e}', e, traceback.format_exc())

        pubSubEntries: List[PubSubEntry] = list()

        for user, twitchAccessToken in usersAndTwitchTokens.items():
            userId = await self.__userIdsRepository.fetchUserIdAsInt(
                userName = user.getHandle(),
                twitchAccessToken = twitchAccessToken
            )

            pubSubEntries.append(PubSubEntry(
                userId = userId,
                userName = user.getHandle().lower(),
                topic = pubsub.channel_points(twitchAccessToken)[userId]
            ))

        return pubSubEntries

    async def onPubSubReconnect(self, topics: Optional[List[Topic]]) -> List[Topic]:
        self.__timber.log('PubSubUtils', f'onPubSubReconnect(): (topics=\"{topics}\")')

        now = datetime.now(self.__timeZone)
        if now <= self.__lastPubSubReconnect + self.__pubSubReconnectCooldown:
            self.__timber.log('PubSubUtils', f'Not performing full PubSub reconnect logic as this new reconnect attempt is within the previous reconnect\'s cooldown: {topics}')
            return topics

        self.__lastPubSubReconnect = now

        for userName, topicQueue in self.__pubSubEntries.items():
            while not topicQueue.empty():
                try:
                    topicQueue.get(block = True, timeout = self.__queueTimeoutSeconds)
                except queue.Empty as e:
                    self.__timber.log('PubSubUtils', f'Encountered queue.Empty when attempting to fetch PubSub topic from \"{userName}\"\'s queue: {e}', e)

        newPubSubEntries = await self.__getSubscribeReadyPubSubEntries(forceFullRefresh = True)
        topicsToAdd: List[Topic] = list()

        for newPubSubEntry in newPubSubEntries:
            try:
                self.__pubSubEntries[newPubSubEntry.getUserName()].put(newPubSubEntry.getTopic(), block = True, timeout = self.__queueTimeoutSeconds)
                topicsToAdd.append(newPubSubEntry.getTopic())
            except queue.Full as e:
                self.__timber.log('PubSubUtils', f'Encountered queue.Full when attempting to add new PubSub topic to \"{userName}\"\'s queue: {e}', e)

        self.__timber.log('PubSubUtils', f'Determined new list of PubSub topics (len={len(topicsToAdd)}): {topicsToAdd}')
        return topicsToAdd

    async def __removePubSubSubscriptions(self, topicsToRemove: Optional[List[Topic]]):
        if not utils.hasItems(topicsToRemove):
            return

        self.__timber.log('PubSubUtils', f'Unsubscribing from {len(topicsToRemove)} PubSub topic(s)...')

        try:
            await self.__pubSubPool.unsubscribe_topics(topicsToRemove)
            self.__timber.log('PubSubUtils', f'Finished unsubscribing from {len(topicsToRemove)} PubSub topic(s)')
        except PubSubError as e:
            self.__timber.log('PubSubUtils', f'Encountered PubSubError when attempting to unsubscribe from {len(topicsToRemove)} topic(s): {e}', e, traceback.format_exc())
        except Exception as e:
            self.__timber.log('PubSubUtils', f'Encountered Exception when attempting to unsubscribe from {len(topicsToRemove)} topic(s): {e}', e, traceback.format_exc())

    async def __refresh(self, forceFullRefresh: bool):
        if not utils.isValidBool(forceFullRefresh):
            raise ValueError(f'forceFullRefresh argument is malformed: \"{forceFullRefresh}\"')

        self.__timber.log('PubSubUtils', f'Refreshing... (forceFullRefresh={forceFullRefresh})')

        if self.__isManagingPubSub:
            self.__timber('PubSubUtils', f'Unable to update PubSub subscriptions because it is currently in progress!')
            return

        self.__isManagingPubSub = True

        try:
            await self.__updatePubSubSubscriptions(forceFullRefresh)
        except Exception as e:
            self.__timber.log('PubSubUtils', f'Encountered Exception when attempting to update PubSub subscriptions: {e}', e, traceback.format_exc())

        self.__isManagingPubSub = False

    def startPubSub(self):
        if self.__isStarted:
            self.__timber.log('PubSubUtils', 'Not starting PubSub as it has already been started')
            return

        self.__isStarted = True
        self.__timber.log('PubSubUtils', 'Starting PubSub...')
        self.__backgroundTaskHelper.createTask(self.__startPubSubUpdateLoop())

    async def __startPubSubUpdateLoop(self):
        while True:
            await self.__refresh(forceFullRefresh = False)

            generalSettings = await self.__generalSettingsRepository.getAllAsync()
            await asyncio.sleep(generalSettings.getRefreshPubSubTokensSeconds())

    async def __updatePubSubSubscriptions(self, forceFullRefresh: bool):
        if not utils.isValidBool(forceFullRefresh):
            raise ValueError(f'forceFullRefresh argument is malformed: \"{forceFullRefresh}\"')

        newPubSubEntries = await self.__getSubscribeReadyPubSubEntries(forceFullRefresh)
        topicsToAdd: List[Topic] = list()
        topicsToRemove: List[Topic] = list()

        if utils.hasItems(newPubSubEntries):
            for newPubSubEntry in newPubSubEntries:
                try:
                    self.__pubSubEntries[newPubSubEntry.getUserName()].put(newPubSubEntry.getTopic(), block = True, timeout = self.__queueTimeoutSeconds)
                    topicsToAdd.append(newPubSubEntry.getTopic())
                except queue.Full as e:
                    self.__timber.log('PubSubUtils', f'Encountered queue.Full when attempting to add new PubSub topic to \"{userName}\"\'s queue: {e}', e)

        for userName, topicQueue in self.__pubSubEntries.items():
            try:
                while topicQueue.qsize() > self.__maxConnectionsPerTwitchChannel:
                    topicsToRemove.append(topicQueue.get(block = True, timeout = self.__queueTimeoutSeconds))
            except queue.Empty as e:
                self.__timber.log('PubSubUtils', f'Encountered queue.Empty when attempting to fetch PubSub topic from \"{userName}\"\'s queue: {e}', e)

        await self.__addPubSubSubscriptions(topicsToAdd)
        await self.__removePubSubSubscriptions(topicsToRemove)
