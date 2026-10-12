import csv

# Путь к вашему очищенному и обогащенному файлу
inf = r"C:\Users\user\Desktop\Try_2\Answer_try_2.csv"

# Структуры для географического анализа
geo_matrix = {}

# Структуры для анализа динамики (трендов)
monthly_trend = {}
quarterly_trend = {
    "Q1": {"sales": 0.0, "profit": 0.0, "count": 0},
    "Q2": {"sales": 0.0, "profit": 0.0, "count": 0},
    "Q3": {"sales": 0.0, "profit": 0.0, "count": 0},
    "Q4": {"sales": 0.0, "profit": 0.0, "count": 0}
}

# Порядок месяцев для правильной сортировки при выводе
month_order = [
    "Январь", "Февраль", "Март", "Апрель", "Май", "Июнь",
    "Июль", "Август", "Сентябрь", "Октябрь", "Ноябрь", "Декабрь"
]

with open(inf, mode='r', encoding='utf-8', newline='') as answerfile:
    reader = csv.reader(answerfile, delimiter=';')
    
    # Пропускаем шапку таблицы
    head = next(reader, None)
    
    # Индексы полей: Region=15, State=16, City=17, Profit=21, Sales=23, Month_Name=27 (из Шага 2/3)
    # Наш обогащенный заголовок в Шаге 2 имел структуру: ... + ["Delivery time", "Month Number", "Month Name", "Quarter"]
    # Проверим точное соответствие индексов в цикле
    for row in reader:
        if len(row) < 25:
            continue
            
        try:
            region = row[15].strip()
            state = row[16].strip()
            city = row[17].strip()
            profit = float(row[21])
            sales = float(row[23])
            
            # Поля обогащения временных трендов (добавлены в конце строки)
            # Если вы дописывали поля "Delivery time" и "Quarter", то Quarter идет в самом конце
            quarter = row[-1].strip()      # Последний элемент (например, Q1, Q2)
            month_name = row[-2].strip()   # Предпоследний элемент (название месяца)
            
            # --- ЛОГИКА 1: Географическая агрегация ---
            if region not in geo_matrix:
                geo_matrix[region] = {}
            if state not in geo_matrix[region]:
                geo_matrix[region][state] = {}
            if city not in geo_matrix[region][state]:
                geo_matrix[region][state][city] = {"sales": 0.0, "profit": 0.0, "count": 0}
                
            geo_matrix[region][state][city]["sales"] += sales
            geo_matrix[region][state][city]["profit"] += profit
            geo_matrix[region][state][city]["count"] += 1
            
            # --- ЛОГИКА 2: Временные тренды (Месяцы) ---
            if month_name not in monthly_trend:
                monthly_trend[month_name] = {"sales": 0.0, "profit": 0.0, "count": 0}
            monthly_trend[month_name]["sales"] += sales
            monthly_trend[month_name]["profit"] += profit
            monthly_trend[month_name]["count"] += 1
            
            # --- ЛОГИКА 3: Временные тренды (Кварталы) ---
            if quarter in quarterly_trend:
                quarterly_trend[quarter]["sales"] += sales
                quarterly_trend[quarter]["profit"] += profit
                quarterly_trend[quarter]["count"] += 1
                
        except (ValueError, IndexError) as e:
            print(f"Ошибка в строке Row ID {row[0]}: {e}")
            continue

# Сбор плоского списка городов для поиска экстремумов (самых прибыльных/убыточных)
flat_cities = []
for reg, states in geo_matrix.items():
    for st, cities in states.items():
        for city_name, metrics in cities.items():
            flat_cities.append({
                "name": f"{city_name} ({st}, {reg})",
                "sales": metrics["sales"],
                "profit": metrics["profit"],
                "count": metrics["count"]
            })

# =====================================================================
# ВЫВОД РЕЗУЛЬТАТОВ В ТЕРМИНАЛ
# =====================================================================

