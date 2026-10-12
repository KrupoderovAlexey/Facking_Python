import csv
from datetime import datetime
import dateutil.parser as d_parser

check_dupl = set()
err_count = 0
dupl_count = 0
good_count = 0

# Функции валидации (исправленные, с защитой от скрытых пробелов)
def floating(val):
    clear_val = str(val).strip().replace('\xa0', '').replace(',', '.')
    if not clear_val:
        raise ValueError("ErrorFloat")
    try:
        return float(clear_val)
    except ValueError:
        raise ValueError("ErrorFloat")

def inting(val):
    clear_val = str(val).strip().replace('\xa0', '').replace(',', '.')
    if not clear_val:
        raise ValueError("ErrorInt")
    try:
        return int(float(clear_val))
    except ValueError:
        raise ValueError("ErrorInt")

def dating(val):
    clear_val = str(val).strip().replace('\xa0', '')
    if not clear_val:
        raise ValueError("ErrorDate")
    try:
        parsed_date_obj = d_parser.parse(clear_val, dayfirst=True)
        return parsed_date_obj.strftime('%d.%m.%Y')
    except (d_parser.ParserError, TypeError, ValueError):
        raise ValueError("ErrorDate")

def check_row_length(row):
    return len(row) == 25

def cell_edit(row):
    f_1 = str(row[1]).strip().capitalize()
    f_2 = floating(row[2])
    f_3 = floating(row[3])
    f_4 = floating(row[4])
    f_5 = str(row[5]).strip()
    f_6 = str(row[6]).strip()
    f_7 = str(row[7]).strip()
    f_8 = str(row[8]).strip()
    f_9 = str(row[9]).strip()
    f_10 = str(row[10]).strip()
    f_11 = str(row[11]).strip()
    f_12 = str(row[12]).strip()
    f_13 = floating(row[13])  # Пустые значения SAFCO вызовут тут ошибку и уйдут в лог
    f_14 = str(row[14]).strip().title()
    f_15 = str(row[15]).strip().title()
    f_16 = str(row[16]).strip().title()
    f_17 = str(row[17]).strip().title()
    f_18 = str(row[18]).strip()
    f_19 = dating(row[19])    # Дата заказа
    f_20 = dating(row[20])    # Дата отправки
    f_21 = floating(row[21])
    f_22 = inting(row[22])
    f_23 = floating(row[23])
    f_24 = str(row[24]).strip()
    
    return [
        row[0], f_1, f_2, f_3, f_4, f_5, f_6, f_7, f_8, f_9, 
        f_10, f_11, f_12, f_13, f_14, f_15, f_16, f_17, f_18, 
        f_19, f_20, f_21, f_22, f_23, f_24
    ]

# Пути к файлам (читаем ИСХОДНЫЙ "Shit_EXEL_2.csv")
inf = r"C:\Users\user\Desktop\Try_2\Shit_EXEL_2.csv"
outf = r"C:\Users\user\Desktop\Try_2\Answer_try_2.csv"
log = r"C:\Users\user\Desktop\Try_2\Log_try_2.csv"

with open(inf, mode='r', encoding='utf-8', newline='') as infile, \
     open(outf, mode='w', encoding='utf-8', newline='') as outfile, \
     open(log, mode='w', encoding='utf-8', newline='') as logfile:
        
        reader = csv.reader(infile, delimiter=';')
        writer = csv.writer(outfile, delimiter=';')
        log_writer = csv.writer(logfile, delimiter=';')

        head = next(reader, None)
        if head:
            log_writer.writerow(head + ["Log Reason"])
            # Сразу добавляем новые столбцы в заголовок чистого файла
            writer.writerow(head + ["Delivery time", "Quarter"]) 

        for row in reader:
            if len(row) <= 1:
                err_count += 1
                log_writer.writerow(row + ["Error (Empty or Short)"])
                continue

            if not check_row_length(row):
                err_count += 1
                log_writer.writerow(row + ["Error (Wrong Columns Count)"])
                continue

            ind = row[0]

            if ind in check_dupl:
                dupl_count += 1
                log_writer.writerow(row + ["Duplicate"])
                continue
    
            try:
                # 1. Сначала полностью очищаем и валидируем строку
                clean_row = cell_edit(row) 
                
                # 2. Если очистка успешна — ПРЯМО ТУТ обогащаем данными о доставке и квартале
                or_date = datetime.strptime(clean_row[19], '%d.%m.%Y')
                sh_date = datetime.strptime(clean_row[20], '%d.%m.%Y')
                
                deliv_time = (sh_date - or_date).days
                if deliv_time < 0:
                    deliv_time = 0
                    
                quarter_num = (or_date.month - 1) // 3 + 1
                quarter_str = f"Q{quarter_num}"
                
                # Дописываем новые столбцы к уже очищенной строке
                final_row = clean_row + [deliv_time, quarter_str]
                
                # Сохраняем результат
                check_dupl.add(ind) 
                writer.writerow(final_row)
                good_count += 1
                
            except ValueError as e:
                err_count += 1
                log_writer.writerow(row + [str(e)])

print(f"Переписано строчек:   {good_count}")
print(f"Дупликатов:   {dupl_count}")
print(f"Ошибок:   {err_count}")
