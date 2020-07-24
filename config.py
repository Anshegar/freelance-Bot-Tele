from telegram import Update, ReplyKeyboardRemove, ReplyKeyboardMarkup
from telegram.ext import CallbackContext
from  datetime import datetime

from telegram import Bot
from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler
from telegram.ext import CallbackQueryHandler
from telegram.ext import Filters
from telegram.ext import CallbackContext
from telegram.ext import ConversationHandler
from telegram.ext import RegexHandler
from telegram.ext import PicklePersistence
import logging
import requests
from bs4 import BeautifulSoup
import re
import os
from random import randint
from threading import Timer
from datetime import datetime, timedelta
from time import sleep


from db import db, User, Ask_for_help
from red_api import *

from api_nkp import api_c, api_f, api_f_auth


from proxy.prox import TG_TOKEN, TG_API_URL
from proxy.const import API_BOT_NAME, API_BOT_PASS, URL

def check_user(name,chat_id):
    mail = 'no help askin'
    subscribe = 0
    if User.query.filter_by(chat_id=chat_id).first():
        print('user exist')
        pass

    else:
        new_user = User(name, mail, chat_id, subscribe)
        db.session.add(new_user)
        db.session.commit()
        print('new user add to BD')



# АВТОМАТИЧЕСКАЯ Приветсвовалка для новых мемберов
def welcome(update, context):
    check_user(update.message.from_user.full_name, update.message.chat_id)

    name1 = update.message.from_user.first_name
    name2 = update.message.from_user.last_name
    update.message.reply_text(f'Welcome to our Group {name1} {name2}')


def do_user_test(update: Update, context):
    check_user(update.message.from_user.full_name,update.message.chat_id )


    chat_id = update.message.chat_id

    user_id = update.message.from_user
    name1 = update.message.from_user.first_name
    name2 = update.message.from_user.last_name
    full_name  = update.message.from_user.full_name


    pro = '104.248.4.187'
    proxies = {'http':f'{pro}','https':f'{pro}','HTTP':f'{pro}','HTTPS':f'{pro}'}
    text = 'Test1'
    url = f'http://api.telegram.org/bot{TG_TOKEN}/sendMessage?chat_id={chat_id}&text={text}'
    requests.post(url,proxies=proxies,data ='Test2222')

    update.message.reply_text(f'Hello User,\n your chat_id - {chat_id},'
                              f'\nyour id - {user_id}'
                              f'\nyour f_name - {name1}'
                              f'\nyour l_name - {name2}'
                              f'\nyour full name {full_name}')


def do_user_test1(bot, update,context):
    print(1)
    check_user(update.message.from_user.full_name, update.message.chat_id)

    chat_id = bot.get_updates()[-1].message.chat_id
    print(chat_id)
    answer = 'Hi'
    bot.sendMessage(chat_id=chat_id, text=answer)




def legend(update: Update, context):
    check_user(update.message.from_user.full_name, update.message.chat_id)

    #name = update.message.from_user.first_name
    name1 = update.message.from_user.first_name
    name2 = update.message.from_user.last_name
    chat_id = update.message.chat_id

    update.message.reply_text(f'Hello {name1} {name2},\nto contact with admin and ask for help, pleas enter command /help_ask !')


#-------------------------------------------------------------- API ------------------------------------------------------------------------------

# Резервные советы, можно и в БД записать, но лучше не перегружать
def offline_api():
    adv_list =[]
    filepath = os.path.abspath(os.path.dirname(__file__)) + '/base.txt'
    baseopen = open(filepath, mode='r', encoding='utf-8-sig')
    for line in baseopen:
        i = line.strip('-').strip()
        if i != '':
            adv_list.append(i)
    baseopen.close()
    generate = randint(0, len(adv_list))
    choice = adv_list[generate - 1]
    return str(choice)


# Разобраться с кодировкой - НЕРАБОТАЕТ
def api_classic(update: Update, context):
    check_user(update.message.from_user.full_name, update.message.chat_id)

    chat_id = update.message.chat_id
    update.message.reply_text(f'1) Hello User ID {chat_id}, here is your advice\n {api_c()}')

# НЕИСПОЛЬЗОВАТЬ
def api_flask(update: Update, context):
    check_user(update.message.from_user.full_name, update.message.chat_id)

    full_name  = update.message.from_user.full_name
    update.message.reply_text(f' Hello  {full_name}, here is your advice\n {api_f()}. '
                              f'\n Если вы захотите подписаться на ежедневные советы введите /adv_sub ')

# ИСПОЛЬЗОВАТЬ
def api_flask_auth(update: Update, context):
    check_user(update.message.from_user.full_name, update.message.chat_id)

    full_name  = update.message.from_user.full_name
    # Проверка наличия сервера, если нету, то из офлан советов дает совет
    try:
        update.message.reply_text(f' Hello  {full_name}, here is your advice\n {api_f_auth()}. '
                              f'\n Вы Авторизированы дял получения советов , если захотите отменить подписку то напишите /no_adv_sub ')
        print('online')
    except Exception as e:
        update.message.reply_text(f' Hello  {full_name}, here is your advice\n {offline_api()}. '
                                  f'\n Вы Авторизированы дял получения советов , если захотите отменить подписку то напишите /no_adv_sub ')
        print('offline')


