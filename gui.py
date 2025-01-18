import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
import customtkinter as ctk
from data_loader import load_data
from data_handler import handle_invalid_values
from data_visualizer import create_plot
import matplotlib.pyplot as plt

class AnalyticsApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Аналитическое приложение")

        self.frame = ctk.CTkFrame(self.root)
        self.frame.pack(pady=20, padx=20)

        self.load_button = ctk.CTkButton(self.frame, text="Загрузить файл", command=self.load_file)
        self.load_button.pack(pady=10)

        self.stats_button = ctk.CTkButton(self.frame, text="Показать статистику", command=self.show_statistics)
        self.stats_button.pack(pady=10)

        self.plot_button = ctk.CTkButton(self.frame, text="Построить график", command=self.plot_data)
        self.plot_button.pack(pady=10)

        self.filter_button = ctk.CTkButton(self.frame, text="Фильтровать данные", command=self.filter_data)
        self.filter_button.pack(pady=10)

        self.text_area = ctk.CTkTextbox(self.frame, width=900, height=400)
        self.text_area.pack(pady=10, fill=tk.BOTH, expand=True)

        self.data = None
        self.plot_types = [
            "Гистограмма", "Диаграмма рассеяния", "Ящик с усами", "Линейный график", 
            "Столбчатая диаграмма", "Круговая диаграмма", "Ствол-лист диаграмма",
            "Контурный график", "Поля градиентов", "Спектральная диаграмма"
        ]
        self.selected_plot_type = ctk.StringVar(value=self.plot_types[0])
        self.plot_type_menu = ctk.CTkComboBox(self.frame, variable=self.selected_plot_type, values=self.plot_types)
        self.plot_type_menu.pack(pady=10)

    def load_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv"), ("Excel files", "*.xlsx"), 
                                                            ("JSON files", "*.json"), ("SQLite DB files", "*.sqlite3")])
        if file_path:
            self.load_data(file_path)

    def load_data(self, file_path):
        try:
            self.data = load_data(file_path)
            handle_invalid_values(self.data)
            messagebox.showinfo("Успех", "Файл успешно загружен!")
        except Exception as e:
            self.show_error(f"Не удалось загрузить файл: {e}")

    def show_statistics(self):
        if self.check_data_loaded():
            stats = self.data.describe(include='all').round().transpose().to_string()
            self.text_area.delete("1.0", tk.END)
            self.text_area.insert(tk.END, stats)

    def plot_data(self):
        if not self.check_data_loaded():
            return

        x_column = simpledialog.askstring("Введите ось X", "Введите имя столбца для оси X:")
        y_column = simpledialog.askstring("Введите ось Y", "Введите имя столбца для оси Y:") if self.selected_plot_type.get() in ["Диаграмма рассеяния", "Линейный график", "Столбчатая диаграмма", "Контурный график","Поля градиентов"] else None

        if self.validate_columns(x_column, y_column):
            plt.figure(figsize=(10, 6))
            create_plot(self.selected_plot_type.get(), self.data, x_column, y_column)
            plt.tight_layout()
            plt.show()

    def validate_columns(self, x_column, y_column):
        if x_column not in self.data.columns:
            messagebox.showwarning("Ошибка", "Столбец X не найден.")
            return False
        if y_column and y_column not in self.data.columns:
            messagebox.showwarning("Ошибка", "Столбец Y не найден.")
            return False
        return True

    def filter_data(self):
        if not self.check_data_loaded():
            return

        column = simpledialog.askstring("Введите имя столбца", "Введите имя столбца для фильтрации:")
        value = simpledialog.askstring("Введите значение", "Введите значение для фильтрации:")

        try:
            if value.isdigit():
                value = int(value)
        except ValueError:
            pass

        if column in self.data.columns:
            filtered_data = self.data[self.data[column] == value]
            self.text_area.delete("1.0", tk.END)
            self.text_area.insert(tk.END, filtered_data.to_string(index=False))
        else:
            messagebox.showwarning("Ошибка", "Нет данных, удовлетворяющих критериям фильтрации..")

    def check_data_loaded(self):
        if self.data is None:
            messagebox.showwarning("Предупреждение", "Сначала загрузите файл.")
            return False
        return True

    def show_error(self, message):
        messagebox.showerror("Ошибка", message)