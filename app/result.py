"""Result for the username parser."""

import logging
from abc import ABC, abstractmethod
from datetime import datetime, timezone
from pathlib import Path

logger = logging.getLogger(__name__)


class Interface(ABC):
    """Interface for the result."""

    @abstractmethod
    def add_user(self, username: str, *, add_tag: bool = True) -> bool:
        """Add a user to the result.

        :param username: username to add
        :param add_tag: whether to add the tag "@username"
        :return: whether the user was added
        """

    @property
    @abstractmethod
    def result_path(self) -> Path:
        """Get the path to the storage."""


class StorageInterface(ABC):
    """Interface for storage operations."""

    @abstractmethod
    def save(self, content: str) -> None:
        """Save content to storage."""

    @property
    @abstractmethod
    def path(self) -> Path:
        """Get the path to the storage."""


class FileStorage(StorageInterface):
    """File storage implementation."""

    def __init__(self, directory: str) -> None:
        """Initialize file storage.

        :param directory: directory to use
        """
        self._directory = Path(directory)
        self._directory.mkdir(parents=True, exist_ok=True)
        self._file = self._get_file_name()
        self._path = self._directory / self._file

    def _get_file_name(self) -> str:
        """Get the file name."""
        now = datetime.now(tz=timezone.utc).astimezone()
        return f"{now.strftime('%Y-%m-%d_%H-%M-%S')}.txt"

    def save(self, content: str) -> None:
        """Save content to storage."""
        with Path(self._path).open("a", encoding="utf-8") as file:
            file.write(f"{content}\n")
        logger.debug("Added %s to %s", content, self._path)

    @property
    def path(self) -> Path:
        """Get the path to the storage."""
        return self._path


class UserResult(Interface):
    """Result for the username parser."""

    def __init__(self, storage: StorageInterface) -> None:
        """Initialize user result.

        :param storage: storage to use
        """
        self._storage = storage
        self._users = []
        self._duplicates = 0

    def add_user(self, username: str, *, add_tag: bool = True) -> bool:
        """Add a user to the result.

        : param username: username to add
        : param add_tag: whether to add the tag "@username"
        """
        if add_tag:
            username = f"@{username}"
            logger.debug("Adding tag to %s", username)

        if username not in self._users:
            self._users.append(username)
            self._storage.save(username)
            return True

        self._duplicates += 1
        logger.debug("Duplicate: %s", username)
        return False

    @property
    def duplicates(self) -> int:
        """Get the number of duplicates."""
        return self._duplicates

    @property
    def result_path(self) -> Path:
        """Get the path to the storage."""
        return self._storage.path

    def __len__(self) -> int:
        """Get the number of users."""
        return len(self._users)