# ------------------------------------------------------- Reminder -------------------------------------------------------------------------


def adv_sub(update: Update, context):
    check_user(update.message.from_user.full_name, update.message.chat_id)
    chat_id = update.message.from_user['id']
    user = User.query.filter_by(chat_id=int(chat_id)).first()
    if user:
        user.subscribe = 1
        db.session.add(user)
        db.session.commit()
    update.message.reply_text(f' Подписка оформленна, если захотите отменить подписку то напишите /no_adv_sub ')





def no_adv_sub(update: Update, context):
    check_user(update.message.from_user.full_name, update.message.chat_id)
    chat_id = update.message.from_user['id']
    user = User.query.filter_by(chat_id=int(chat_id)).first()
    if user:
        user.subscribe = 0
        db.session.add(user)
        db.session.commit()
    update.message.reply_text(f'Подписка отменена, если захотите  вновь подписаться отменить подписку то напишите /adv_sub ')



def reminder(updater):

    #Создаем среду для отправки сообщений через updater.bot
    mess_sender = updater.bot

    # Приводим все запросы на автосоветы к единому времени. Создаем дельту, разницу  между текущей  и наступившей датой
    # ВАЖНО что бы при окончании месяца программа не ебнулась надо добавить + timedelta(day=1), или hour или minute
    try:
        x = datetime.today()
        y = x.replace(day=x.day + 1, hour=8, minute=0, second=0, microsecond=0)  # + timedelta(seconds=4)

    except Exception as e:
        # Если переход с 31 на 1 то плючует к таймдельте что бы дни не становились отрицательными
        print(e)
        x = datetime.today()
        y = x.replace(day=x.day, hour=8, minute=0, second=0, microsecond=0) + timedelta(days=1)


    delta_t = y - x

    # Вычисление промежутка первого запуска программы
    secs = delta_t.total_seconds()
    print('Время до запуска: ', secs)

    # Цикл ежедневного повторения отправки советов всем пользователям с включенными автосоветами
    # в новом потоке отдельном от основного скрипта,
    # он каждый заданый выше отрезок вроемени будет проверять  БД, и отправлять сообщение
    def checkin_user():
        while True:
            print("Активация напоминания")
            user = User.query.filter_by(subscribe=1).all()
            try:
                for i in user:
                    print(i.name)
                    data = requests.get(URL + API_BOT_NAME + API_BOT_PASS)
                    soup = BeautifulSoup(data.text, 'html.parser')
                    print(soup)
                    mess_sender.send_message(chat_id=f'{i.chat_id}', text=f'Ваш ежедневный совет : \n{soup}', )
                    print('online')
            except Exception as e:
                for i in user:
                    print(i.name)
                    mess_sender.send_message(chat_id=f'{i.chat_id}', text=f'Ваш ежедневный совет : \n{offline_api()}', )
                    print('online')


            sleep(86400)


    # Создание нового, ассинхроного потока, отдельного от потока основной программы и запуск его
    t = Timer(secs, checkin_user)
    t.start()




#--------------------------------------------------------------------------------------------------------------------------------------------






# Применяется для ввода данных после команды, к примеру надо добавить почту , пишем команду добавления почты и почту
def parse_command(update: Update) -> (str, str):
    # Получаем текст от пользователя, и разделяем один раз его, отделяя коману от самого сообщения которое нужно сохранить
    key, value = update.message.text.split(' ', 1)
    #print('1', key,value)
    return key, value


# ---------
# Askin for help. global arg - mail + ask (/help_ask)
MAIL, ASK = range(2)

def start_handler_func(update: Update, context: CallbackContext):
    check_user(update.message.from_user.full_name, update.message.chat_id)

    # Ask Name
    update.message.reply_text('Введите свою электроную почту, что бы мы могли связаться с вами в случае необходимости, пожалуйста:',
                              reply_markup=ReplyKeyboardRemove())
    return MAIL



def mail_handler_func(update, context):
    # Get mail
    context.user_data[MAIL] = update.message.text
    update.message.reply_text(f'Пожалуйста, опишите вашу проблемму')
    return ASK


def ask_handler_func(update, context):
    context.user_data[ASK] = update.message.text
    update.message.reply_text(
        f'Ваша проблемма будет рассмотрена в ближайшее время, благодарим за обращение')

    name = update.message.from_user.first_name
    chat_id = update.message.chat_id
    mail = context.user_data[MAIL]
    ask = context.user_data[ASK]
    date = datetime.utcnow()

    new_ask = Ask_for_help(name, chat_id, mail, ask, date)
    db.session.add(new_ask)
    db.session.commit()
    return ConversationHandler.END


def cancel_handler_func(update, context):
    print(999)
    update.message.reply_text('Ввод данных отменен')
    return ConversationHandler.END



