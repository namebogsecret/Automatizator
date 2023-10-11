
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np
from time import time

months_names = {
    1: 'Январь',
    2: 'Февраль',
    3: 'Март',
    4: 'Апрель',
    5: 'Май',
    6: 'Июнь',
    7: 'Июль',
    8: 'Август',
    9: 'Сентябрь',
    10: 'Октябрь',
    11: 'Ноябрь',
    12: 'Декабрь'
}
days_of_week = {
    0: 'Воскресенье',
    1: 'Понедельник',
    2: 'Вторник',
    3: 'Среда',
    4: 'Четверг',
    5: 'Пятница',
    6: 'Суббота'
}
# pylint: disable=no-member
colors = cm.tab20(np.linspace(0, 1, 12))

def plot_data_week_month(filter_df, title):
    grouped = filter_df.groupby(['day_of_week', 'month']).size().reset_index(name='counts')
    pivot_df = grouped.set_index(['day_of_week', 'month']).unstack('month')['counts']

    ax = pivot_df.plot(kind='bar', figsize=(15, 8), color=colors, width=0.8)

    # Рассчитываем проценты для дней недели
    total_counts = filter_df.shape[0]
    daily_counts = filter_df.groupby('day_of_week').size()
    percentages = 100 * daily_counts / total_counts

    day_labels = [f"{days_of_week[i]} ({percentages[i]:.1f}%)" for i in range(7)]
    plt.xticks(ticks=range(7), labels=day_labels, rotation=45, ha='right')

    # Построение огибающих кривых
    for month in months_names.keys():  # Используем ключи из словаря месяцев
        if month in pivot_df.columns:  # Проверка наличия месяца в данных
            month_data = pivot_df[month]
            ax.plot(month_data, label=months_names[month], alpha=0.8, linewidth=2.5, color=colors[month-1])

    # Усредненная кривая по всем месяцам
    mean_curve = pivot_df.mean(axis=1)
    ax.plot(mean_curve, color='black', linestyle='--', linewidth=2.5, label="Среднее по всем месяцам")

    # Легенда
    ax.legend(loc='center left', bbox_to_anchor=(1, 0.5), title="Месяцы")

    # Улучшим видимость подписей осей
    max_value = pivot_df.values.max()
    if not np.isnan(max_value):
        ax.set_ylim(0, max_value + 10)  # устанавливаем пределы оси Y
    else:
        print("Warning: Maximum value in data is NaN.")
    #ax.set_ylim(0, pivot_df.values.max() + 10)  # устанавливаем пределы оси Y
    for tick in ax.get_xticklabels():  # увеличиваем шрифт подписей оси X
        tick.set_fontsize(10)
    for tick in ax.get_yticklabels():  # увеличиваем шрифт подписей оси Y
        tick.set_fontsize(10)

    plt.title(title)
    plt.tight_layout()
    timestamp = int(time())
    plt.savefig(f"{title}_{timestamp}.png", bbox_inches="tight")
    plt.show()