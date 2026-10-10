import openpyxl as op
import numpy as np

# Чтение
wb = op.load_workbook(r"C:\Users\user\Desktop\Shit_EXEL.xlsx", read_only = True, data_only = True)
sh = wb.active
data = []
for row in sh.iter_rows(values_only = True):
    if all(c is None for c in row):
        break
    data.append(list(row))

# Вывод
for i in range(len(data)):
    print(i, "   ", data[i])

# Даты в один формат
for i in range(1, len(data)):
    cl = data[i][1].strip()
    if '-' in cl: 
        parts = cl.split('-')
    elif '.' in cl: 
        parts = cl.split('.')
    elif ' ' in cl: 
        parts = cl.split(' ')
    elif '/' in cl: 
        parts = cl.split('/')
    if (len(parts[0]) == 4):
        day = parts[2]
        month = parts[1]
        year = parts[0]
        new = f"{day}.{month}.{year}"
    else:
        new = cl.replace('/', '.')
    data[i][1] = new

# Товар в один формат
for i in range(1, len(data)):
    data[i] = str(data[i]).strip().title()


# Количество в один формат int
for i in range(1, len(data)):
    val = data[i]
    if isinstance(val, str):
        val_clean = val.strip()
        try:
            data[i] = int(val_clean)
        except ValueError:
            data[i] = 0
    elif isinstance(val, (int, float)):
        data[i] = int(val)
    else:
        data[i] = 0
    
# Приведение цены к единому виду
for i in range(1, len(data)):
    val = data[i][4]
    if isinstance(val, str):
        num = val.replace(" ", "").strip()
        while num and not num.isdigit():
            num = num[:-1]
        if num.isdigit():
            data[i][4] = int(num)
        else:
            data[i][4] = 0
    elif isinstance(val, (int, float)):
        data[i][4] = int(val)

# Приведение к одному формату скидки
for i in range(1, len(data)):
    if type(data[i][5]) == str:
        p = data[i][5].strip()
        if 'без' in p or p == '':
            data[i][5] = 0.0
        elif '%' in p:
            p_clean = p.replace('%', '').strip()
            data[i][5] = round(float(p_clean) / 100, 2)
        else:
            try:
                data[i][5] = float(p)
            except ValueError:
                data[i][5] = 0.0
    elif isinstance(data[i][5], (int, float)):
        data[i][5] = float(data[i][5])
        
    else:
        data[i][5] = 0.0
        

# Приведение к одному формату статуса
for i in range(1, len(data)):
    data[i][6] = str(data[i][6]).strip().capitalize()

# Удаление повторов
new_data = [data[0]]
for row in data[1:]:
    if row not in new_data:
        new_data.append(row)
data = new_data

# Вывод
print ('\n\n')
for i in range(len(data)):
    print(i, "   ", data[i])

# Запись в новый файл
new_wb = op.Workbook()
ww = new_wb.active
for row in data:
    ww.append(row)
s = r"C:\Users\user\Desktop\MyAnswer.xlsx"
new_wb.save(s)
print(f"Файл сохранен в {s}")

# Закрытие
wb.close()
