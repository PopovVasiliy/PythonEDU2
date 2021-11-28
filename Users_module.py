from enum import Enum
from abc import abstractmethod
from dataclasses import dataclass


class Status(Enum):
    online = 0
    offline = 1
    printing = 2


@dataclass
class ClientUsers:
    nick_user: str
    name_user: str
    status: Status


class AbstractUser(object):

    @abstractmethod
    def get_users(self):
        return NotImplemented

    @staticmethod
    def get_users_from_server():
        return NotImplemented


class ClientUsersStorage(AbstractUser):
    def __init__(self):
        self._list_of_Users = []

    # ///////получить список пользователей ///////
    def get_users(self):
        return self._list_of_Users

    def get_user(self, nick_user):
        for client_user in self._list_of_Users:
            if client_user.nick_user == nick_user:
                return client_user
        return None

    def set_user(self, nick_user: str, name_user: str, status: Status):
        new_user = ClientUsers(nick_user, name_user, status)
        self._list_of_Users.append(new_user)
