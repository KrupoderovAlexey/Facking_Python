import csv

# Путь к вашему очищенному и обогащенному файлу
inf = r"C:\Users\user\Desktop\Try_2\Answer_try_2.csv"

# Структуры данных для логистического анализа
ship_mode_matrix = {}
priority_matrix = {}
container_matrix = {}

with open(inf, mode='r', encoding='utf-8', newline='') as answerfile:
    reader = csv.reader(answerfile, delimiter=';')
    
    # Пропускаем шапку таблицы
    head = next(reader, None)
    
    for row in reader:
        if len(row) < 25:
            continue
            
        try:
            # Извлекаем данные по точным индексам
            order_priority = row[1].strip()
            shipping_cost = float(row[4])
            ship_mode = row[7].strip()
            product_container = row[11].strip()
            
            # Поля обогащения временных трендов (добавлены в конце строки)
            # Из Шага 6: Quarter идет в самом конце (row[-1]), Delivery time идет предпоследним (row[-2])
            delivery_time = int(row[-2])
            
            # --- ЛОГИКА 1: Эффективность доставки (Ship Mode) ---
            if ship_mode not in ship_mode_matrix:
                ship_mode_matrix[ship_mode] = {"cost_sum": 0.0, "time_sum": 0, "count": 0}
            ship_mode_matrix[ship_mode]["cost_sum"] += shipping_cost
            ship_mode_matrix[ship_mode]["time_sum"] += delivery_time
            ship_mode_matrix[ship_mode]["count"] += 1
            
            # --- ЛОГИКА 2: Влияние приоритета на логистику (Order Priority) ---
            if order_priority not in priority_matrix:
                priority_matrix[order_priority] = {"time_sum": 0, "count": 0}
            priority_matrix[order_priority]["time_sum"] += delivery_time
            priority_matrix[order_priority]["count"] += 1
            
            # --- ЛОГИКА 3: Анализ типов контейнеров (Product Container) ---
            if product_container not in container_matrix:
                container_matrix[product_container] = {"cost_sum": 0.0, "count": 0}
            container_matrix[product_container]["cost_sum"] += shipping_cost
            container_matrix[product_container]["count"] += 1
            
        except (ValueError, IndexError) as e:
            print(f"Ошибка в строке Row ID {row[0]}: {e}")
            continue

# =====================================================================
# ВЫВОД РЕЗУЛЬТАТОВ В ТЕРМИНАЛ
# =====================================================================

print("=" * 95)
print(f"{'АНАЛИЗ ЭФФЕКТИВНОСТИ ТИПОВ ДОСТАВКИ (SHIP MODE)':^95}")
print("=" * 95)
print(f"{'Тип доставки':<25} | {'Заказы':<8} | {'Ср. Стоимость':<18} | {'Ср. Скорость (дни)':<18}")
print("-" * 95)

for mode, metrics in ship_mode_matrix.items():
    cnt = metrics["count"]
    avg_cost = metrics["cost_sum"] / cnt if cnt > 0 else 0.0
    avg_time = metrics["time_sum"] / cnt if cnt > 0 else 0.0
    print(f" {mode:<24} | {cnt:<8} | {avg_cost:>16,.2f}$ | {avg_time:>16.2f} дн.")


print("\n" + "=" * 95)
print(f"{'АНАЛИЗ ВЛИЯНИЯ ПРИОРИТЕТА НА СКОРОСТЬ ОТПРАВКИ (ORDER PRIORITY)':^95}")
print("=" * 95)
print(f"{'Приоритет заказа':<25} | {'Заказы':<8} | {'Среднее время отправки (в днях)':<30}")
print("-" * 95)

# Принудительный порядок вывода приоритетов от Critical до Low для наглядности
priority_order = ["Critical", "High", "Medium", "Low", "Not Specified"]
for prio in priority_order:
    if prio in priority_matrix:
        metrics = priority_matrix[prio]
        cnt = metrics["count"]
        avg_time = metrics["time_sum"] / cnt if cnt > 0 else 0.0
        print(f" {prio:<24} | {cnt:<8} | {avg_time:>28.2f} дн.")


print("\n" + "=" * 95)
print(f"{'АНАЛИЗ ТИПОВ КОНТЕЙНЕРОВ И ТРАНСПОРТИРОВКИ (PRODUCT CONTAINER)':^95}")
print("=" * 95)
print(f"{'Тип контейнера / упаковки':<35} | {'Заказы':<8} | {'Средняя стоимость доставки':<25}")
print("-" * 95)

# Сортируем контейнеры по убыванию средней стоимости доставки
sorted_containers = sorted(
    container_matrix.items(), 
    key=lambda x: (x[1]["cost_sum"] / x[1]["count"]) if x[1]["count"] > 0 else 0.0, 
    reverse=True
)

for container, metrics in sorted_containers:
    cnt = metrics["count"]
    avg_cost = metrics["cost_sum"] / cnt if cnt > 0 else 0.0
    print(f" {container:<34} | {cnt:<8} | {avg_cost:>23,.2f}$")

print("=" * 95)
