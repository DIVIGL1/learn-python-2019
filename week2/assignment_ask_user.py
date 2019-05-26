# -*- coding: utf-8 -*-
"""
Created on Sun May 26 18:19:12 2019

@author: Dim-Dim
"""
A_AND_Q = { "": "Задайте, пожалуйста, вопрос.",
           "как дела": "Нормально!",
           "что делаешь": "Программирую.",
           "ты бот": "Угу...",
           "ты робот": "Да.",
           "что": "Что 'Что?'",
           "ты человек": "Нет!!!" }

def ask_user():
    try:
        while True:
            print("Как дела?")
            user_a = input()
            user_a = user_a.replace(" ","").lower()
            if user_a=="хорошо": break
    
        print("Теперь ты спроси что-нибудь!")
        while True:
            user_q = input()
            user_q = user_q.lower().strip().replace("?","")
            print(A_AND_Q.get(user_q,"Что-то я Вас не понимаю, уточните, пожалуйста, вопрос?"))
    except KeyboardInterrupt:
        print("Пока!")

ask_user()
