
import time
import os

TOKEN ='891815354:AAHPEgLm6cGvVq9LC16qVHGediSgd23s6G4'

proxies = {
    'http': 'http://217.23.6.40:8080',
    'https': 'http://51.15.76.119:3128',
}

# apihelper.proxy = proxies

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Howdy, how are you doing?")


# Обработка команд
@bot.message_handler(commands=['timer'])
def timer(message):
    for i in range(5):
        time.sleep(1)
        bot.send_message(message.chat.id, i + 1)


# Команда в параметром
@bot.message_handler(commands=['say'])
def say(message):
    # получить то что после команды
    text = ' '.join(message.text.split(' ')[1:])
    bot.reply_to(message, f'***{text.upper()}!***')


# Команда администратора
@bot.message_handler(commands=['admin'], func=lambda message: message.from_user.username == 'DanteOnline')
def admin(message):
    print(message)
    info = os.name
    bot.reply_to(message, info)


@bot.message_handler(commands=['admin2'])
def admin2(message):
    if message.from_user.username == 'DanteOnline':
        info = os.name
        bot.reply_to(message, info)
    else:
        bot.reply_to(message, 'Метод недоступен, нет прав')


@bot.message_handler(commands=['restart'])
def restart_server(message):
    # выполнить команду операционки из python
    # os.system('notepad')
    bot.reply_to(message, 'ура!')


@bot.message_handler(commands=['file'])
def get_file(message):
    print('зашел')
    # Передать какой то файл который есть на диске
    # with open('text.txt', 'r', encoding='utf-8') as data:
    #     bot.send_document(message.chat.id, data)
    with open('pict.jpg', 'rb') as data:
        bot.send_photo(message.chat.id, data)


@bot.message_handler(content_types=['text'])
def reverse_text(message):
    if 'плохой' in message.text.lower():
        bot.reply_to(message, 'В тексте слово плохой')
        return
    text = message.text[::-1]
    bot.reply_to(message, text)


@bot.message_handler(content_types=['sticker'])
def send_sticker(message):
    FILE_ID = 'CAADAgADPQMAAsSraAsqUO_V6idDdBYE'
    bot.send_sticker(message.chat.id, FILE_ID)


bot.polling(none_stop=True, timeout=123)