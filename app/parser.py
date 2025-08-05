"""Parser for telegram."""

import logging
from abc import ABC, abstractmethod
from collections.abc import AsyncGenerator
from typing import Any

from telethon import TelegramClient
from telethon.tl.functions.channels import GetParticipantsRequest
from telethon.tl.functions.messages import GetHistoryRequest
from telethon.tl.types import (
    Channel,
    ChannelParticipantsSearch,
    InputChannel,
    InputPeerChannel,
    PeerUser,
    User,
)

logger = logging.getLogger(__name__)


class BaseParser(ABC):
    """Parser for telegram."""

    def __init__(
        self,
        client: TelegramClient,
        target_entity: str,
    ) -> None:
        """Initialize parser.

        :param client: Telegram client
        :param target_entity: Target entity
        """
        self._client = client
        self._target_entity = target_entity
        self._parsed = 0

    @abstractmethod
    async def parse(self) -> AsyncGenerator[str, None]:
        """Parse method."""
        yield ""
        raise NotImplementedError

    @property
    def parsed(self) -> int:
        """Count of parsed elements."""
        return self._parsed

    async def _get_channel_entity(self) -> Channel:
        """Get and validate channel entity."""
        entity = await self._client.get_entity(self._target_entity)
        if isinstance(entity, list):
            entity = entity[-1]

        if not isinstance(entity, Channel):
            msg = f"Entity is not a Channel, got {type(entity)}"
            raise TypeError(msg)

        if entity.access_hash is None:
            msg = "Channel access_hash is None, cannot proceed"
            raise ValueError(msg)

        return entity


class ChannelParser(BaseParser):
    """Parser for telegram channel."""

    def __init__(
        self,
        client: TelegramClient,
        target_entity: str,
    ) -> None:
        """Initialize channel parser.

        :param client: Telegram client
        :param target_entity: Target entity
        """
        super().__init__(client, target_entity)

    async def parse(self) -> AsyncGenerator[str, None]:
        """Get participants.

        :return: Async generator of participants
        """
        entity = await self._get_channel_entity()

        while True:
            participants: Any = await self._client(
                GetParticipantsRequest(
                    channel=InputChannel(
                        entity.id,
                        entity.access_hash,  # type: ignore[attr-defined]
                    ),
                    offset=self._parsed,
                    limit=200,
                    filter=ChannelParticipantsSearch(""),
                    hash=0,
                ),
            )

            users_list = getattr(participants, "users", [])
            if not users_list:
                break

            with_username = 0
            for participant in users_list:
                if isinstance(participant, User) and participant.username:
                    with_username += 1
                    yield participant.username

            logger.info(
                "Get participants: %s, with username: %s",
                len(users_list),
                with_username,
            )
            self._parsed += len(users_list)


class MessageHistoryParser(BaseParser):
    """Parser for telegram message."""

    def __init__(
        self,
        client: TelegramClient,
        target_entity: str,
    ) -> None:
        """Initialize message parser.

        :param client: Telegram client
        :param target_entity: Target entity
        """
        super().__init__(client, target_entity)

    async def parse(self) -> AsyncGenerator[str, None]:
        """Get messages.

        :return: Async generator of messages
        """
        entity = await self._get_channel_entity()

        while True:
            messages: Any = await self._client(
                GetHistoryRequest(
                    peer=InputPeerChannel(
                        entity.id,
                        entity.access_hash,  # type: ignore[attr-defined]
                    ),
                    offset_id=0,
                    offset_date=None,
                    add_offset=self._parsed,
                    limit=100,
                    max_id=0,
                    min_id=0,
                    hash=0,
                ),
            )

            messages_list = getattr(messages, "messages", [])
            if not messages_list:
                break

            with_username = 0
            for message in messages_list:
                if hasattr(message, "from_id") and isinstance(
                    message.from_id,
                    PeerUser,
                ):
                    user_entity = await self._client.get_entity(
                        message.from_id.user_id,
                    )

                    if isinstance(user_entity, User) and user_entity.username:
                        with_username += 1
                        yield user_entity.username

            logger.info(
                "Get messages: %s, with username: %s",
                len(messages_list),
                with_username,
            )
            self._parsed += len(messages_list)
