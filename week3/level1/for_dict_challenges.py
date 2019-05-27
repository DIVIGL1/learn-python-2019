# Задание 1
# Дан список учеников, нужно посчитать количество повторений каждого имени ученика.
print("Дан список учеников, нужно посчитать количество повторений каждого имени ученика:")
students = [
    {'first_name': 'Вася'},
    {'first_name': 'Петя'},
    {'first_name': 'Маша'},
    {'first_name': 'Маша'},
    {'first_name': 'Петя'},
]

unic_names = {}
for one_student in students:
    student_name_counter = unic_names.get(one_student['first_name'],0)
    unic_names.update({one_student['first_name']: student_name_counter+1})

for one_name in unic_names.keys():
    print("{}: {}".format(one_name,unic_names[one_name]))

# Пример вывода:
# Вася: 1
# Маша: 2
# Петя: 2


# Задание 2
# Дан список учеников, нужно вывести самое часто повторящееся имя.
print("\nДан список учеников, нужно вывести самое часто повторящееся имя:")
students = [
    {'first_name': 'Вася'},
    {'first_name': 'Петя'},
    {'first_name': 'Маша'},
    {'first_name': 'Маша'},
    {'first_name': 'Оля'},
]

def print_one_name(start_text,students):
    unic_names = {}
    for one_student in students:
        student_name_counter = unic_names.get(one_student['first_name'],0)
        unic_names.update({one_student['first_name']: student_name_counter+1})

    print_name = ""
    for one_name in unic_names.keys():
        if unic_names.get(one_name)>unic_names.get(print_name,0):
            print_name = one_name

    print(start_text+print_name)

print_one_name("Самое частое имя среди учеников: ",students)

# Пример вывода:
# Самое частое имя среди учеников: Маша

# Задание 3
# Есть список учеников в нескольких классах, нужно вывести самое частое имя в каждом классе.
print("\nЕсть список учеников в нескольких классах, нужно вывести самое частое имя в каждом классе:")
school_students = [
    [  # это – первый класс
        {'first_name': 'Вася'},
        {'first_name': 'Вася'},
    ],
    [  # это – второй класс
        {'first_name': 'Маша'},
        {'first_name': 'Маша'},
        {'first_name': 'Оля'},
    ]
]

for j in range(len(school_students)):
    print_one_name("Самое частое имя в классе {}: ".format(j+1),school_students[j])

# Пример вывода:
# Самое частое имя в классе 1: Вася
# Самое частое имя в классе 2: Маша


# Задание 4
# Для каждого класса нужно вывести количество девочек и мальчиков в нём.
print("\nДля каждого класса нужно вывести количество девочек и мальчиков в нём:")
school = [
    {'class': '2a', 'students': [{'first_name': 'Маша'}, {'first_name': 'Оля'}]},
    {'class': '3c', 'students': [{'first_name': 'Олег'}, {'first_name': 'Миша'}]},
]
is_male = {
    'Маша': False,
    'Оля': False,
    'Олег': True,
    'Миша': True,
}
# ???

def get_nums_girls_and_boys(students):
    gils, boys = 0, 0
    for one_student in students:
        if is_male[one_student["first_name"]]: boys += 1
        else: gils += 1
    return(gils, boys)

for one_class in school:
    girls,boys = get_nums_girls_and_boys(one_class["students"])
    print("В классе {} {} девочки и {} мальчика.".format(one_class["class"],girls,boys))
    

# Пример вывода:
# В классе 2a 2 девочки и 0 мальчика.
# В классе 3c 0 девочки и 2 мальчика.


# Задание 5
# По информации о учениках разных классов нужно найти класс, в котором больше всего девочек и больше всего мальчиков.
print("\nПо информации о учениках разных классов нужно найти класс, в котором больше всего девочек и больше всего мальчиков:")
school = [
    {'class': '2a', 'students': [{'first_name': 'Маша'}, {'first_name': 'Оля'}]},
    {'class': '3c', 'students': [{'first_name': 'Олег'}, {'first_name': 'Миша'}]},
]
is_male = {
    'Маша': False,
    'Оля': False,
    'Олег': True,
    'Миша': True,
}

# Иницируем значениями из мервого класса:
girls,boys = get_nums_girls_and_boys(school[0]["students"])
class_with_max_girls = [school[0]["class"],girls]
class_with_max_boys = [school[0]["class"],boys]
# Пробегаем все классы и сравниваем, выбирая максимальные:
for one_class in school:
    girls,boys = get_nums_girls_and_boys(one_class["students"])
    if class_with_max_girls[1]<girls: class_with_max_girls = [one_class["class"],girls]
    if class_with_max_boys[1]<boys: class_with_max_boys = [one_class["class"],boys]

print("Больше всего мальчиков в классе "+class_with_max_boys[0])
print("Больше всего девочек в классе "+class_with_max_girls[0])

# Пример вывода:
# Больше всего мальчиков в классе 3c
# Больше всего девочек в классе 2a