import time
import datetime
from random import choice
from glob import glob


from telegram import ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, RegexHandler
import ephem

from handlers import command_start, command_calc, command_cities, command_elephant, command_next_full_moon, command_planet, command_wordcount

from utils import get_planet_info, test_new_city, talk_with_ai
from my_loger import config_loggin, my_loger
import bot_settings 

def main():
    # @DimDim_bot
        
    config_loggin()
    my_loger("The 'Bot' started")
    
    mybot = Updater(bot_settings.BOT_ID, request_kwargs=bot_settings.PROXY)

    dp = mybot.dispatcher

    dp.add_handler(CommandHandler("start", command_start))
    dp.add_handler(CommandHandler("calc", command_calc))
    dp.add_handler(CommandHandler("cities", command_cities))
    dp.add_handler(CommandHandler("elephant", command_elephant))
    dp.add_handler(CommandHandler("next_full_moon", command_next_full_moon))
    dp.add_handler(CommandHandler("planet", command_planet))
    dp.add_handler(CommandHandler("wordcount", command_wordcount))

    dp.add_handler(RegexHandler("^Прислать слоника$",command_elephant))
    dp.add_handler(RegexHandler("^Когда полнолуние$",command_next_full_moon))
    dp.add_handler(RegexHandler("^Начать игру в города$",command_cities))
    
    # Важно, что бы следующая строка была после всех "dp.add_handler(CommandHandler(",
    # иначе она будет перехватывать все сообщения первой.
    dp.add_handler(MessageHandler(Filters.text, talk_with_ai))
    test_new_city() # Иницируем список горродов.

    mybot.start_polling()
    mybot.idle()

main()
