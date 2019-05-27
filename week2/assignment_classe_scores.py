# -*- coding: utf-8 -*-
"""
Created on Mon May 27 18:28:37 2019

@author: Dim-Dim
"""

# Создать список из словарей с оценками учеников разных классов школы вида:
# [{'school_class': '4a', 'scores': [3,4,4,5,2]}, ...]
# Посчитать и вывести средний балл по всей школе.
# Посчитать и вывести средний балл по каждому классу.

CLASSES_AND_SCORES = [
            {'school_class': '4a', 'scores': [3,4,4,5,2]},
            {'school_class': '4б', 'scores': [5,5,4,5,5]},
            {'school_class': '4в', 'scores': [4,4,4,4,4]},
            {'school_class': '4г', 'scores': [3,4,4,3,4]},
            {'school_class': '5a', 'scores': [3,3,4,5,3]},
            {'school_class': '5б', 'scores': [4,5,4,5,4]},
            {'school_class': '5в', 'scores': [3,4,5,4,3]}
        ]

# Выведем средний балл по всей школе:
sum_scores = 0
scores_counter = 0
for one_class in CLASSES_AND_SCORES:
    for score_in_class in one_class["scores"]:
        sum_scores += score_in_class
        scores_counter += 1

print("Средняя оценка по всей школе: {}".format(sum_scores/scores_counter))

print("Список средних оценок по каждому классу")
print("---------------------------------------")

for one_class in CLASSES_AND_SCORES:
    sum_scores = 0
    scores_counter = 0
    for score_in_class in one_class["scores"]:
        sum_scores += score_in_class
        scores_counter += 1
    print("класс: {} \t\tср. оценка: {}".format(one_class["school_class"],sum_scores/scores_counter))

        