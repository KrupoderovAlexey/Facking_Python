import openpyxl
from openpyxl.styles import Font
import random

# Создаем книгу
wb = openpyxl.Workbook()
ws = wb.active
ws.title = "Выгрузка_Продаж"

# Заголовки
headers = ["ID Заказа", "Дата", "Товар", "Количество", "Цена за штуку", "Скидка", "Статус"]
ws.append(headers)

# Грязные данные для генерации
dirty_dates = ["2026-03-01", "02/03/2026", "03.03.2026", " 04.03.2026 ", "2026.03.05"]
dirty_prices = ["15 000 руб.", " 4200р", "12500", "750 руб", "не указана", " 900 р. "]
dirty_discounts = ["10%", "0.05", "без скидки", None, "15 %", None]

# Генерируем 15 строк "кошмара аналитика"
random.seed(42) # Фиксируем хаос для воспроизводимости
for i in range(1, 16):
    order_id = f"REQ-{1000 + i}"
    
    # Делаем дубликат строки для проверки на дубли
    if i == 7:
        order_id = "REQ-1005" 
        
    date = random.choice(dirty_dates)
    item = f" Смартфон Модель {random.choice(['A', 'B', 'C'])}   " # Пробелы по краям
    qty = random.choice([1, 2, "3", 1, " 2 "]) # Перемешаны строки и числа
    price = random.choice(dirty_prices)
    discount = random.choice(dirty_discounts)
    status = random.choice(["Доставлено", "доставлено", " Отменено", "В ПУТИ "])
    
    ws.append([order_id, date, item, qty, price, discount, status])

# Сохраняем файл
wb.save("raw_sales_data.xlsx")
print("Файл 'raw_sales_data.xlsx' успешно создан! Пора его причесать.")
