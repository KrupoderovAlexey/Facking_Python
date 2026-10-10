import time

def repeat_action(action, times=4, interval=5, *args, **kwargs):
    """
    Выполняет переданную функцию action несколько раз.
    
    Параметры:
        action: функция, которую нужно выполнять
        times: количество повторений
        interval: пауза между выполнениями
        *args, **kwargs: аргументы для action
    """
    for i in range(times):
        print(f"--- Итерация {i+1} из {times} ---")
        action(*args, **kwargs)      # Выполняем переданную функцию
        if i < times - 1:            # Если не последняя
            print(f"Жду {interval} секунд...")
            time.sleep(interval)

# Использование с нашим запросом курса
import requests

def show_rate():
    response = requests.get("https://www.cbr-xml-daily.ru/daily_json.js")
    rate = response.json()["Valute"]["USD"]["Value"]
    print(f"Текущий курс: {rate} ₽")

# Запускаем 4 раза с паузой 5 секунд
repeat_action(show_rate, times=4, interval=2)
