# Генератор таблицы exel с таблицей квадратов до вашего числа до вашей степени

wb = op.Workbook()
ww = wb.active
n = int(input("Введите до какого числа писать ...      ")) + 1
m = int(input("Введите до какой степени писать ...   ")) + 1
for i in range(1, m):
    ww.cell(row=1, column=i, value=i)
for i in range(1, n):
    ww.cell(row=i, column=1, value=i)

for i in range(2, n):
    for j in range(2, m):
        ww.cell(row=i, column=j, value= i**j)

#
for i in range(1, n):
    # Корректируем ширину столбца (берём букву столбца по его индексу i)
    col_letter = get_column_letter(i)
    ww.column_dimensions[col_letter].width = 5  # Узкие столбцы
    
    # Корректируем высоту строки
    ww.row_dimensions[i].height = 25  # Чуть повыше, для баланса
#

s = r"C:\Users\user\Desktop\Mytable_2.xlsx"
wb.save(s)
print(f"Файл сохранен в {s}")
