import csv

product_cat = {}
loss_product = {}

with open(r"C:\Users\user\Desktop\Try_2\Answer_try_2.csv", mode='r', encoding='utf-8', newline='') as answerfile:
    reader = csv.reader(answerfile, delimiter=';')
    head = next(reader, None)
    for row in reader:
        if len(row) < 25:
            continue
        try:
            disc = float(row[2])
            cat = row[9].strip()
            sub_cat = row[10].strip()
            name_prod = row[12].strip()

            base_marg = float(row[13]) if row[13] else 0.0

            profit = float(row[21])
            sales = float(row[23])

            if cat not in product_cat:
                product_cat[cat] = {}
            if sub_cat not in product_cat[cat]:
                product_cat[cat][sub_cat] = {
                    "sales" : 0.0,
                    "profit" : 0.0,
                    "marg_summ" : 0.0,
                    "count" : 0
                }
            product_cat[cat][sub_cat]["sales"] += sales
            product_cat[cat][sub_cat]["profit"] += profit
            product_cat[cat][sub_cat]["marg_summ"] += base_marg
            product_cat[cat][sub_cat]["count"] += 1

            if profit < 0:
                if name_prod not in loss_product:
                    loss_product[name_prod] = 0.0
                loss_product[name_prod] += abs(profit)

        except ValueError as e:
            print(f"Ошибка в строке Row ID {row[0]}: {e}")
            continue

print("=" * 115)
print(f"{"Подкатегория":<34} {"Заказы":<15} {"Продажи":<16} {"Прибыль":<15} {"Реал.маржа":<11} {"План.маржа":<11} {"Отклонение":<11}")
print("=" * 115)

for cat_name, sub_dict in product_cat.items():
    print(f"\n ОСНОВНАЯ КАТЕГОРИЯ: {cat_name.upper()}")
    print("-" * 115)
    
    for sub_cat_name, metrics in sub_dict.items():
        s_total = metrics["sales"]
        p_total = metrics["profit"]
        cnt = metrics["count"]
        # Реальная рентабельность подкатегории (ROS)
        real_margin = (p_total / s_total) * 100 if s_total > 0 else 0.0
        # Средняя плановая маржинальность из справочника
        plan_margin = (metrics["marg_summ"] / cnt) * 100 if cnt > 0 else 0.0
        # Разница (на сколько реальность отстает от плана или обгоняет его)
        diff = real_margin - plan_margin
        
        print(f"  {sub_cat_name:<34} {cnt:<8} {s_total:>16,.2f} {p_total:>16,.2f} {real_margin:>11.2f}% {plan_margin:>11.2f}% {diff:>11.2f}%")

print("\n" + "=" * 115)
print(f"{'ТОП-10 НАИБОЛЕЕ УБЫТОЧНЫХ ТОВАРОВ («ЧЕРНЫЕ ДЫРЫ»)':^115}")
print("=" * 115)

# Сортируем товары по убыванию накопленного убытка
# loss_products.items() возвращает кортежи (Имя_товара, Сумма_убытка)
# key=lambda x: x[1] заставляет сортировать именно по Сумме_убытка
sorted_losses = sorted(loss_product.items(), key=lambda x: x[1], reverse=True)

print(f"  {'Название товара':<75} | {'Суммарный чистый убыток':<15}")
print("-" * 115)

# Выводим первые 10 позиций из отсортированного списка
for i, (prod_name, total_loss) in enumerate(sorted_losses[:10], 1):
    # Если название товара слишком длинное — обрезаем его для красоты таблицы
    short_name = prod_name[:72] + "..." if len(prod_name) > 75 else prod_name
    print(f" {i:>2}. {short_name:<72} | -{total_loss:>19,.2f}")

print("=" * 115)
