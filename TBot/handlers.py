import time
from random import choice
import datetime

from glob import glob

from telegram import ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, RegexHandler
import ephem

import bot_settings
from my_loger import my_loger, config_loggin
from utils import get_planet_info, test_new_city, talk_with_ai

def command_elephant(bot, update):
    # Отправим картинку со слоном:
    elephant_list = glob("TBot/images/elephant*.jpg")
    elephant_pict = choice(elephant_list)
    bot.send_photo(chat_id=update.message.chat_id, photo=open(elephant_pict,"rb"))
            
def command_planet(bot, update):
    # Получили сомманду для вывода информации о планете:
    message_text = update.message.text.strip()
    planet_name = set(message_text.split(" "))
    planet_name.discard("")
    planet_name.discard("/planet")
    planet_name = list(planet_name)[0].capitalize()
    my_loger("Got a command /planet with name: " + planet_name)
    planet_info = get_planet_info(planet_name)
    if not planet_info:
        response = "Планеты с таким именем не найдено..."
    else:
        response = "{} сейчас находится в созвездии {}".format(planet_name,planet_info)

    bot.send_message(chat_id=update.message.chat_id, text=response)

    my_loger("Answer: " + response)

def command_cities(bot, update):
    # Получили сомманду c наименованием города:
    message_text = update.message.text.strip()
    city_name = message_text.replace("/cities","").strip().capitalize()
    if ( \
            ((city_name=="") and (bot_settings.last_mentioned_city=="")) \
            or (city_name==bot_settings.PLAY_CITY_TEXT) \
        ):
        # Установим признаком того, что это начало игры,
        # а bot должен дать первое слово
        bot_settings.last_mentioned_city = "Нижний Новгород"
        message = "{} Начинам игру в города.\nЯ называю город: {}".format(bot_settings.emo_smile, bot_settings.last_mentioned_city)
        bot.send_message(chat_id=update.message.chat_id, text=message)
        return()
    elif city_name=="":
        my_loger("Got a command /cities without city.")
        bot.send_message(chat_id=update.message.chat_id, text="Вы не указали наименование города.\n(для рестарта игры напечатайте /start а потом /cities)")
        return()
    my_loger("Got a command /cities with city: " + city_name)

    # Проверим город на наличие и повторное использование:
    ret_code, ret_text = test_new_city(city_name=city_name)
    bot.send_message(chat_id=update.message.chat_id, text=ret_text)
    if ret_code:
        my_loger("Good answer: " + city_name)
        # Сообщение о том какой город был назван.
        bot.send_message(chat_id=update.message.chat_id, text="Он заканчивается на букву '{}'".format(city_name[-1].upper()))
        bot.send_message(chat_id=update.message.chat_id, text="Тогда я называю город... секундочку...")
        time.sleep(1)
        ret_code, ret_text = test_new_city(city_name="GetNewCity")
        bot.send_message(chat_id=update.message.chat_id, text=ret_text)
        if ret_code:
            pass
        else:
            test_new_city()
            bot_settings.last_mentioned_city = ""
            bot.send_message(chat_id=update.message.chat_id, text="Игра запущена с самого начала.")
    else:
        my_loger("Bad answer: " + city_name)
        # Сообщение об ошибочно названном городе уже было отправлено перед if.

def command_calc(bot, update):
    # Получили сомманду c двумя числами:
    message_text = update.message.text.strip()
    expression_str = message_text.replace("/calc","").strip().capitalize()
    if expression_str=="":
        my_loger("Got a command /calc without 2-number expression.")
        bot.send_message(chat_id=update.message.chat_id, text="Вы не указали выражение из двух чисел.")
        return()
    expression_str = expression_str.replace(" ","")
    my_loger("Got a command /calc with expression: " + expression_str)
    for one_sign in ["+","-","*","/"]:
        if one_sign in expression_str:
            operation_sign = one_sign
            break
    number1 = expression_str.split(operation_sign)[0]
    number2 = expression_str.split(operation_sign)[1]
    if not ((number1.upper()==number1.lower()) and (number2.upper()==number2.lower())):
        bot.send_message( 
            chat_id=update.message.chat_id, 
            text="В этом калькулятоне в качестве аргументов можно использовать только числа!")
        return()

    # Протестируем на возможные ошибки:
    try:
        expression_result = eval(number1+operation_sign+number2)
        bot.send_message( 
            chat_id=update.message.chat_id, 
            text="Результатом вычисления выражения {} {} {} будет {}".format(number1,operation_sign,number2,expression_result))
    except ZeroDivisionError:
        bot.send_message( 
            chat_id=update.message.chat_id, 
            text="Вычислить выражение {} {} {} нельзя - деление на ноль.".format(number1,operation_sign,number2))

def command_wordcount(bot, update):
    # Получили сомманду для вывода информации о количестве слов в предложении:
    message_text = update.message.text.strip()
    sentance = set(message_text.split(" "))
    sentance.discard("")
    sentance.discard("/wordcount")
    my_loger("Got a command /wordcount with sentance: " + " ".join(list(sentance)))
    if len(sentance)==0:
        response = "Не введено ни одного слова."
    else:
        response = "Количество введенных слов - {} шт.".format(len(sentance))

    bot.send_message(chat_id=update.message.chat_id, text=response)

    my_loger("Answer: " + response)

def command_next_full_moon(bot, update):
    # Получили сомманду для вывода информации о ближайшем полнолунии:
    message_text = update.message.text.replace(bot_settings.FULL_MOON_TEXT,"").replace("/next_full_moon","").strip()
    if message_text.replace(" ","")=="":
        param_date = datetime.datetime.now()
    else:
        param_date = set(message_text.split(" "))
        param_date.discard("")
        param_date = list(param_date)[0]
        try:
            param_date = datetime.datetime.strptime(param_date, '%Y/%m/%d')
        except (ValueError, IndexError):
            param_date = datetime.datetime.now()
            bot.send_message(chat_id=update.message.chat_id, text="Вы ввели не правильную дату!")

    my_loger("Got a command /next_full_moon with date: " + param_date.strftime('%Y-%m-%d'))
    response = ephem.next_full_moon(param_date)
    response = "Ближайшее к {} новолуние состоится {}".format(param_date.strftime('%Y-%m-%d'),response.datetime().strftime('%Y-%m-%d'))

    bot.send_message(chat_id=update.message.chat_id, text=response)

    my_loger("Answer: " + response)

def command_start(bot, update):
    # Получили сомманду /start
    bot_settings.last_mentioned_city = ""

    log_text = "Got a command: /start"
    my_loger(log_text)
    message = "Hello {}\n\n".format(bot_settings.emo_smile) + \
        "1. /planet pn  - (where 'pn' - planet name) helps you want to get information about planet.\n" + \
        "2. /wordcount sentance  - counts words :-)\n" + \
        "3. /next_full_moon date  - calculates nearest full moon after date.\n" + \
        "4. /cities city  - Game 'city'\n" + \
        "5. /calc 2ne  - (where '2ne' - 2-number expression) calculates 2-number expressions\n" +\
        "6. /elephant  - shows you an elephant photo."

    my_keyboard = ReplyKeyboardMarkup(bot_settings.MY_KEYBOARD)
    update.message.reply_text(message, reply_markup=my_keyboard)

    test_new_city() # Иницируем список горродов.