print("=" * 115)
print(f"{'ГЕОГРАФИЧЕСКИЙ СРЕЗ ПРОДАЖ И ПРИБЫЛИ':^115}")
print("=" * 115)

# ТОП-5 Самых прибыльных локаций
sorted_profitable = sorted(flat_cities, key=lambda x: x["profit"], reverse=True)
print(f" ПОДРАЗДЕЛЕНИЕ: ТОП-5 САМЫХ ПРИБЫЛЬНЫХ ЛОКАЦИЙ (ГОРОДОВ)")
print("-" * 115)
print(f"  {'№':<2} | {'Локация (Город, Штат, Регион)':<55} | {'Заказы':<6} | {'Продажи (Sales)':<16} | {'Прибыль (Profit)':<16}")
print("-" * 115)
for i, item in enumerate(sorted_profitable[:5], 1):
    print(f"  {i:<2} | {item['name']:<55} | {item['count']:<6} | {item['sales']:>16,.2f} | {item['profit']:>16,.2f}")

# ТОП-5 Самых убыточных локаций («Черные дыры» географии)
sorted_unprofitable = sorted(flat_cities, key=lambda x: x["profit"])
print("\n" + "-" * 115)
print(f" ПОДРАЗДЕЛЕНИЕ: ТОП-5 НАИБОЛЕЕ УБЫТОЧНЫХ ЛОКАЦИЙ (ГОРОДОВ)")
print("-" * 115)
print(f"  {'№':<2} | {'Локация (Город, Штат, Регион)':<55} | {'Заказы':<6} | {'Продажи (Sales)':<16} | {'Прибыль (Profit)':<16}")
print("-" * 115)
for i, item in enumerate(sorted_unprofitable[:5], 1):
    print(f"  {i:<2} | {item['name']:<55} | {item['count']:<6} | {item['sales']:>16,.2f} | {item['profit']:>16,.2f}")


print("\n" + "=" * 115)
print(f"{'ДИНАМИКА ПРОДАЖ И СЕЗОННОСТЬ (ВРЕМЕННЫЕ ТРЕНДЫ)':^115}")
print("=" * 115)

# Вывод тренда по Кварталам
print(f" ТРЕНД ПО КВАРТАЛАМ:")
print("-" * 115)
print(f"  {'Квартал':<15} | {'Количество заказов':<18} | {'Сумма продаж (Sales)':<22} | {'Чистая прибыль (Profit)':<22} | {'Рентабельность':<12}")
print("-" * 115)
for q_name in sorted(quarterly_trend.keys()):
    q_metrics = quarterly_trend[q_name]
    q_sales = q_metrics["sales"]
    q_profit = q_metrics["profit"]
    q_margin = (q_profit / q_sales) * 100 if q_sales > 0 else 0.0
    print(f"  {q_name:<15} | {q_metrics['count']:<18} | {q_sales:>22,.2f} | {q_profit:>22,.2f} | {q_margin:>11.2f}%")

# Вывод тренда по Месяцам (с принудительной сортировкой по календарному календарю)
print("\n" + "-" * 115)
print(f" ТРЕНД ПО МЕСЯЦАМ (КАЛЕНДАРНЫЙ ГОД):")
print("-" * 115)
print(f"  {'Месяц':<15} | {'Количество заказов':<18} | {'Сумма продаж (Sales)':<22} | {'Чистая прибыль (Profit)':<22} | {'Рентабельность':<12}")
print("-" * 115)

for m_name in month_order:
    if m_name in monthly_trend:
        m_metrics = monthly_trend[m_name]
        m_sales = m_metrics["sales"]
        m_profit = m_metrics["profit"]
        m_margin = (m_profit / m_sales) * 100 if m_sales > 0 else 0.0
        print(f"  {m_name:<15} | {m_metrics['count']:<18} | {m_sales:>22,.2f} | {m_profit:>22,.2f} | {m_margin:>11.2f}%")

print("=" * 115)
