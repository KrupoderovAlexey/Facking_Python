import numpy as np

alpha = {"Шарик": 4, "Тузик": 5, "Бука": 6}

class Dog:
    def __init__(self, name, age):
        self.name = name  # Атрибут объекта
        self.age = age    # Атрибут объекта

    # Метод класса (теперь отступ правильный)
    def bark(self):
        return f"{self.name} говорит: Гав!", f"{self.name} == {self.name}"

animal = []
for name, age in alpha.items():
    my_dog = Dog(name, age)
    animal.append(my_dog)

for i in range(3):
    print(animal[i].bark())

# 1. Создаем объект (экземпляр) класса Dog
my_dog = Dog("Шарик", 4)

# 2. Вызываем метод bark() и выводим результат
print(my_dog.bark())

# 3. Выводим отдельные атрибуты
print(f"Имя собаки: {my_dog.name}")
print(f"Возраст собаки: {my_dog.age}")

users = [] # Создаем пустой список

# Добавляем объекты по одному с помощью метода append
users.append(User("Алексей", 25))
users.append(User("Мария", 19))
