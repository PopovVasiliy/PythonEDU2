# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

from History_module import *


# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    # тесты
    # инициализируем хранилище с пользователями
    user_storage = ClientUsersStorage()

    # добавляем туда пользователей
    user_storage.set_user('loki', 'Vasiliy', Status.online)
    user_storage.set_user('Iv21', 'Ivan', Status.online)

    # создаем два объекта истории сообщений
    h_message1 = HistoryMessages(datetime.today(), user_storage.get_user('loki'), 'Наше первое сообщение из истории')
    h_message2 = HistoryMessages(datetime.today(), user_storage.get_user('Iv21'), 'Наше второе сообщение из истории')

    # создаем хранилище для сообщений в базе данных и записываем Insert-ом туда данные объектов
    # our_storage = HistoryMessagesMemoryStorage()
    our_storage = HistoryMessagesDatabaseStorage('our_file.txt', user_storage)
    our_storage.history_messages = h_message1
    our_storage.history_messages = h_message2

    # удаляем из базы данных историю сообщений одного из пользователей
    our_storage.clear_history_user(user_storage.get_user('Iv21'))

    # получаем текущие сообщения пользователей
    list_of_messages = our_storage.history_messages

    # выводим их на экран
    for el in list_of_messages:
        print(el.message_user.name_user)
        print(el.message_text)

