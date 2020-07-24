

from telegram import Update, ReplyKeyboardRemove
from telegram.ext import CallbackContext

from telegram.error import (TelegramError, Unauthorized, BadRequest,
                            TimedOut, ChatMigrated, NetworkError)

from db import db, User, Ask_for_help


def error_callback(update, context):
    try:
        raise context.error
    except Unauthorized as e:
        print(e)
        print(1)
        # remove update.message.chat_id from conversation list
    except BadRequest as e:
        print(e)
        print(2)
        # handle malformed requests - read more below!
    except TimedOut as e:
        print(e)
        print(3)
        # handle slow connection problems
    except NetworkError as e:
        print(e)
        print(4)
        # handle other connection problems
    except ChatMigrated as e:
        print(e)
        print(5)
        # the chat_id of a group has changed, use e.new_chat_id instead
    except TelegramError as e:
        print(e)
        print(6)
        # handle all other telegram related errors

def do_admin_test(update: Update, context):
    chat_id = update.message.chat_id
    update.message.reply_text(f'Hello Admin ID {chat_id},\nChat me something, please!')


def parse_command(update: Update) -> (str, str):
    # Получаем текст от пользователя, и разделяем один раз его, отделяя коману от самого сообщения которое нужно сохранить
    key, value = update.message.text.split(' ', 1)
    print('1', key,value)
    return key, value

# Запрос всех комманд
def a_legend(update: Update, context):
    name = update.message.chat.username
    update.message.reply_text(f'\n /test_a      - Тестирование работы комманд админа'
                              f'\n /a_help      - Запрос ВСЕХ комманд бота для админа и для пользователя'
                              f'\n /a_add       - Добавить пользователя в БД ПОЛЬЗОВАТЕЛЯ'
                              f'\n /a_list      - Просмотр ВСЕХ запросов помощи из БД ЗАПРОСА ПОМОЩИ'
                              f'\n /a_id_del    - Удаление запроса о помощи из БД ЗАПРОСА ПОМОЩИ по id запроса'
                              f'\n /a_all_del   - Очистить всю БД ЗАПРОСОВ ПОМОЩИ'
    
                              f'\n /test_u      - Тестирование работы комманд пользователя'
                              f'\n /adv         - Запросить совет NKP'
                              f'\n /help        - Запрос доступных пользователю команд'
                              f'\n /help_ask    - Запрос помощи от пользователя'
                              f'\n /ank_start   - Анкетирование пользователяс кнопками, с возможностью возвращения ик предыдущим пунктам и подтверждением данных '
                              f'\n /api_test    - Тестирование запроса API Редита в телеграмм боте'
                              f'\n END' )


# КОММАНДЫ Просмотра, Добавления, удаления элементов, Удаления элемента, Вывода списка эллементов, очеищение списка от всех элементов

#/a_list
def list_all(update: Update, context: CallbackContext):
    items = Ask_for_help.query.all()
    result = []
    for i in items:
        result.append(str(i))
    update.message.reply_text('\n'.join(result) if len(items) > 0 else 'List empty 😢')


#/a_id_del
def id_del_ask(update: Update, context: CallbackContext):
    key, value  = parse_command(update)

    if Ask_for_help.query.filter_by(id=int(value)).first():
        Ask_for_help.query.filter_by(id=int(value)).delete()
        db.session.commit()
        update.message.reply_text(f'\nПользовател с id:{int(value)} удален')
    else:
        update.message.reply_text(f'\nПользователя с id:{int(value)} несуществует 😢')


#/a_all_del
def list_clear(update: Update, context: CallbackContext):
    Ask_for_help.query.delete()
    db.session.commit()
    update.message.reply_text('Cleared 🧼')


def admin_add_new_user(update: Update, context: CallbackContext):

    key, value = parse_command(update)
    print('add')

    name = update.message.chat.username
    mail = value
    chat_id = update.message.chat_id
    print(name,mail,chat_id)

    new_data = User(name,mail,chat_id)
    db.session.add(new_data)
    db.session.commit()
    update.message.reply_text('Saved 💾')




