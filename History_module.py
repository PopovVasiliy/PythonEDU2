from datetime import datetime
from dataclasses import dataclass
from abc import abstractmethod
import sqlite3
from typing import Tuple
from Users_module import *

@dataclass
class HistoryMessages:
    message_datetime: datetime
    message_user: ClientUsers
    message_text: str


class BaseHistoryMessages:
    def __init__(self, filename: str = ""):
        self._list_of_messages = []
        self._filename = filename

    @abstractmethod
    def history_messages(self):
        return NotImplemented

    @abstractmethod
    def clear_history_user(self, user: ClientUsers = None):
        return NotImplemented


class HistoryMessagesMemoryStorage(BaseHistoryMessages):
    def __init__(self):
        super().__init__()
        self.list_of_messages_user = []

    # получить историю сообщений по пользователю
    @property
    def history_messages(self, user: ClientUsers = None):

        if user is None:
            return self._list_of_messages
        else:
            self.list_of_messages_user.clear()
            for elem in self._list_of_messages:
                if elem.message_user == user:
                    self.list_of_messages_user.append(elem)
            return self.list_of_messages_user

    # добавить сообщение в историю сообщений
    @history_messages.setter
    def history_messages(self, history_message: HistoryMessages):
        self._list_of_messages.append(history_message)

    # очистить историю сообщений по пользователю
    def clear_history_user(self, user: ClientUsers = None):
        if user is None:
            self._list_of_messages.clear()
        else:
            pulldel = 0
            while pulldel == 0:
                for elem in self._list_of_messages:
                    if elem.message_user == user:
                        self._list_of_messages.remove(elem)
                        break
                    pulldel = 1


class HistoryMessagesDatabaseStorage(BaseHistoryMessages):
    def __init__(self, filename, user_storage_: ClientUsersStorage):
        super().__init__()
        self.__connection = sqlite3.Connection(filename)
        self.__cursor = self.__connection.cursor()
        self._user_storage = user_storage_
        self.list_of_messages_user = []
        self.__cursor.execute(
            'CREATE TABLE IF NOT EXISTS history_messages (message_datetime datetime, nick_user text, message_text text)')

    @property
    def history_messages(self, user: ClientUsers = None):
        self.list_of_messages_user.clear()
        if user is None:
            rows = self.__cursor.execute('SELECT * FROM history_messages ')
        else:
            rows = self.__cursor.execute('SELECT * FROM history_messages WHERE nick_user=:nick_user', {'nick_user': user.nick_user})

        for elem in rows:
            self.list_of_messages_user.append(self._make_history_message(elem))

        return self.list_of_messages_user

    @history_messages.setter
    def history_messages(self, history_message: HistoryMessages):
        self.__cursor.execute(
            'INSERT INTO history_messages VALUES (:message_datetime, :nick_user, :message_text) ', (history_message.message_datetime, history_message.message_user.nick_user, history_message.message_text))
        self.__connection.commit()

    def clear_history_user(self, user: ClientUsers = None):
        if user is None:
            self.__cursor.execute('DELETE FROM history_messages')
            self.__connection.commit()

        else:
            self.__cursor.execute('DELETE FROM history_messages  WHERE nick_user=:nick_user', {'nick_user': user.nick_user})
            self.__connection.commit()

    def _make_history_message(self, row: Tuple[datetime, str, str]) -> HistoryMessages:

        return HistoryMessages(row[0], self.get_user_on_usernick(self._user_storage, row[1]), row[2])

    @staticmethod
    def get_user_on_usernick(user_storage__: ClientUsersStorage, usernick):
        return user_storage__.get_user(usernick)