conv_handler_var = ConversationHandler(
    entry_points=[CommandHandler('help_ask', start_handler_func)],
    states={
        MAIL: [MessageHandler(Filters.all, mail_handler_func, pass_user_data=True), ],
        ASK: [MessageHandler(Filters.all, ask_handler_func, pass_user_data=True), ],
    },
    fallbacks=[CommandHandler('cancel', cancel_handler_func), ], )

# -----




# Anketa with buttons( ask- approve- if Yes then over - if no then cancel )
# Анкета с кнопками (Снача спросить чтото, потом подтвердить, если да то закончить если нет то отменить)
# -----

ANK, FIRSTASKONEMORETIME, ASKAPPROVE ,APPROVE =range(4)

def askin_to_start(update,context):
    check_user(update.message.from_user.full_name, update.message.chat_id)

    # Asking
    reply_keyboard = [['Да', 'Нет', 'Спроси ещё раз, я подумаю']]
    update.message.reply_text('Желаете ли вы пройти анкетирование?', reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
    return ANK

def start_anketa(update,context):
    print(update.message.text)
    context.user_data[ANK] = update.message.text

    if update.message.text == 'Да':
        reply_keyboard = [['Мальчик', 'Девочка', 'Сланешит']]
        update.message.reply_text('Кто вы по жизни', reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
        return ASKAPPROVE

    if update.message.text == 'Нет':
        update.message.reply_text('Ввод данных отменен')
        return ConversationHandler.END

    if update.message.text == 'Спроси ещё раз, я подумаю':
        reply_keyboard = [['Да', 'Нет', 'Спроси ещё раз, я подумаю']]
        update.message.reply_text('Повторный запрос \nЖелаете ли вы пройти анкетирование?',
                                  reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
        return ANK


def ask_one_more_time(update,context):
    # Asking
    reply_keyboard = [['Да', 'Нет', 'Спроси ещё раз, я подумаю']]
    update.message.reply_text('Желаете ли вы пройти анкетирование?', reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
    return ANK


def ask_to_approve(update,context):
    context.user_data[ASKAPPROVE] = update.message.text
    reply_keyboard = [['Все верно', 'Нет не верно','Зацикли опрос']]
    update.message.reply_text(f'Вы согластны были пройти опрос{ANK}, по жизни вы{ASKAPPROVE}',
                              reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
    return APPROVE


def approved_anketa(update,context):
    context.user_data[APPROVE] = update.message.text


    if update.message.text == 'Все верно':
        update.message.reply_text('+++++++')
        return ConversationHandler.END

    if update.message.text == 'Нет не верно':

        update.message.reply_text('Ввод данных отменен, хотите ли вы пройти опрос снова?')
        reply_keyboard = [['Да', 'Нет']]
        update.message.reply_text(f'Ввод данных отменен, хотите ли вы пройти опрос снова?',
                                  reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
        return ANK


    if update.message.text == 'Зацикли опрос':
        context.user_data[ASKAPPROVE] = update.message.text
        reply_keyboard = [['Все верно', 'Нет не верно', 'Зацикли опрос']]
        update.message.reply_text(f'Вы согластны были пройти опрос{ANK}, по жизни вы{ASKAPPROVE}',
                                  reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
        return APPROVE





anketa_conv_handler_var = ConversationHandler(
    entry_points=[CommandHandler('ank_start', askin_to_start)],
    states={
        FIRSTASKONEMORETIME: [MessageHandler(Filters.all, ask_one_more_time, pass_user_data=True), ],
        ANK: [MessageHandler(Filters.all, start_anketa, pass_user_data=True), ],
        ASKAPPROVE: [MessageHandler(Filters.all, ask_to_approve, pass_user_data=True), ],
        APPROVE: [MessageHandler(Filters.all, approved_anketa, pass_user_data=True), ],
    },
    fallbacks=[CommandHandler('cancel', cancel_handler_func), ], )

# -----



# -----
# Creating Reddit API for bot
def reddit_api_test(update: Update, context):
    check_user(update.message.from_user.full_name, update.message.chat_id)

    try:
        # Создание Главного ОБЪЕКТА reddit - тоесть обращения ко ВСЕМУ редиту со всеми его тредами
        reddit_def = create_reddit_object()

        # Создание ПОДЗАПРОССА Reddit subreddit - тоесть Запрос треда ( редит это форму а саб редит это ветки этого формума соответсвенно)
        subred = reddit_def.subreddit('starcitizen')

        name = update.message.chat.username
        update.message.reply_text(f"Hello {name},\n here you 3 hotes themes from Reddit \n")

        hot = subred.hot(limit=3)
        hot_list = list(hot)
        for i in hot_list:
            update.message.reply_text(
                f"{i, '-Author: ', i.author, '-Category', i.link_flair_text, '-Title:', i.title, '-Votes up,down,result:', i.ups, i.downs, i.score, '-Date:', i.created_utc, '- Vote for thred:', i.upvote(), i.url}")
    except Exception as e:
        print('No API found')
        print(e)
