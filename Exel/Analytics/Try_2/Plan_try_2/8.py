import csv

# Путь к вашему очищенному и обогащенному файлу
inf = r"C:\Users\user\Desktop\Try_2\Answer_try_2.csv"

# 1. Структура для анализа влияния скидок (Интервалы скидок)
# Распределим скидки по классическим диапазонам
discount_intervals = {
    "Без скидки (0%)": {"sales": 0.0, "profit": 0.0, "quantity": 0, "count": 0},
    "Мелкая (1% - 5%)": {"sales": 0.0, "profit": 0.0, "quantity": 0, "count": 0},
    "Средняя (6% - 10%)": {"sales": 0.0, "profit": 0.0, "quantity": 0, "count": 0},
    "Крупная (10%+)": {"sales": 0.0, "profit": 0.0, "quantity": 0, "count": 0}
}

# 2. Структура для анализа зависимости стоимости и объема (Интервалы цен)
price_intervals = {
    "Бюджетные (до 10$)": {"quantity_sum": 0, "count": 0},
    "Средний сегмент (10$ - 50$)": {"quantity_sum": 0, "count": 0},
    "Бизнес сегмент (50$ - 100$)": {"quantity_sum": 0, "count": 0},
    "Премиум (100$+)": {"quantity_sum": 0, "count": 0}
}

with open(inf, mode='r', encoding='utf-8', newline='') as answerfile:
    reader = csv.reader(answerfile, delimiter=';')
    head = next(reader, None)
    
    for row in reader:
        if len(row) < 25:
            continue
            
        try:
            # Извлекаем нужные поля по точным индексам
            discount = float(row[2])         # Discount
            unit_price = float(row[3])       # Unit Price
            profit = float(row[21])          # Profit
            quantity = int(row[22])          # Quantity ordered new
            sales = float(row[23])           # Sales
            
            # --- ЛОГИКА 1: Влияние скидок ---
            if discount == 0.0:
                disc_group = "Без скидки (0%)"
            elif 0.0 < discount <= 0.05:
                disc_group = "Мелкая (1% - 5%)"
            elif 0.05 < discount <= 0.10:
                disc_group = "Средняя (6% - 10%)"
            else:
                disc_group = "Крупная (10%+)"
                
            discount_intervals[disc_group]["sales"] += sales
            discount_intervals[disc_group]["profit"] += profit
            discount_intervals[disc_group]["quantity"] += quantity
            discount_intervals[disc_group]["count"] += 1
            
            # --- ЛОГИКА 2: Взаимосвязь стоимости и объема ---
            if unit_price <= 10.0:
                price_group = "Бюджетные (до 10$)"
            elif 10.0 < unit_price <= 50.0:
                price_group = "Средний сегмент (10$ - 50$)"
            elif 50.0 < unit_price <= 100.0:
                price_group = "Бизнес сегмент (50$ - 100$)"
            else:
                price_group = "Премиум (100$+)"
                
            price_intervals[price_group]["quantity_sum"] += quantity
            price_intervals[price_group]["count"] += 1
            
        except ValueError as e:
            print(f"Ошибка в строке Row ID {row[0]}: {e}")
            continue

# =====================================================================
# ВЫВОД РЕЗУЛЬТАТОВ В ТЕРМИНАЛ
# =====================================================================

print("=" * 105)
print(f"{'АНАЛИЗ ВЛИЯНИЯ СКИДОК НА ОБЪЕМЫ И ФИНАНСОВЫЙ РЕЗУЛЬТАТ':^105}")
print("=" * 105)
print(f"{'Группа скидок':<20} | {'Сделки':<6} | {'Продажи (Sales)':<16} | {'Прибыль (Profit)':<16} | {'Ср.Кол-во в заказе':<18} | {'Рентабельность':<10}")
print("-" * 105)

for disc_group, metrics in discount_intervals.items():
    cnt = metrics["count"]
    s_total = metrics["sales"]
    p_total = metrics["profit"]
    q_total = metrics["quantity"]
    
    avg_quantity = q_total / cnt if cnt > 0 else 0.0
    margin = (p_total / s_total) * 100 if s_total > 0 else 0.0
    
    print(f" {disc_group:<19} | {cnt:<6} | {s_total:>16,.2f} | {p_total:>16,.2f} | {avg_quantity:>18.2f} шт | {margin:>9.2f}%")


print("\n" + "=" * 105)
print(f"{'АНАЛИЗ ВЗАИМОСВЯЗИ ЦЕНЫ ЗА ЕДИНИЦУ И ЗАКАЗЫВАЕМОГО КОЛИЧЕСТВА':^105}")
print("=" * 105)
print(f"{'Ценовой сегмент товара':<30} | {'Количество сделок':<18} | {'Среднее кол-во штук в одном заказе':<35}")
print("-" * 105)

for price_group, metrics in price_intervals.items():
    cnt = metrics["count"]
    q_sum = metrics["quantity_sum"]
    avg_items = q_sum / cnt if cnt > 0 else 0.0
    
    print(f" {price_group:<29} | {cnt:<18} | {avg_items:>35.2f} шт")

print("=" * 105)
