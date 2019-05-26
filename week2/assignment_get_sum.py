# -*- coding: utf-8 -*-
"""
Created on Sun May 26 22:10:41 2019

@author: Dim-Dim
"""

def get_summ(num_one, num_two):
    try:
        num_one = int(num_one)
        num_two = int(num_two)
        return(num_one + num_two)
    except ValueError:
        print("Не удалось привести одно из переданных значений к int: '{}' или '{}'".format(num_one, num_two))
        return(0)
    

print(get_summ(1, 2))
print(get_summ(10.2, 2.222))
print(get_summ("Слово", 2.222))