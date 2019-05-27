# Вывести последнюю букву в слове
word = 'Архангельск'
print("Последняя буква: ",word[-1])

# Вывести количество букв а в слове
word = 'Архангельск'
print("Количество букв: ",len(word))

# Вывести количество гласных букв в слове
word = 'Архангельск'
len_start = len(word)
word = word.lower()
for letter in list("уеыаоэяию"):
    word = word.replace(letter,"")
print("Количество гласных букв: ",len_start-len(word))


# Вывести количество слов в предложении
sentence = 'Мы приехали в гости'

print("Количество слов в предложении: ",len(sentence.split(" ")))


# Вывести первую букву каждого слова на отдельной строке
sentence = 'Мы приехали в гости'
print("Для слова "+sentence+" выводим первую букву каждого слова на отдельной строке:") 
for word in sentence.split(" "):
    print(word[0])


# Вывести усреднённую длину слова.
sentence = 'Мы приехали в гости'
sum_letters = 0
words_list = sentence.split(" ")
for word in words_list:
    sum_letters += len(word)
print("Усреднённая длинна слов: ",sum_letters/len(words_list))