from datetime import datetime

from model.MessageModel import MessageModel 

class MessageController():
    bad_words_file = open('./../badwords.txt', 'r')
    all_lines = bad_words_file.read()
    bad_words = all_lines.split(', ')
    print(bad_words)
    @classmethod
    def get_old_messages(cls, room):
        return list(map(lambda x: x.json() if x else None, MessageModel.filter_by_room(room)))

    @classmethod
    def clean_message(cls, username, room, message):
        words = message.split(' ')
        for i in range(len(words)):
            if words[i] in bad_words:
                words[i] = "고양이"
        new_message = MessageModel(username, room, message)
        new_message.save_to_db()
        return new_message.json()


    @classmethod
    def new_message(cls, username, room, message):
        new_message = MessageModel(username, room, message)
        new_message.save_to_db()
        return new_message.json()
