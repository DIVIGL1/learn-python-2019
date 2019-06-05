import apiai
import datetime
import ephem
import logging
import json
import os
import pandas as pd
import time

from glob import glob
from random import choice

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

import bot_settings

last_mentioned_city = ""
cities_list = {}

def command_elephant(bot, update):
    # Отправим картинку со слоном:
    elephant_list = glob("TBot/images/elephant*.jpg")
    elephant_pict = choice(elephant_list)
    bot.send_photo(chat_id=update.message.chat_id, photo=open(elephant_pict,"rb"))
            
def get_planet_info(planet_name,year=0,month=0,day=0):
    thisday = datetime.datetime.now()
    if year==0: year = thisday.year
    if month==0: month = thisday.month
    if day==0: day = thisday.day
    date4planet = "{0}/{1:0>2}/{2:0>2}".format(year,month,day)
    planet_name = planet_name.lower().replace(' ', '').title()
    method_name = bot_settings.ALL_PLANETS.get(planet_name,"")
    planet = getattr(ephem,method_name)(date4planet)
    if planet=="": return("")
    return (ephem.constellation(planet)[1])

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

def test_new_city(city_name="InitCityList"):
    global last_mentioned_city, cities_list
    if city_name=="InitCityList":
        ''' Получим из csv-файла словарь типа:
            {   'Москва': 0,
                'Абрамцево': 0,
                'Алабино': 0,
                'Апрелевка': 0,
                'Архангельское': 0}
        '''
        if os.path.isfile("Cities.csv"):
            city_file_name = "Cities.csv"
        elif os.path.isfile("TBot/Cities.csv"):
            city_file_name = "TBot/Cities.csv"
        else:
            my_loger("Не найден файл с перечнем городов!")
        cities_list = pd.read_csv(city_file_name, encoding="cp1251", index_col="name", sep=";")
        cities_list["used"] = 0 # На всякий случай обнулим.
        cities_list = cities_list.to_dict()["used"]
        print("< ЗАГРУЖЕН СПИСОК ГОРОДОВ >")
        return(True,"")
    elif city_name=="GetNewCity":
        # Время ответа Бота. Последний правильный ответ хранится в last_mentioned_city
        for one_city_name in cities_list.keys():
            if (cities_list[one_city_name]==0) and (one_city_name[0].lower()==last_mentioned_city[-1].lower()):
                print("Bot answer:",one_city_name)
                cities_list[one_city_name]==1
                last_mentioned_city = one_city_name.lower().capitalize()
                return(True,"Я назову город '{}'. С Вас город на '{}'".format(last_mentioned_city,last_mentioned_city[-1].upper()))
        return(False, "Я не знаю городов на букву '{}'. Вы выиграли! Поздравляю!".format(last_mentioned_city[-1].upper()))
    else:
        # Это значит, что передан город от пользователя и его надо проверить.
        city_name = city_name.lower().capitalize()
        if not last_mentioned_city=="":
            if not (city_name[0].lower()==last_mentioned_city[-1].lower()):
                return(False,"Город должен начинаться с буквы '{}'! Попробуйте ещё раз.".format(city_name[0].upper()))
        used_type = cities_list.get(city_name,-1)
        if used_type==-1:
            return(False,"Такого города НЕ существует! Попробуйте ещё раз.")
        elif used_type==0:
            # Сохраним последний правильный город и пометим его как использованный.
            last_mentioned_city = city_name
            cities_list[city_name] = 1
            return(True,"'{}'. Такой город существует!".format(city_name.lower().capitalize()))
        elif used_type==1:
            return(False,"'{}'. Этот город уже называли! Выберите другой.".format(city_name.lower().capitalize()))
        else:
            return(False,"Что-то пошло не так.... У меня в коде ошибка!")

