import numpy as np
import random as ran
# ------------------------------------------             Перезапись мужских фамилий на женские
with open('familii_man.txt', 'r', encoding='utf-8') as file:
    familii_man = [line.strip() for line in file]
familii_girl = []
for i in range(len(familii_man)):
    if (familii_man[i][-1] == "й"):
        familii_man_new = familii_man[i][:-2]
        familii_girl.append(familii_man_new + "ая")
    else:
        familii_girl.append(familii_man[i] + "a")
with open('familii_girl.txt', 'w', encoding='utf-8') as file:
    for familia in familii_girl:
        file.write(familia + '\n')
# ------------------------------------------             Перезапись мужских имен на отчества
with open('names_man.txt', 'r', encoding='utf-8') as file:
    names_man = [line.strip() for line in file]
surname_man = []
for i in range(len(names_man)):
    if (names_man[i][-1] == "й"):
        names_man_new = names_man[i][:-1]
        surname_man.append(names_man_new + "евич")
    else:
        surname_man.append(names_man[i] + "ович")
with open('surname_man.txt', 'w', encoding='utf-8') as file:
    for surname in surname_man:
        file.write(surname + '\n')
surname_girl = []
for i in range(len(names_man)):
    if (names_man[i][-1] == "й"):
        names_man_new = names_man[i][:-1]
        surname_girl.append(names_man_new + "евна")
    else:
        surname_girl.append(names_man[i] + "овна")
with open('surname_girl.txt', 'w', encoding='utf-8') as file:
    for surname in surname_girl:
        file.write(surname + '\n')
# ------------------------------------------             Создание массива женских имен
with open('names_girl.txt', 'r', encoding='utf-8') as file:
    names_girl = [line.strip() for line in file]
# ------------------------------------------             Создание массива полных имен
full_name_man = []
full_name_girl = []
def construct():
    fnm = ''.join(familii_man[ran.randint(0,len(familii_man)-1)]) + ' ' + ''.join(names_man[ran.randint(0,len(names_man)-1)]) + ' ' + ''.join(surname_man[ran.randint(0,len(surname_man)-1)])
    full_name_man.append(fnm)
    fng = ''.join(familii_girl[ran.randint(0,len(familii_girl)-1)]) + ' ' + ''.join(names_girl[ran.randint(0,len(names_girl)-1)]) + ' ' + ''.join(surname_girl[ran.randint(0,len(surname_girl)-1)])
    full_name_girl.append(fng)
for _ in range(250):
    construct()
full_name_people = full_name_girl + full_name_man
ran.shuffle(full_name_people)
ran.shuffle(full_name_people)
ran.shuffle(full_name_people)
# ------------------------------------------             Создание массива почт
rus = ['а', 'б', 'в', 'г', 'д', 'е', 'ё', 'ж', 'з', 'и', 'й', 'к', 'л', 'м', 'н', 'о', 'п', 'р', 'с', 'т', 'у', 'ф', 'х', 'ц', 'ч', 'ш', 'щ', 'ъ', 'ы', 'ь', 'э', 'ю', 'я']
lat = ['a', 'b', 'v', 'g', 'd', 'e', 'e', 'j', 'th', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'r', 's', 't', 'u', 'f', 'x', 'sk', 'ch', 'sh', 'sh', "", "i", "", "a", "ju", "ja"]
transliter = dict(zip(rus, lat))
g_g = "@gmail.com"
def translate(text):
    result = ""
    for char in text:
        result += transliter.get(char, char)
    return result
name_vs_post = {}
for i in range(len(full_name_people)):
    imya = full_name_people[i]
    res = translate(full_name_people[i].split()[0].lower()) + "." + translate(full_name_people[i].split()[1][0:3].lower()) + g_g
    name_vs_post[imya] = res
# ------------------------------------------             Создание массива полных номеров телефонов
oper = ["919", "950", "982", "952", "999", "995"]
num_tel = []
for i in range(len(full_name_people)):
    num = '8' + ran.choice(oper) + \
          str(ran.randint(100, 999)) + \
          str(ran.randint(10, 99)) + \
          str(ran.randint(10, 99))
    num_tel.append(num)
# ------------------------------------------             Создание массива дат рождения
dat = []
for i in range(len(full_name_people)):
    d = str(ran.randint(1, 30)) + ' ' + str(ran.randint(1, 12)) + ' ' + str(ran.randint(1960, 2010))
    dat.append(d)
# ------------------------------------------             Вывод
n = int(input())
def count():
    h = ran.randint(0,len(full_name_people)-1)
    print('\t')
    print(full_name_people[h], '----------',num_tel[ran.randint(0,len(num_tel)-1)], '----------', dat[ran.randint(0,len(dat)-1)], '----------', name_vs_post[full_name_people[h]])
for _ in range(n):
    count()
