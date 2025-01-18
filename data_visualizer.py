import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

def create_plot(plot_type, data, x_column, y_column):
    plot_functions = {
        "Гистограмма": lambda: sns.histplot(data[x_column], kde=True),
        "Диаграмма рассеяния": lambda: plt.scatter(data[x_column], data[y_column]),
        "Ящик с усами": lambda: sns.boxplot(x=data[x_column]),
        "Линейный график": lambda: plt.plot(data[x_column], data[y_column]),
        "Столбчатая диаграмма": lambda: sns.barplot(x=data[x_column], y=data[y_column]),
        "Круговая диаграмма": lambda: plt.pie(data[x_column].value_counts(), labels=data[x_column].unique(), autopct='%1.1f%%'),
        "Ствол-лист диаграмма": lambda: plt.stem(data[x_column].index, data[x_column], basefmt=" "),
        "Контурный график": lambda: create_contour_plot(data, x_column, y_column),
        "Поля градиентов": lambda: plt.quiver(data[x_column], data[y_column], np.random.rand(len(data)), np.random.rand(len(data))),
        "Спектральная диаграмма": lambda: plt.specgram(data[x_column], Fs=1)
    }
    plot_functions[plot_type]()

def create_contour_plot(data, x_column, y_column):
    X, Y = np.meshgrid(data[x_column], data[y_column])
    Z = np.sin(X) * np.cos(Y)
    plt.contour(X, Y, Z)