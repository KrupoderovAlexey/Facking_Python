# Генератор таблицы exel с таблицей умножения от 1 до вашего числа

exx = op.Workbook()
ex = exx.active
n = int(input("Введите до какого числа считать...    ")) + 1
for i in range(1, n): 
    ex.cell(row=i, column=1, value=i)
    ex.cell(row=1, column=i, value=i)
for i in range(2,n):
    for j in range(2, n):
        ex.cell(row=i, column=j, value=i * j)

#
for i in range(1, n):
    # Корректируем ширину столбца (берём букву столбца по его индексу i)
    col_letter = get_column_letter(i)
    ex.column_dimensions[col_letter].width = 5  # Узкие столбцы
    
    # Корректируем высоту строки
    ex.row_dimensions[i].height = 25  # Чуть повыше, для баланса
#

s = r"C:\Users\user\Desktop\MyTable.xlsx"
exx.save(s)
print(f"Файл сохренен в {s}")
