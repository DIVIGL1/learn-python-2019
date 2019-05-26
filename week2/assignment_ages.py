# -*- coding: utf-8 -*-
"""
Created on Sun May 26 18:19:12 2019

@author: Dim-Dim
"""
def between(data,n1,n2):
    return(data>=n1 and data<=n2)

def iif(bool_value,v1,v2):
    return(v1 if bool_value else v2)

def test_age(nage):
    if between(user_data,3,6):
        return("учиться в детском саду")
    elif between(user_data,7,17):
        return("учиться в школе")
    elif between(user_data,18,23):
        return("учиться в ВУЗе")
    else:
        return("работать")
        

print("Введите, пожалуйста, свой возраст: ")
user_data = 0
while user_data==0:
    user_data = int(input())
    if user_data<=2: print("Вы ввели не правильный возраст. Попробуйте ещё раз.")
    else: break
    user_data = 0
    
ret_value = test_age(user_data)
print("Если ваш возраст составляет {} {}, то Вы должны {}.".format(user_data,iif(user_data<5,"года","лет"),ret_value))
