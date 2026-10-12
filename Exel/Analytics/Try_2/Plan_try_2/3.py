import csv

sales_total = 0 # 23
total_quantity = 0 # 21
profit_amount = 0 # 22
total_discount = 0 # 2
row_count = 0

with open(r"C:\Users\user\Desktop\Try_2\Answer_try_2.csv", mode='r', encoding='utf-8', newline='') as answerfile:
    reader = csv.reader(answerfile, delimiter=';')
    head = next(reader, None)
    for row in reader:
        if len(row) < 25:
            continue
        try:
            sales_total += float(row[23])
            total_quantity += int(row[22])
            profit_amount += float(row[21])
            total_discount += float(row[2])
            row_count += 1
        except ValueError as e:
            print(f"Пропущена строка с ошибкой конвертации в Row ID {row[0]}: {e}")
if row_count > 0 and sales_total > 0:
    average_discount = total_discount / row_count
    sales_margin_percent = (profit_amount / sales_total) * 100
else:
    print("Error")

print(f"Всего заказов :   {row_count}")
print(f"Общий обьем продаж :   {sales_total}")
print(f"Общая чистая прибыль :   {profit_amount}")
print(f"Количество товаров :   {total_quantity}")
print(f"Средний размер скидки :   {average_discount}")
print(f"Маржа :   {sales_margin_percent}")
