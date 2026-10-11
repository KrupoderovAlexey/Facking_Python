1:   
import csv
with open(r"C:\Users\user\Desktop\Shit_EXEL_2.csv", mode='r', encoding='utf-8') as f:
    reader = csv.reader(f, delimiter=';')
    fr = next(reader)
translit = """ ID строки;Приоритет заказа;Скидка;Цена за единицу;Стоимость доставки;ID клиента;Имя клиента;Способ доставки;Сегмент клиентов;Категория товара;Подкатегория товара;Тип упаковки;Название товара;Базовая маржинальность;Страна;Регион;Штат или провинция;Город;Почтовый индекс;Дата заказа;Дата отправки;Прибыль;Количество в заказе;Продажи;ID заказа"""
item_translit = translit.split(';')
tape = """ str;str;float;float;float;int;str;str;str;str;str;str;str;float;str;str;str;str;str;datetime;datetime;float;int;float;str"""
tape_new = tape.split(';')
for i in range(len(fr)):
    print(f"{i+1:<4} {fr[i]:<24} {item_translit[i]:<25} {tape_new[i]:<10}")
