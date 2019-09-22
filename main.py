import telebot as tb
from dbhelper import DBHelper
import datetime

bot = tb.TeleBot('944057887:AAEhF2Xp3lHFmc4ipZP8xNVExvzRI7BtL24')

@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, 'Привет, давай-ка я поведаю о функционале!\n '+
    'Я призван для того чтобы хранить только самое последнее дз, чтобы не было "А что задали?", что может раздражать нас, физматеров :)\n'+
    'Так, что насчет команд? Я умею хранить последнее дз, добавлять что-то упущенное к дз и конечно ведать о нем если нужно, не держать же все в себе, верно? Ниже описаны команды(патерны) которые я понимаю:\n')
    bot.send_message(message.chat.id, '/update название_предмета домашнее задание - заменить последнее задание по предмету\n' +
    '/add название_предмета дополнение к дз - добавить информацию к дз по предмету\n' +
    '/show название_предмета - показывает последнее дз по предмету\n'+
    '/help - рекурсия :)')

@bot.message_handler(content_types=['text'])
def messages_processing(message):
    if not message.text is None:
        if message.text.startswith('/help'):
            bot.send_message(message.chat.id, '/update название_предмета домашнее задание - заменить последнее задание по предмету\n' +
    '/add название_предмета дополнение к дз - добавить информацию к дз по предмету\n' +
    '/show название_предмета - показывает последнее дз по предмету\n'+
    '/help - рекурсия :)')
        
        # Update task
        if message.text.startswith('/update'):
            text = message.text.replace('/update', '')
            if len(text.split()) >= 2:
                db = DBHelper()
                db.setup(columns=['subject', 'task', 'photos', 'date'])
                now = datetime.datetime.now()
                splitted_text = text.split()
                items = [splitted_text[0].lower(), ' '.join(splitted_text[1:]), '', now.strftime('%m-%d')]
                db.change_item(items, 'subject')
                bot.send_message(message.chat.id, 'Твое дз в надежных руках ;)')
            else:
                bot.send_message(message.chat.id, 'Хей, перечитай в каком виде должна быть команда! Предмет должен быть одним словом!')
        
        # Add information to exist task
        if message.text.startswith('/add'):
            text = message.text.replace('/add', '')
            if len(text.split()) >= 2:
                db = DBHelper()
                db.setup(columns=['subject', 'task', 'photos', 'date'])
                now = datetime.datetime.now()
                splitted_text = text.split()
                items = [splitted_text[0].lower(), ' '.join(splitted_text[1:]), '', now.strftime('%m-%d')]
                db.update_item(items, 'subject')
                bot.send_message(message.chat.id, 'Ладно, ладно, в последний раз добавляю коррективы в твое дз! В следующий раз не забывай ничего!')
            else:
                bot.send_message(message.chat.id, 'Хей, перечитай в каком виде должна быть команда! Предмет должен быть одним словом!')

        # Show subject
        if message.text.startswith('/show'):
            text = message.text.replace('/show', '')
            if len(text.split()) >= 1:
                db = DBHelper()
                db.setup(columns=['subject', 'task', 'photos', 'date'])
                subject = text.split()[0]
  
                item = db.get_items(subject.lower(), 'subject')
                if len(item) < 1:
                    bot.send_message(message.chat.id, 'Такого предмета я не помню... Может с русским беда?')
                else:
                    item = item[0]
                    text = '|'+item[0].capitalize()+'|' + '\n|Дата: ' + item[3] + '|\n' + item[1].capitalize()
                    bot.send_message(message.chat.id, text)
                    if len(item[2].split()) >= 1:
                        for i in item[2].split():
                            bot.send_photo(message.chat.id, i)
            else:
                bot.send_message(message.chat.id, 'Хей, перечитай в каком виде должна быть команда! Предмет должен быть одним словом!')




@bot.message_handler(content_types=['photo'])
def messages_processing2(message): 
    if not message.caption is None:
        if message.caption.startswith('/update'):
            text = message.caption.replace('/update', '')
            if len(text.split()) >= 2:
                db = DBHelper()
                db.setup(columns=['subject', 'task', 'photos', 'date'])
                now = datetime.datetime.now()
                splitted_text = text.split()
                items = [splitted_text[0].lower(), ' '.join(splitted_text[1:]), '', now.strftime('%m-%d')]
                db.change_item(items, 'subject')
                db.update_item([splitted_text[0].lower(), '', message.photo[0].file_id, now.strftime('%m-%d')], 'subject')
                bot.send_message(message.chat.id, 'Твое дз в надежных руках ;)')
            else:
                bot.send_message(message.chat.id, 'Хей, перечитай в каком виде должна быть команда! Предмет должен быть одним словом!')
        
        if message.caption.startswith('/add'):
            text = message.caption.replace('/add', '')
            if len(text.split()) >= 2:
                db = DBHelper()
                db.setup(columns=['subject', 'task', 'photos', 'date'])
                now = datetime.datetime.now()
                splitted_text = text.split()
                items = [splitted_text[0].lower(), ' '.join(splitted_text[1:]), message.photo[0].file_id, now.strftime('%m-%d')]
                db.update_item(items, 'subject')
                bot.send_message(message.chat.id, 'Ладно, ладно, в последний раз добавляю коррективы в твое дз! В следующий раз не забывай ничего!')
            else:
                bot.send_message(message.chat.id, 'Хей, перечитай в каком виде должна быть команда! Предмет должен быть одним словом!')

        


bot.polling(none_stop=True, interval=0, timeout=200)