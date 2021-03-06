# Задание 1
# Необходимо вывести имена всех учеников из списка с новой строки

print("Необходимо вывести имена всех учеников из списка с новой строки:")
names = ['Оля', 'Петя', 'Вася', 'Маша']
for one_name in names:
    print(one_name)

# Задание 2
# Необходимо вывести имена всех учеников из списка, рядом с именем показать количество букв в нём.

print("\nНеобходимо вывести имена всех учеников из списка, рядом с именем показать количество букв в нём:")
names = ['Оля', 'Петя', 'Вася', 'Маша']
for one_name in names:
    print(one_name,"->",len(one_name))


# Задание 3
# Необходимо вывести имена всех учеников из списка, рядом с именем вывести пол ученика

print("\nНеобходимо вывести имена всех учеников из списка, рядом с именем вывести пол ученика:")
is_male = {
  'Оля': False,  # если True, то пол мужской
  'Петя': True,
  'Вася': True,
  'Маша': False,
}
names = ['Оля', 'Петя', 'Вася', 'Маша']
for one_name in names:
    print(one_name,"->","М" if is_male[one_name] else "Ж")


# Задание 4
# Даны группу учеников. Нужно вывести количество групп и для каждой группы – количество учеников в ней
# Пример вывода:
# Всего 2 группы.
# В группе 2 ученика.
# В группе 3 ученика.

print("\nДаны группу учеников. Нужно вывести количество групп и для каждой группы – количество учеников в ней:")
groups = [
  ['Вася', 'Маша'],
  ['Оля', 'Петя', 'Гриша'],
]
print("Всего групп: "+str(len(groups)))
for one_group in groups:
    print("В группе {} учениека.".format(len(one_group)))


# Задание 5
# Для каждой пары учеников нужно с новой строки перечислить учеников, которые в неё входят.
# Пример:
# Группа 1: Вася, Маша
# Группа 2: Оля, Петя, Гриша

print("\nДля каждой пары учеников нужно с новой строки перечислить учеников, которые в неё входят:")
groups = [
  ['Вася', 'Маша'],
  ['Оля', 'Петя', 'Гриша'],
]
for j in range(len(groups)):
    print("Группа {}: {}".format(j+1,", ".join(groups[j])))