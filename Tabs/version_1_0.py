import matplotlib.pyplot as plt
import numpy as np

# Данные
x = [1, 2, 3, 4, 5]
y = [2, 3, 5, 7, 11]
labels = ['1', '2', '3', '4', '5']  # цифры в виде строк



fig, ax = plt.subplots(figsize=(16, 6))

X = [0.2, 0.2, 0.2, 0.2, 0.2, 0.2]
Y = [1, 2, 3, 4, 5, 6]
labels_osn = ['1', '2', '3', '4', '5', '6']  # цифры в виде строк
for i in range(len(X)):
    ax.plot(X[i], Y[i], 
            marker=f'${labels_osn[i]}$',  # LaTeX формат для цифр
            markersize=8,            # размер маркера
            linestyle='None',         # убираем линию между точками
            color='black',             # цвет цифр
            markeredgecolor='black',  # цвет обводки
            #markeredgewidth=0.5,      # толщина обводки
            markerfacecolor='black', # цвет заливки маркера
            alpha=0.9)                # прозрачность


# === ДОБАВЛЯЕМ ГОРИЗОНТАЛЬНЫЕ ЛИНИИ ===
y_lines = [1, 2, 3, 4, 5, 6]  # значения Y для линий

for y_val in y_lines:
    ax.axhline(y=y_val, 
               color='black',           # цвет линии
               linestyle='--',        # стиль: '--' пунктир, '-' сплошная, ':' точки
               linewidth=1,           # толщина линии
               alpha=0.6)             # прозрачность

# Создаем кастомные маркеры с настройками
for i in range(len(x)):
    ax.plot(x[i], y[i], 
            marker=f'${labels[i]}$',  # LaTeX формат для цифр
            markersize=5.5,            # размер маркера
            linestyle='None',         # убираем линию между точками
            color='red',             # цвет цифр
            markeredgecolor='red',  # цвет обводки
            #markeredgewidth=0.5,      # толщина обводки
            markerfacecolor='lightblue', # цвет заливки маркера
            alpha=0.9)                # прозрачность


# Сетка для удобства чтения
ax.grid(True, alpha=0.3, linestyle='--')
ax.set_xticks(np.arange(0, 41, 1))  # от 0 до 40 включительно, шаг 1
# Настройка пределов осей (с небольшим отступом)
ax.set_xlim(0, 40)
ax.set_ylim(0, 7)


plt.tight_layout()
plt.show()
