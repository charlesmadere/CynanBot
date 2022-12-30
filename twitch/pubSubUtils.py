import asyncio
import queue
from asyncio import AbstractEventLoop
from collections import defaultdict
from queue import SimpleQueue
from typing import Dict, List, Optional

from twitchio import Client
from twitchio.ext import pubsub
from twitchio.ext.pubsub import PubSubPool
from twitchio.ext.pubsub.topics import Topic

import CynanBotCommon.utils as utils
from CynanBotCommon.network.exceptions import GenericNetworkException
from CynanBotCommon.timber.timber import Timber
from CynanBotCommon.twitch.exceptions import (
    TwitchAccessTokenMissingException, TwitchErrorException,
    TwitchJsonException, TwitchRefreshTokenMissingException)
from CynanBotCommon.twitch.twitchTokensRepository import TwitchTokensRepository
from CynanBotCommon.users.userIdsRepository import UserIdsRepository
from CynanBotCommon.users.userInterface import UserInterface
from CynanBotCommon.users.usersRepositoryInterface import \
    UsersRepositoryInterface
from generalSettingsRepository import GeneralSettingsRepository
from twitch.pubSubEntry import PubSubEntry


class PubSubUtils():

    def __init__(
        self,
        eventLoop: AbstractEventLoop,
        client: Client,
        generalSettingsRepository: GeneralSettingsRepository,
        timber: Timber,
        twitchTokensRepository: TwitchTokensRepository,
        userIdsRepository: UserIdsRepository,
        usersRepository: UsersRepositoryInterface,
        maxConnectionsPerTwitchChannel: int = 16,
        queueTimeoutSeconds: int = 3
    ):
        if not isinstance(eventLoop, AbstractEventLoop):
            raise ValueError(f'eventLoop argument is malformed: \"{eventLoop}\"')
        elif not isinstance(client, Client):
            raise ValueError(f'client argument is malformed: \"{client}\"')
        elif not isinstance(generalSettingsRepository, GeneralSettingsRepository):
            raise ValueError(f'generalSettingsRepository argument is malformed: \"{generalSettingsRepository}\"')
        elif not isinstance(timber, Timber):
            raise ValueError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(twitchTokensRepository, TwitchTokensRepository):
            raise ValueError(f'twitchTokensRepository argument is malformed: \"{twitchTokensRepository}\"')
        elif not isinstance(userIdsRepository, UserIdsRepository):
            raise ValueError(f'userIdsRepository argument is malformed: \"{userIdsRepository}\"')
        elif not isinstance(usersRepository, UsersRepositoryInterface):
            raise ValueError(f'usersRepository argument is malformed: \"{usersRepository}\"')
        elif not utils.isValidInt(maxConnectionsPerTwitchChannel):
            raise ValueError(f'maxConnectionsPerTwitchChannel argument is malformed: \"{maxConnectionsPerTwitchChannel}\"')
        elif maxConnectionsPerTwitchChannel < 4 or maxConnectionsPerTwitchChannel >= 128:
            raise ValueError(f'maxConnectionsPerTwitchChannel argument is out of bounds: {maxConnectionsPerTwitchChannel}')
        elif not utils.isValidNum(queueTimeoutSeconds):
            raise ValueError(f'queueTimeoutSeconds argument is malformed: \"{queueTimeoutSeconds}\"')
        elif queueTimeoutSeconds < 1 or queueTimeoutSeconds > 8:
            raise ValueError(f'queueTimeoutSeconds argument is out of bounds: {queueTimeoutSeconds}')

        self.__eventLoop: AbstractEventLoop = eventLoop
        self.__generalSettingsRepository: GeneralSettingsRepository = generalSettingsRepository
        self.__timber: Timber = timber
        self.__twitchTokensRepository: TwitchTokensRepository = twitchTokensRepository
        self.__userIdsRepository: UserIdsRepository = userIdsRepository
        self.__usersRepository: UsersRepositoryInterface = usersRepository
        self.__maxConnectionsPerTwitchChannel: int = maxConnectionsPerTwitchChannel
        self.__queueTimeoutSeconds: int = queueTimeoutSeconds

        self.__isManagingPubSub: bool = False
        self.__isStarted: bool = False
        self.__pubSubEntries: Dict[str, SimpleQueue[Topic]] = defaultdict(lambda: SimpleQueue())

        self.__pubSubPool: PubSubPool = PubSubPool(
            client = client,
            max_pool_size = maxConnectionsPerTwitchChannel * 4,
            max_connection_topics = maxConnectionsPerTwitchChannel * 16
        )

    async def __getSubscribeReadyPubSubEntries(self) -> Optional[List[PubSubEntry]]:
        twitchHandles = await self.__twitchTokensRepository.getExpiringTwitchHandles()
        users: Optional[List[UserInterface]] = None

        if twitchHandles is None:
            # if twitchHandles is None, then we must do a full validate and refresh
            users = await self.__usersRepository.getUsersAsync()
        elif len(twitchHandles) == 0:
            # if twitchHandles is empty, then there is no need to do a validate or refresh of anyone
            return None
        else:
            # if twitchHandles has entries, then we will validate and refresh those specific users
            users = list()

            for twitchHandle in twitchHandles:
                users.append(await self.__usersRepository.getUserAsync(twitchHandle))

        usersWithTwitchTokens: List[UserInterface] = list()

        for user in users:
            if await self.__twitchTokensRepository.hasAccessToken(user.getHandle()):
                usersWithTwitchTokens.append(user)

        if not utils.hasItems(usersWithTwitchTokens):
            return None

        usersAndTwitchTokens: Dict[UserInterface, str] = dict()

        for user in usersWithTwitchTokens:
            try:
                await self.__twitchTokensRepository.validateAndRefreshAccessToken(
                    twitchHandle = user.getHandle()
                )

                usersAndTwitchTokens[user] = await self.__twitchTokensRepository.getAccessToken(user.getHandle())
            except (GenericNetworkException, TwitchAccessTokenMissingException, TwitchErrorException, TwitchJsonException, TwitchRefreshTokenMissingException) as e:
                # if we run into one of the Twitch errors, that most likely means that this user changed their password
                self.__timber.log('PubSubUtils', f'Failed to validate and refresh access Twitch tokens for \"{user.getHandle()}\": {e}', e)

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

    def startPubSub(self):
        if self.__isStarted:
            self.__timber.log('PubSubUtils', 'Not starting PubSub as it has already been started')
            return

        self.__isStarted = True
        self.__timber.log('PubSubUtils', 'Starting PubSub...')
        self.__eventLoop.create_task(self.__startPubSubUpdateLoop())

    async def __startPubSubUpdateLoop(self):
        while True:
            self.__timber.log('PubSubUtils', 'Refreshing...')

            if self.__isManagingPubSub:
                self.__timber('PubSubUtils', f'Unable to update PubSub subscriptions because it is currently in progress!')
            else:
                self.__isManagingPubSub = True

                try:
                    await self.__updatePubSubSubscriptions()
                except Exception as e:
                    self.__timber.log('PubSubUtils', f'Encountered Exception when attempting to update PubSub subscriptions: {e}', e)

                self.__isManagingPubSub = False

            generalSettings = await self.__generalSettingsRepository.getAllAsync()
            await asyncio.sleep(generalSettings.getRefreshPubSubTokensSeconds())

    async def __updatePubSubSubscriptions(self):
        pubSubTopicsToAdd: List[Topic] = list()
        pubSubTopicsToRemove: List[Topic] = list()
        newPubSubEntries = await self.__getSubscribeReadyPubSubEntries()

        if utils.hasItems(newPubSubEntries):
            for newPubSubEntry in newPubSubEntries:
                pubSubTopicsToAdd.append(newPubSubEntry.getTopic())
                self.__pubSubEntries[newPubSubEntry.getUserName()].put(newPubSubEntry.getTopic())

        for userName, topicQueue in self.__pubSubEntries.items():
            try:
                while topicQueue.qsize() > self.__maxConnectionsPerTwitchChannel:
                    pubSubTopicsToRemove.append(topicQueue.get(block = True, timeout = self.__queueTimeoutSeconds))
            except queue.Empty as e:
                self.__timber.log('PubSubUtils', f'Encountered queue.Empty when attempting to fetch PubSub topic from \"{userName}\"\'s queue: {e}', e)

        if utils.hasItems(pubSubTopicsToAdd):
            self.__timber.log('PubSubUtils', f'Subscribing to {len(newPubSubEntries)} PubSub user(s)...')

            try:
                await self.__pubSubPool.subscribe_topics(pubSubTopicsToAdd)
            except Exception as e:
                self.__timber.log('PubSubUtils', f'Encountered Exception when attempting to subscribe to {len(pubSubTopicsToAdd)} topic(s): {e}', e)

            self.__timber.log('PubSubUtils', f'Finished subscribing to {len(newPubSubEntries)} PubSub user(s)')

        if utils.hasItems(pubSubTopicsToRemove):
            self.__timber.log('PubSubUtils', f'Unsubscribing from {len(pubSubTopicsToRemove)} PubSub user(s)...')

            try:
                await self.__pubSubPool.unsubscribe_topics(pubSubTopicsToRemove)
            except Exception as e:
                self.__timber.log('PubSubUtils', f'Encountered Exception when attempting to unsubscribe from {len(pubSubTopicsToRemove)} topic(s): {e}', e)

            self.__timber.log('PubSubUtils', f'Finished unsubscribing from {len(pubSubTopicsToRemove)} PubSub user(s)')
