import csv
import datetime as dt
import dateutil.parser as d_parser

# Кастомное исключение, чтобы цикл понимал, что в данных ошибка
class DataValidationError(Exception):
    pass

def floatalize(val):
    c_val = str(val).strip().replace(',', '.')
    if not c_val:
        return None  # Если ячейка изначально пустая - это нормально, возвращаем None
    try:
        return float(c_val)
    except ValueError:
        # Если там был текст вместо числа - выбрасываем ошибку для лога
        raise DataValidationError(f"Ошибка конвертации во float: '{val}'")

def intialize(val):
    c_val = str(val).strip()
    if not c_val:
        return None  # Пустая ячейка - это нормально
    try:
        return int(c_val)
    except ValueError:
        # Если индекс или ID сломан - выбрасываем ошибку
        raise DataValidationError(f"Ошибка конвертации в int: '{val}'")

def parse_date(val):
    c_val = str(val).strip()
    if not c_val:
        return None  # Пустая ячейка - это нормально
    try:
        parsed_date_obj = d_parser.parse(c_val, dayfirst=True)
        return parsed_date_obj.strftime('%d.%m.%Y')
    except (d_parser.ParserError, TypeError, ValueError):
        # Если дата не распознана парсером - выбрасываем ошибку
        raise DataValidationError(f"Неверный формат даты: '{val}'")

def stringify_id(val):
    return str(val) if val is not None else None

seen_rows = set()
duplicate_count = 0
corrupted_count = 0

inf = r"C:\Users\user\Desktop\Shit_EXEL_2.csv"
outf = r"C:\Users\user\Desktop\Processed_File.csv"
logf = r"C:\Users\user\Desktop\log_file.csv"

with open(inf, mode='r', encoding='utf-8', newline='') as inFile, \
     open(outf, mode='w', encoding='utf-8', newline='') as outFile, \
     open(logf, mode='w', encoding='utf-8', newline='') as logFile:
     
    reader = csv.reader(inFile, delimiter=';')
    writer = csv.writer(outFile, delimiter=';')
    log_writer = csv.writer(logFile, delimiter=';')
    
    header = next(reader, None)
    if header:
        # Добавляем в шапку лог-файла колонку "Причина попадания в лог"
        log_header = header + ["Log Reason"]
        writer.writerow(header)
        log_writer.writerow(log_header)
        
    for row in reader:
        if len(row) > 1:
            try:
                # 1. Проверяем дубликаты (Row ID на позиции 0)
                # Делаем это ДО полной обработки, чтобы не тратить ресурсы на дубли
                raw_row_id = str(row[0]).strip()
                if raw_row_id in seen_rows:
                    duplicate_count += 1
                    log_writer.writerow(row + ["Duplicate Row ID"])
                    continue
                
                # 2. Пытаемся обработать и очистить данные таблицы
                processed_row = list(row) # Создаем копию для безопасных изменений
                
                processed_row[0] = stringify_id(intialize(row[0]))
                processed_row[1] = row[1].strip()
                processed_row[2] = floatalize(row[2])
                processed_row[3] = floatalize(row[3])
                processed_row[4] = floatalize(row[4])
                processed_row[5] = stringify_id(intialize(row[5]))
                processed_row[6] = row[6].strip()
                processed_row[7] = row[7].strip()
                processed_row[8] = row[8].strip()
                processed_row[9] = row[9].strip()
                processed_row[10] = row[10].strip()
                processed_row[11] = row[11].strip()
                processed_row[12] = row[12].strip()
                processed_row[13] = floatalize(row[13])
                
                processed_row[14] = row[14].title()
                processed_row[15] = row[15].title()
                processed_row[16] = row[16].title()
                processed_row[17] = row[17].title()
                processed_row[18] = row[18].strip()
                
                processed_row[19] = parse_date(row[19])
                processed_row[20] = parse_date(row[20])
                processed_row[21] = floatalize(row[21])
                processed_row[22] = intialize(row[22])
                processed_row[23] = floatalize(row[23])
                processed_row[24] = stringify_id(intialize(row[24]))
                
                # Если все функции выполнились без ошибок:
                seen_rows.add(processed_row[0]) # Запоминаем очищенный ID
                writer.writerow(processed_row)   # Пишем в чистый файл
                
            except DataValidationError as e:
                # 3. Если любая колонка выкинула ошибку - перехватываем её
                corrupted_count += 1
                # Записываем ОРИГИНАЛЬНУЮ "грязную" строку в лог и в конец дописываем текст ошибки
                log_writer.writerow(row + [str(e)])
                continue

print("Обработка завершена успешно!")
print(f"-> Успешно очищено и сохранено строк: {len(seen_rows)}")
print(f"-> Удалено полных дубликатов: {duplicate_count}")
print(f"-> Отправлено в лог из-за ошибок в данных (битые ячейки): {corrupted_count}")
