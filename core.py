
import os
from telegram import Bot, ParseMode
from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler
from telegram.ext import Filters
from telegram.ext import ConversationHandler
from telegram.ext import CallbackContext
from telegram import Update, ReplyKeyboardRemove, ReplyKeyboardMarkup

import schedule

from proxy.prox import TG_TOKEN, TG_API_URL
from admin import error_callback, do_admin_test,a_legend, admin_add_new_user, list_all, id_del_ask, list_clear
from config import welcome, do_user_test, legend ,conv_handler_var,anketa_conv_handler_var,\
    reddit_api_test,api_classic,api_flask,api_flask_auth,adv_sub,no_adv_sub,reminder




# СОЗДАЙ КЛАСС БОТА, ПОТОМ ЕГО ОБЪЕКТ И ИЗ НЕГО УЖЕ ТАЩИ ЕГО ФУНКЦИИ!!!






# Crate bot core
def main():


    bot = Bot(token=TG_TOKEN, base_url=TG_API_URL)
    updater = Updater(bot=bot, use_context=True)

    reminder(updater)

    updater.dispatcher.add_handler(CommandHandler('test_a', do_admin_test))
    updater.dispatcher.add_handler(CommandHandler('a_help', a_legend))
    updater.dispatcher.add_handler(CommandHandler('a_add', admin_add_new_user))
    updater.dispatcher.add_handler(CommandHandler('a_list', list_all))
    updater.dispatcher.add_handler(CommandHandler('a_id_del', id_del_ask))
    updater.dispatcher.add_handler(CommandHandler('a_all_del', list_clear))


    updater.dispatcher.add_handler(MessageHandler(Filters.status_update.new_chat_members, welcome))

    updater.dispatcher.add_handler(CommandHandler('test_u', do_user_test))
    updater.dispatcher.add_handler(CommandHandler('help', legend))
    updater.dispatcher.add_handler(CommandHandler('api_test', reddit_api_test))
    updater.dispatcher.add_handler(CommandHandler('api_c', api_classic))
    updater.dispatcher.add_handler(CommandHandler('adv_simple', api_flask))
    updater.dispatcher.add_handler(CommandHandler('adv', api_flask_auth))
    updater.dispatcher.add_handler(CommandHandler('adv_sub', adv_sub))
    updater.dispatcher.add_handler(CommandHandler('no_adv_sub', no_adv_sub))


    updater.dispatcher.add_handler(conv_handler_var)
    updater.dispatcher.add_handler(anketa_conv_handler_var)

    updater.dispatcher.add_error_handler(error_callback)

    updater.start_polling()
    updater.idle()



# Activate reminder func
#reminder()

if __name__ == '__main__':
    main()
