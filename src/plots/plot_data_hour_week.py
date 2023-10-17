
import numpy as np
import matplotlib.pyplot as plt
from time import time

hours_of_day = list(range(24))

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
colors = plt.cm.tab20c(np.linspace(0, 1, 7))  # Разные цвета для дней недели

def plot_data_day_hour(filter_df, title, specific_day=None):
    grouped = filter_df.groupby(['hour', 'day_of_week']).size().reset_index(name='counts')
    pivot_df = grouped.set_index(['hour', 'day_of_week']).unstack('day_of_week')['counts']
    
    ax = pivot_df.plot(kind='bar', figsize=(15, 8), color=colors, width=0.8)
    if specific_day is not None and specific_day in range(7):
        day_data = pivot_df[specific_day]
        ax.plot(day_data, label=days_of_week[specific_day], alpha=0.8, linewidth=2.5, color=colors[specific_day])

    elif specific_day is None:
         # Усредненная кривая по всем дням
        mean_curve = pivot_df.mean(axis=1)
        ax.plot(mean_curve, color='red', linestyle='--', linewidth=2.5, label="Среднее по всем дням")
    else:
        # Построение огибающих кривых
        for day in range(7):
            day_data = pivot_df[day]
            ax.plot(day_data, label=days_of_week[day], alpha=0.8, linewidth=2.5, color=colors[day])

        # Усредненная кривая по всем дням
        mean_curve = pivot_df.mean(axis=1)
        ax.plot(mean_curve, color='red', linestyle='--', linewidth=2.5, label="Среднее по всем дням")

    # Легенда
    ax.legend(loc='center left', bbox_to_anchor=(1, 0.5), title="Дни недели")

    plt.title(title)
    plt.tight_layout()
    plt.xticks(ticks=range(24), labels=hours_of_day, rotation=45, ha='right')
    # Сохранение графика в виде изображения
    timestamp = int(time())
    plt.savefig(f"{title}_{timestamp}.png", bbox_inches="tight")

    plt.show()


