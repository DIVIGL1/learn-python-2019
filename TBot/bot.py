from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import logging
import apiai
import json
import ephem
import datetime


PROXY = {'proxy_url': 'socks5://t1.learn.python.ru:1080',
    'urllib3_proxy_kwargs': {'username': 'learn', 'password': 'python'}}

ALL_PLANETS = {
        'Mercury': 'Mercury', "Меркурий": 'Mercury', 
        'Venus': 'Venus', "Венера": 'Venus', 
        'Mars': 'Mars', "Марс": 'Mars', 
        'Jupiter': 'Jupiter', "Юритер": 'Jupiter', 
        'Saturn': 'Saturn', "Сатурн": 'Saturn', 
        'Uranus': 'Uranus', "Уран": 'Uranus', 
        'Neptune': 'Neptune', "Нептун": 'Neptune', 
        'Pluto': 'Pluto', "Плутон": 'Pluto', 
        'Sun': 'Sun', "Солнце": 'Sun', 
        'Moon': 'Moon', "Луна": 'Moon', 
        'Phobos': 'Phobos', "Фобос": 'Phobos', 
        'Deimos': 'Deimos', "Деймос": 'Deimos', 
        'Io': 'Io', "Ио": 'Io', 
        'Ganymede': 'Ganymede', "Ганимед": 'Ganymede',
        'Callisto': 'Callisto', "Калисто": 'Callisto',
        'Mimas': 'Mimas', "Мимас": 'Mimas', 
        'Enceladus': 'Enceladus', "Энцелад": 'Enceladus', 
        'Tethys': 'Tethys', "Тефия": 'Tethys',
        'Dione': 'Dione', "Диона": 'Dione', 
        'Rhea': 'Rhea', "Рея": 'Rhea', 
        'Titan': 'Titan', "Титан": 'Titan', 
        'Hyperion': 'Hyperion', "Гипкрион": 'Hyperion', 
        'Iapetus': 'Iapetus', "Япет": 'Iapetus', 
        'Ariel': 'Ariel', "Ариэль": 'Ariel', 
        'Umbriel': 'Umbriel', "Умбриэль": 'Umbriel', 
        'Titania':'Titania', "Титания": 'Titania', 
        'Oberon': 'Oberon', "Оберон": 'Oberon', 
        'Miranda': 'Miranda', "Миранда": 'Miranda'
        }

#PROXY = {'proxy_url': 'socks5://localhost:9050'} 

def get_planet_info(planet_name,year=0,month=0,day=0):
    thisday = datetime.datetime.now()
    if year==0: year = thisday.year
    if month==0: month = thisday.month
    if day==0: day = thisday.day
    date4planet = "{0}/{1:0>2}/{2:0>2}".format(year,month,day)
    planet_name = planet_name.lower().replace(' ', '').title()
    method_name = ALL_PLANETS.get(planet_name,"")
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
        response = "Птанеты с таким именем не найдено..."
    else:
        response = "{} сейчас находится в созвездии {}".format(planet_name,planet_info)

    bot.send_message(chat_id=update.message.chat_id, text=response)

    my_loger("Answer: " + response)

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
    except (ValueError,IndexError):
        param_date = datetime.datetime.now()
        bot.send_message(chat_id=update.message.chat_id, text="Вы ввели не правильную дату!")

    my_loger("Got a command /next_full_moon with date: " + param_date.strftime('%Y-%m-%d'))
    response = ephem.next_full_moon(param_date)
    response = "Ближайшее к {} новолуние состося {}".format(param_date.strftime('%Y-%m-%d'),response.datetime().strftime('%Y-%m-%d'))

    bot.send_message(chat_id=update.message.chat_id, text=response)

    my_loger("Answer: " + response)

def command_start(bot, update):
    # Получили сомманду /start
    log_text = "Got a command: /start"
    my_loger(log_text)
    message = \
        "1. /planet pn (where 'pn' - planet name) helps you want to get information about planet." + \
        "\n" + \
        "2. /wordcount sentance counts words :-)" + \
        "\n" + \
        "3. /next_full_moon date - calculates nearest full moon after date."

    update.message.reply_text(message)

def talk_to_me(bot, update):
    # Получили сообщение введённое пользователем в клиенте и залогим его:
    message_text = update.message.text.strip()
    my_loger("Got a user text: " + update.message.text)
    if message_text.lower()[:8]=="/planet ":
        planet_name = set(message_text.split(" "))
        planet_name.discard("")
        planet_name.discard("/planet")
        planet_name = list(planet_name)[0]
        planet_info = get_planet_info(planet_name)
        if not planet_info:
            response = "Птанеты с таким именем не найдено..."
        else:
            response = "Планета {} сейчас находится в созвездии {}".format(planet_name,planet_info)
    else:
        # Подключим ИИ с dialogflow.com и отправим запрос:
        client_access_token = '596138ef4ca148c3989ba7ead4091cd6'
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
    
    mybot = Updater("807610709:AAHxSZ2MGfEUuOi2_Oj8bv4wKCYkJQzeVAI", request_kwargs=PROXY)

    dp = mybot.dispatcher
    dp.add_handler(CommandHandler("start", command_start))
    dp.add_handler(CommandHandler("planet", command_planet))
    dp.add_handler(CommandHandler("wordcount", command_wordcount))
    dp.add_handler(CommandHandler("next_full_moon", command_next_full_moon))
    
    dp.add_handler(MessageHandler(Filters.text, talk_to_me))

    mybot.start_polling()
    mybot.idle()

main()
