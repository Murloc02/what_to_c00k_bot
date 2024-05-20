from os import path
from pickle import dump, load

FOLDER = 'user_messages'


def get_messages(user_id: (int, str)):
    if type(user_id) is int:
        user_id = str(user_id)
    file_name = path.join(FOLDER, user_id)
    if not path.exists(file_name):
        return None
    with open(file_name, 'rb') as file:
        messages = load(file)
    return messages


def save_messages(user_id: (int, str), messages: list):
    if type(user_id) is int:
        user_id = str(user_id)
    file_name = path.join(FOLDER, user_id)
    with open(file_name, 'wb') as file:
        dump(messages, file)


if __name__ == '__main__':
    # save_messages(123, [{1: 34, 3: 34}, {'324': '324'}])
    print(get_messages(1345005475))
