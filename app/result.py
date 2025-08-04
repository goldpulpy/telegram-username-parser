"""Result for the username parser"""

import logging
from abc import ABC, abstractmethod
from datetime import datetime
from pathlib import Path

logger = logging.getLogger(__name__)


class Interface(ABC):
    """Interface for the result"""

    @abstractmethod
    def add_user(self, username: str, add_tag: bool = True) -> bool:
        """Add a user to the result

        :param username: username to add
        :param add_tag: whether to add the tag "@username"
        :return: whether the user was added
        """

    @property
    @abstractmethod
    def result_path(self) -> Path:
        """Get the path to the storage"""


class StorageInterface(ABC):
    """Interface for storage operations"""

    @abstractmethod
    def save(self, content: str) -> None:
        """Save content to storage"""

    @property
    @abstractmethod
    def path(self) -> Path:
        """Get the path to the storage"""


class FileStorage(StorageInterface):
    """File storage implementation"""

    def __init__(self, directory: str) -> None:
        self._directory = Path(directory)
        self._directory.mkdir(parents=True, exist_ok=True)
        self._file = f"{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.txt"
        self._path = self._directory / self._file

    def save(self, content: str) -> None:
        with open(self._path, "a", encoding="utf-8") as file:
            file.write(f"{content}\n")
        logger.debug("Added %s to %s", content, self._path)

    @property
    def path(self) -> Path:
        """Get the path to the storage"""
        return self._path


class DublicateCounter:
    """Counter for dublicate elements"""

    def __init__(self) -> None:
        self._dublicates = 0

    @property
    def dublicates(self) -> int:
        """Count of dublicate elements"""
        return self._dublicates


class UserResult(Interface, DublicateCounter):
    """Result for the username parser"""

    def __init__(self, storage: StorageInterface) -> None:
        self._storage = storage
        self._users = []
        DublicateCounter.__init__(self)

    def add_user(self, username: str, add_tag: bool = True) -> bool:
        """Add a user to the result

        :param username: username to add
        :param add_tag: whether to add the tag "@username"
        """
        if add_tag:
            username = f"@{username}"
            logger.debug("Adding tag to %s", username)

        if username not in self._users:
            self._users.append(username)
            self._storage.save(username)
            return True

        self._dublicates += 1
        logger.debug("Dublicate: %s", username)
        return False

    @property
    def result_path(self) -> Path:
        """Get the path to the storage"""
        return self._storage.path

    def __len__(self) -> int:
        """Get the number of users"""
        return len(self._users)
