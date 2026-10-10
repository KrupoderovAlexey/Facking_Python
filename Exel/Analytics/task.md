for i in range(len(data) - 1, 0, -1):
    example = data[i][0]
    for j in range(0, i):
        if (data[j][0] == example):
            del data[i]
            break

for i in range(1, len(data)):
    date = data[i][1]
    if (not date or not isinstance(data[i][1], str)):
        continue
    cl = data[i][1].strip()
    if '-' in cl :
        parts = cl.split('-')
    elif '.' in cl :
        parts = cl.split('.')
    elif '/' in cl :
        parts = cl.split('/')
    else:
        continue
    if (len(parts[0]) == 4):
        year = parts[0]
        month = parts[1]
        day = parts[2]
        new_date = f"{day}.{month}.{year}"
    else:
        new_date = cl.replace('/', '.')
    data[i][1] = new_date
