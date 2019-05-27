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
    my_loger("Got a command /planet with name: " + update.message.text)
    message_text = update.message.text.strip()
    planet_name = set(message_text.split(" "))
    planet_name.discard("")
    planet_name.discard("/planet")
    planet_name = list(planet_name)[0]
    my_loger("Got a command /planet with name: " + planet_name)
    planet_info = get_planet_info(planet_name)
    if not planet_info:
        response = "Птанеты с таким именем не найдено..."
    else:
        response = "Планета {} сейчас находится в созвездии {}".format(planet_name,planet_info)

    bot.send_message(chat_id=update.message.chat_id, text=response)

    my_loger("Answer: " + response)

def command_start(bot, update):
    # Получили сомманду /start
    log_text = "Got a command: /start"
    my_loger(log_text)
    update.message.reply_text("You can use command /planet pn (where 'pn' - planet name) if you want to get information about planet.")

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
    my_loger("Program started")
    
    mybot = Updater("807610709:AAHxSZ2MGfEUuOi2_Oj8bv4wKCYkJQzeVAI", request_kwargs=PROXY)

    dp = mybot.dispatcher
    dp.add_handler(CommandHandler("start", command_start))
    dp.add_handler(CommandHandler("planet", command_planet))
    dp.add_handler(MessageHandler(Filters.text, talk_to_me))

    mybot.start_polling()
    mybot.idle()

main()
