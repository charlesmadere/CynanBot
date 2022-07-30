import asyncio
from asyncio import AbstractEventLoop
from collections import defaultdict
from queue import SimpleQueue
from typing import Dict, List

import CynanBotCommon.utils as utils
from authRepository import AuthRepository
from CynanBotCommon.timber.timber import Timber
from CynanBotCommon.twitch.twitchTokensRepository import (
    TwitchAccessTokenMissingException, TwitchExpiresInMissingException,
    TwitchJsonException, TwitchNetworkException,
    TwitchRefreshTokenMissingException, TwitchTokensRepository)
from CynanBotCommon.userIdsRepository import UserIdsRepository
from generalSettingsRepository import GeneralSettingsRepository
from twitchio import Client
from twitchio.ext import pubsub
from twitchio.ext.pubsub import PubSubPool
from twitchio.ext.pubsub.topics import Topic
from users.user import User
from users.usersRepository import UsersRepository

from twitch.pubSubEntry import PubSubEntry


class PubSubUtils():

    def __init__(
        self,
        eventLoop: AbstractEventLoop,
        authRepository: AuthRepository,
        client: Client,
        generalSettingsRepository: GeneralSettingsRepository,
        timber: Timber,
        twitchTokensRepository: TwitchTokensRepository,
        userIdsRepository: UserIdsRepository,
        usersRepository: UsersRepository,
        maxConnectionsPerTwitchChannel: int = 8
    ):
        if eventLoop is None:
            raise ValueError(f'eventLoop argument is malformed: \"{eventLoop}\"')
        elif authRepository is None:
            raise ValueError(f'authRepository argument is malformed: \"{authRepository}\"')
        elif client is None:
            raise ValueError(f'client argument is malformed: \"{client}\"')
        elif generalSettingsRepository is None:
            raise ValueError(f'generalSettingsRepository argument is malformed: \"{generalSettingsRepository}\"')
        elif timber is None:
            raise ValueError(f'timber argument is malformed: \"{timber}\"')
        elif twitchTokensRepository is None:
            raise ValueError(f'twitchTokensRepository argument is malformed: \"{twitchTokensRepository}\"')
        elif userIdsRepository is None:
            raise ValueError(f'userIdsRepository argument is malformed: \"{userIdsRepository}\"')
        elif usersRepository is None:
            raise ValueError(f'usersRepository argument is malformed: \"{usersRepository}\"')
        elif not utils.isValidNum(maxConnectionsPerTwitchChannel):
            raise ValueError(f'maxConnectionsPerTwitchChannel argument is malformed: \"{maxConnectionsPerTwitchChannel}\"')
        elif maxConnectionsPerTwitchChannel < 2 or maxConnectionsPerTwitchChannel > 16:
            raise ValueError(f'maxConnectionsPerTwitchChannel argument is out of bounds: {maxConnectionsPerTwitchChannel}')

        self.__eventLoop: AbstractEventLoop = eventLoop
        self.__authRepository: AuthRepository = authRepository
        self.__generalSettingsRepository: GeneralSettingsRepository = generalSettingsRepository
        self.__timber: Timber = timber
        self.__twitchTokensRepository: TwitchTokensRepository = twitchTokensRepository
        self.__userIdsRepository: UserIdsRepository = userIdsRepository
        self.__usersRepository: UsersRepository = usersRepository

        self.__isManagingPubSub: bool = False
        self.__isStarted: bool = False
        self.__pubSubEntries: Dict[str, SimpleQueue[Topic]] = defaultdict(lambda: SimpleQueue())
        self.__maxConnectionsPerTwitchChannel: int = maxConnectionsPerTwitchChannel

        self.__pubSubPool: PubSubPool = PubSubPool(
            client = client,
            max_pool_size = max(32, maxConnectionsPerTwitchChannel * 4),
            max_connection_topics = max(128, maxConnectionsPerTwitchChannel * 16)
        )

    async def __getSubscribeReadyPubSubEntries(self) -> List[PubSubEntry]:
        twitchHandles = await self.__twitchTokensRepository.getExpiringTwitchHandles()
        authSnapshot = await self.__authRepository.getAllAsync()
        users: List[User] = None

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

        usersAndTwitchTokens: Dict[User, str] = dict()

        for user in users:
            twitchAccessToken = await self.__twitchTokensRepository.getAccessToken(user.getHandle())

            if utils.isValidStr(twitchAccessToken):
                usersAndTwitchTokens[user] = twitchAccessToken

        if not utils.hasItems(usersAndTwitchTokens):
            return None

        usersToRemove: List[User] = list()

        for user in usersAndTwitchTokens:
            try:
                await self.__twitchTokensRepository.validateAndRefreshAccessToken(
                    twitchClientId = authSnapshot.requireTwitchClientId(),
                    twitchClientSecret = authSnapshot.requireTwitchClientSecret(),
                    twitchHandle = user.getHandle()
                )

                usersAndTwitchTokens[user] = await self.__twitchTokensRepository.getAccessToken(user.getHandle())
            except (TwitchAccessTokenMissingException, TwitchExpiresInMissingException, TwitchJsonException, TwitchNetworkException, TwitchRefreshTokenMissingException) as e:
                # if we run into this error, that most likely means that this user changed
                # their password
                usersToRemove.append(user)
                self.__timber.log('CynanBot', f'Failed to validate and refresh access Twitch token for {user.getHandle()}: {e}')

        if utils.hasItems(usersToRemove):
            for user in usersToRemove:
                del usersAndTwitchTokens[user]

        pubSubEntries: List[PubSubEntry] = list()

        for user in usersAndTwitchTokens:
            twitchAccessToken = usersAndTwitchTokens[user]

            userId = await self.__userIdsRepository.fetchUserIdAsInt(
                userName = user.getHandle(),
                twitchAccessToken = twitchAccessToken,
                twitchClientId = authSnapshot.requireTwitchClientId()
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
            await self.__updatePubSubSubscriptions()
            generalSettings = await self.__generalSettingsRepository.getAllAsync()
            await asyncio.sleep(generalSettings.getRefreshPubSubTokensSeconds())
            self.__timber.log('PubSubUtils', 'Refreshing...')

    async def __updatePubSubSubscriptions(self):
        if self.__isManagingPubSub:
            self.__timber('PubSubUtils', f'Unable to update PubSub subscriptions because it is currently working!')
            return

        self.__isManagingPubSub = True

        pubSubTopicsToAdd: List[Topic] = list()
        pubSubTopicsToRemove: List[Topic] = list()
        newPubSubEntries = await self.__getSubscribeReadyPubSubEntries()

        if utils.hasItems(newPubSubEntries):
            for newPubSubEntry in newPubSubEntries:
                pubSubTopicsToAdd.append(newPubSubEntry.getTopic())
                self.__pubSubEntries[newPubSubEntry.getUserName()].put(newPubSubEntry.getTopic())

        if utils.hasItems(self.__pubSubEntries):
            for topicQueue in self.__pubSubEntries.values():
                if topicQueue.qsize() > self.__maxConnectionsPerTwitchChannel:
                    pubSubTopicsToRemove.append(topicQueue.get(block = True, timeout = 3))

        if utils.hasItems(pubSubTopicsToAdd):
            self.__timber.log('PubSubUtils', f'Subscribing to {len(newPubSubEntries)} PubSub user(s)...')
            await self.__pubSubPool.subscribe_topics(pubSubTopicsToAdd)
            self.__timber.log('PubSubUtils', f'Finished subscribing to {len(newPubSubEntries)} PubSub user(s)')

        if utils.hasItems(pubSubTopicsToRemove):
            self.__timber.log('PubSubUtils', f'Unsubscribing from {len(pubSubTopicsToRemove)} PubSub user(s)...')
            await self.__pubSubPool.unsubscribe_topics(pubSubTopicsToRemove)
            self.__timber.log('PubSubUtils', f'Finished unsubscribing from {len(pubSubTopicsToRemove)} PubSub user(s)')

        self.__isManagingPubSub = False
