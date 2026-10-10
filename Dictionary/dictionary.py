# Вывод словаря по типу -> ключ : значение

def disp(dictionary, key) :
    return f"{key} : {dictionary[key]}"

sqares = {x : x**2 for x in range(10)}

for i in range(1, 10):
    print(disp(sqares, i))
