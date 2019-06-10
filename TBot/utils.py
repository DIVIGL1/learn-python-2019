import os
import datetime
import pandas as pd
import json
from random import choice


import apiai
import ephem

from my_loger import my_loger
import bot_settings

cities_list = {}

def get_planet_info(planet_name,year=0,month=0,day=0):
    thisday = datetime.datetime.now()
    if year==0: year = thisday.year
    if month==0: month = thisday.month
    if day==0: day = thisday.day
    date4planet = "{0}/{1:0>2}/{2:0>2}".format(year,month,day)
    planet_name = planet_name.lower().replace(' ', '').title()
    method_name = bot_settings.ALL_PLANETS.get(planet_name,"")
    planet = getattr(ephem, method_name)(date4planet)
    if planet=="": return("")
    return (ephem.constellation(planet)[1])

def test_new_city(city_name="InitCityList"):
    global cities_list
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
        # Время ответа Бота. Последний правильный ответ хранится в bot_settings.last_mentioned_city
        for one_city_name in cities_list.keys():
            if (cities_list[one_city_name]==0) and (one_city_name[0].lower()==bot_settings.last_mentioned_city[-1].lower()):
                print("Bot answer:",one_city_name)
                cities_list[one_city_name]==1
                bot_settings.last_mentioned_city = one_city_name.lower().capitalize()
                return(True,"Я назову город '{}'. С Вас город на '{}'".format(bot_settings.last_mentioned_city,bot_settings.last_mentioned_city[-1].upper()))
        return(False, "{} Я не знаю городов на букву '{}'. Вы выиграли! Поздравляю!".format(bot_settings.emo_smile,bot_settings.last_mentioned_city[-1].upper()))
    else:
        # Это значит, что передан город от пользователя и его надо проверить.
        city_name = city_name.lower().capitalize()
        if not bot_settings.last_mentioned_city=="":
            if not (city_name[0].lower()==bot_settings.last_mentioned_city[-1].lower()):
                return(False,"{} Город должен начинаться с буквы '{}'! Попробуйте ещё раз.".format(bot_settings.emo_smile,bot_settings.last_mentioned_city[-1].upper()))
        used_type = cities_list.get(city_name,-1)
        if used_type==-1:
            return(False,"{} Такого города НЕ существует! Попробуйте ещё раз.".format(bot_settings.emo_smile))
        elif used_type==0:
            # Сохраним последний правильный город и пометим его как использованный.
            bot_settings.last_mentioned_city = city_name
            cities_list[city_name] = 1
            return(True,"'{}'. Такой город существует!".format(city_name.lower().capitalize()))
        elif used_type==1:
            return(False,"'{} {}'. Этот город уже называли! Выберите другой.".format(bot_settings.emo_smile,city_name.lower().capitalize()))
        else:
            return(False,"Что-то пошло не так.... У меня в коде ошибка!")

def talk_with_ai(bot, update):
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
