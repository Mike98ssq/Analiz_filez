import pandas as pd
from tkinter import messagebox, simpledialog

def handle_invalid_values(data):
    invalid_values = data[data.isnull().any(axis=1)]
    if not invalid_values.empty:
        prompt_invalid_value_action(data, invalid_values)

def prompt_invalid_value_action(data, invalid_values):
    messagebox.showwarning("Некорректные значения", f"Некорректные значения найдены в следующих строках:\n{invalid_values}")
    action = simpledialog.askstring("Некорректные значения", "Выберите действие:\n1. Удалить строки 2. Заменить на значение Введите 1 или 2:")
    if action == '1':
        data.dropna(inplace=True)
    elif action == '2':
        replacement_value = simpledialog.askstring("Заменить на значение", "Введите значение для замены:")
        data.fillna(value=replacement_value, inplace=True)