def command_cities(bot, update):
    global last_mentioned_city
    # Получили сомманду c наименованием города:
    message_text = update.message.text.strip()
    city_name = message_text.replace("/cities","").strip().capitalize()
    if city_name=="":
        my_loger("Got a command /cities without city.")
        bot.send_message(chat_id=update.message.chat_id, text="Вы не указали наименование города.")
        return()
    my_loger("Got a command /cities with city: " + city_name)
    # Проверим город на наличие и повторное использование:
    ret_code, ret_text = test_new_city(city_name)
    bot.send_message(chat_id=update.message.chat_id, text=ret_text)
    if ret_code:
        my_loger("Good answer: " + city_name)
        # Сообщение о том какой город был назван.
        bot.send_message(chat_id=update.message.chat_id, text="Он заканчивается на букву '{}'".format(city_name[-1].upper()))
        bot.send_message(chat_id=update.message.chat_id, text="Тогда я называю город... секундочку...")
        time.sleep(1)
        ret_code, ret_text = test_new_city("GetNewCity")
        bot.send_message(chat_id=update.message.chat_id, text=ret_text)
        if ret_code:
            pass
        else:
            test_new_city()
            last_mentioned_city = ""
            bot.send_message(chat_id=update.message.chat_id, text="Игра будут начата с самого начала.")
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
    message_text = update.message.text.strip()
    param_date = set(message_text.split(" "))
    param_date.discard("")
    param_date.discard("/next_full_moon")
    try:
        param_date = list(param_date)[0]
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
    global last_mentioned_city
    last_mentioned_city = ""

    log_text = "Got a command: /start"
    my_loger(log_text)
    message = \
        "1. /planet pn  - (where 'pn' - planet name) helps you want to get information about planet.\n" + \
        "2. /wordcount sentance  - counts words :-)\n" + \
        "3. /next_full_moon date  - calculates nearest full moon after date.\n" + \
        "4. /cities city  - Game 'city'\n" + \
        "5. /calc 2ne  - (where '2ne' - 2-number expression) calculates 2-number expressions\n" +\
        "6. /elephant  - shows you an elephant photo."

    update.message.reply_text(message)
    test_new_city() # Иницируем список горродов.

def talk_to_me(bot, update):
    # Получили сообщение введённое пользователем в клиенте и залогим его:
    my_loger("Got a user text: " + update.message.text)
    # Подключим ИИ с dialogflow.com и отправим запрос:
    client_access_token = bot_settings.AI_ID
    request = apiai.ApiAI(client_access_token).text_request()
    request.lang = 'ru' # На каком языке будет послан запрос
    request.session_id = 'BatlabAIBot' # ID Сессии диалога (нужно, чтобы потом учить бота)
    request.query = update.message.text # Посылаем запрос к ИИ с сообщением от юзера
    # Обработаем полученный запрос:
    responseJson = json.loads(request.getresponse().read().decode('utf-8'))
    response = responseJson['result']['fulfillment']['speech'] # Разбираем JSON и вытаскиваем ответ
    # Если есть ответ от бота - присылаем юзеру, если нет - бот его не понял
    if not response:
        response = 'Я Вас не совсем понял!'
    bot.send_message(chat_id=update.message.chat_id, text=response)

    my_loger("AI answer: " + response)

def my_loger(log_text):
    print(log_text)
    logging.info(log_text)
    
def main():
    logging.basicConfig(format='%(name)s - %(levelname)s - %(message)s',
                        level=logging.INFO,
                        filename='bot.log'
                        )
    my_loger("The 'Bot' started")
    
    mybot = Updater(bot_settings.BOT_ID, request_kwargs=bot_settings.PROXY)

    dp = mybot.dispatcher
    dp.add_handler(CommandHandler("start", command_start))
    dp.add_handler(CommandHandler("planet", command_planet))
    dp.add_handler(CommandHandler("wordcount", command_wordcount))
    dp.add_handler(CommandHandler("next_full_moon", command_next_full_moon))
    dp.add_handler(CommandHandler("cities", command_cities))
    dp.add_handler(CommandHandler("calc", command_calc))
    dp.add_handler(CommandHandler("elephant", command_elephant))
    
    # Важно, что бы следующая строка была после всех "dp.add_handler(CommandHandler(",
    # иначе она будет перехватывать все сообщения первой.
    dp.add_handler(MessageHandler(Filters.text, talk_to_me))
    test_new_city() # Иницируем список горродов.

    mybot.start_polling()
    mybot.idle()

main()
