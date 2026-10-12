import csv

segments = {}
client_sale = {}
total_company_sales = 0.0

with open(r"C:\Users\user\Desktop\Try_2\Answer_try_2.csv", mode='r', encoding='utf-8', newline='') as answerfile:
    reader = csv.reader(answerfile, delimiter=';')
    head = next(reader, None)
    for row in reader:
        if len(row) < 25:
            continue
        try:
            cust_name = row[6].strip()
            cust_segment = row[8].strip()
            profit = float(row[21])
            sales = float(row[23])

            total_company_sales += sales

            if cust_segment not in segments:
                segments[cust_segment] = {
                    "sales" : 0.0,
                    "profit" : 0.0,
                    "orders_count" : 0
                }
            segments[cust_segment]["sales"] += sales
            segments[cust_segment]["profit"] += profit
            segments[cust_segment]["orders_count"] += 1

            if cust_name not in client_sale:
                client_sale[cust_name] = 0.0
            client_sale[cust_name] += sales
        except ValueError as e:
            print(f"Ошибка конвертации в строке Row ID {row[0]}: {e}")
            

print("=" * 95)
print(f"{'АНАЛИЗ КЛИЕНТСКИХ СЕГМЕНТОВ':^95}")
print("=" * 95)
print(f"{'Клиентский сегмент':<20} | {'Заказы':<8} | {'Продажи (Sales)':<16} | {'Прибыль (Profit)':<16} | {'Средний чек':<12} | {'Рентабельность':<10}")
print("-" * 95)

top_segment_name = ""
max_segment_sales = 0.0

for seg_name, metrics in segments.items():
    s_total = metrics["sales"]
    p_total = metrics["profit"]
    cnt = metrics["orders_count"]
    
    # Расчет среднего чека и рентабельности продаж (ROS)
    avg_check = s_total / cnt if cnt > 0 else 0.0
    margin = (p_total / s_total) * 100 if s_total > 0 else 0.0
    
    # Поиск лидера по объему выручки
    if s_total > max_segment_sales:
        max_segment_sales = s_total
        top_segment_name = seg_name
        
    print(f" {seg_name:<19} | {cnt:<8} | {s_total:>16,.2f} | {p_total:>16,.2f} | {avg_check:>12,.2f} | {margin:>9.2f}%")

print("-" * 95)
print(f" Финансовый лидер: сегмент {top_segment_name.upper()} с общим доходом {max_segment_sales:,.2f}")


print("\n" + "=" * 95)
print(f"{'АНАЛИЗ КОНЦЕНТРАЦИИ КЛИЕНТОВ (ТОП-5 ПО ВЫРУЧКЕ)':^95}")
print("=" * 95)

# Сортируем клиентов по убыванию объема их покупок (Sales)
sorted_clients = sorted(client_sale.items(), key=lambda x: x[1], reverse=True)

print(f"  {'№':<2} | {'ФИО Клиента':<35} | {'Сумма покупок':<16} | {'Доля в продажах':<15}")
print("-" * 95)

top_5_sales_sum = 0.0

for i, (c_name, c_sales) in enumerate(sorted_clients[:5], 1):
    # Расчет индивидуальной доли клиента в общем обороте компании
    client_share = (c_sales / total_company_sales) * 100 if total_company_sales > 0 else 0.0
    top_5_sales_sum += c_sales
    
    print(f"  {i:<2} | {c_name:<35} | {c_sales:>16,.2f} | {client_share:>14.2f}%")

# Расчет совокупного риска концентрации ТОП-5 клиентов
total_top_5_share = (top_5_sales_sum / total_company_sales) * 100 if total_company_sales > 0 else 0.0

print("-" * 95)
print(f"Совокупная выручка ТОП-5 клиентов: {top_5_sales_sum:,.2f}")
print(f"Доля ТОП-5 клиентов в общих продажах компании: {total_top_5_share:.2f}%")

if total_top_5_share > 20.0:
    print(" ВНИМАНИЕ: Высокая зависимость от крупных клиентов (риск концентрации рынка)!")
else:
    print(" ВЫВОД: Продажи распределены по базе равномерно, риски минимальны.")
print("=" * 95)
