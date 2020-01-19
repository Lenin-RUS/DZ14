import json
import requests
from bs4 import BeautifulSoup
import random
from telegram.ext import Updater
from telegram.ext import CommandHandler, MessageHandler, Filters
import time

# Токен
TOKEN ='891815354:AAHPEgLm6cGvVq9LC16qVHGediSgd23s6G4'

# Прокси
REQUEST_KWARGS={
    'proxy_url': 'http://83.175.166.234:8080',
}

# Запуск бота    , request_kwargs=REQUEST_KWARGS
updater = Updater(token=TOKEN, use_context=True)
dispatcher = updater.dispatcher

manual='/help - этот Хелп \n /start - старт бота \n /rand_im - случайная картинка \n /rand_im_cont n - n случайных картинок \n /rand_com - комментарии со случайной страницы \n /send_img n - картинка со страницы n \n /send_com n - комментарии со страницы n'


# команда старт -                                                                                                                   РАБОТАЕТ
def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Добро пожаловать в телеграмм бот Ильича")
start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

# команда хэлп  -                                                                                                                   РАБОТАЕТ
def help(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text=manual)
help_handler = CommandHandler('help', help)
dispatcher.add_handler(help_handler)

# команда вывод случайной картинки
def rand_im(update, context):
    n=random.randint(100,13850)
    url = 'http://udaff.com/view_listen/photo/page'+str(n)+'.html'
    soup = BeautifulSoup(requests.get(url).text, 'html.parser')
    div_tag_pic="http://udaff.com"+soup.find('div', class_="pic-cont").find('img').get('src')
    print(div_tag_pic)
    context.bot.send_message(chat_id=update.effective_chat.id, text=div_tag_pic)
rand_im = CommandHandler('rand_im', rand_im)
dispatcher.add_handler(rand_im)

# команда вывод случайной картинки в цикле
def rand_im_cont(update, context):
    n = int(context.args[0])
    for i in range(10):
        url = 'http://udaff.com/view_listen/photo/page'+str(n+i)+'.html'
        soup = BeautifulSoup(requests.get(url).text, 'html.parser')
        div_tag_pic="http://udaff.com"+soup.find('div', class_="pic-cont").find('img').get('src')
        print(div_tag_pic)
        context.bot.send_message(chat_id=update.effective_chat.id, text=div_tag_pic)
        time.sleep(2)

rand_im_cont = CommandHandler('rand_im_cont', rand_im_cont)
dispatcher.add_handler(rand_im_cont)

# команда вывод случайных комментариев                                                                                           -   РАБОТАЕТ
def rand_com(update, context):
    n=random.randint(100,13850)
    result_of_parsing=parser(1,n)
    for cur_comment in result_of_parsing[0]['comments']:
        context.bot.send_message(chat_id=update.effective_chat.id, text=cur_comment['comment'])
rand_com = CommandHandler('rand_com', rand_com)
dispatcher.add_handler(rand_com)




# картинка со страницы n
def send_img(update, context):
    n = int(context.args[0])
    url = 'http://udaff.com/view_listen/photo/page'+str(n)+'.html'
    soup = BeautifulSoup(requests.get(url).text, 'html.parser')
    div_tag_pic="http://udaff.com"+soup.find('div', class_="pic-cont").find('img').get('src')
    print(div_tag_pic)
    context.bot.send_message(chat_id=update.effective_chat.id, text=div_tag_pic)
send_img = CommandHandler('send_img', send_img)
dispatcher.add_handler(send_img)


# комментарий со страницы n                                                                                                          -РАБОТАЕТ

def send_com(update, context):
    n = int(context.args[0])
    result_of_parsing=parser(1, n)
    for cur_comment in result_of_parsing[0]['comments']:
        context.bot.send_message(chat_id=update.effective_chat.id, text=cur_comment['comment'])
send_com = CommandHandler('send_com', send_com)
dispatcher.add_handler(send_com)



updater.start_polling()



# number_of_pages=int(input('Сколько страниц парсить: '))
# first_page_to_parce = int(input('С какой страницы парсить (там около 15 000 страниц): '))

def parser(number_of_pages, first_page_to_parce):
    udaff_parser_all=[]
    udaff_parser=dict()

    for i in range(number_of_pages):
        udaff_parser=dict()
        url = 'http://udaff.com/view_listen/photo/page'+str(first_page_to_parce+i)+'.html'
        udaff_parser['url']=url
        udaff_parser['number']=i
        soup = BeautifulSoup(requests.get(url).text, 'html.parser')
        div_tag_comments=soup.find('div', class_="comments")
        comment_number=1
        udaff_comment_tmp=[]
        print(url)
        while not div_tag_comments.find('div', class_="item N"+str(comment_number)) is None:
            udaff_comment={}
            udaff_comment['comment_number']=comment_number
            item_tag = div_tag_comments.find('div', class_="item N"+str(comment_number))
            udaff_comment['comment']=item_tag.find('p', class_="c_msg_text").text
            author=item_tag.find('p', class_="author")
            author_name=author.find('a')
            try:
                udaff_comment['author']=author_name.text
            except:
                udaff_comment['author']=author.text
            udaff_comment_tmp.append(udaff_comment)
            # print(udaff_comment)
            comment_number=comment_number+1
        print(f'На странице было {comment_number-1} комментариев')
        udaff_parser['comments'] = udaff_comment_tmp
        udaff_parser_all.append(udaff_parser)
    return(udaff_parser_all)


    # with open(f'Udaff_from_{first_page_to_parce}_to_{first_page_to_parce+number_of_pages-1}.json', 'w') as f:
    #     json.dump({'udaff':udaff_parser_all}, f)
#
# n=random.randint(1,13850)
# result_of_parsing=parser(1,n)
# print(result_of_parsing)
# for cur_comment in result_of_parsing[0]['comments']:
#     print(cur_comment['comment'])



# parser(number_of_pages, first_page_to_parce)