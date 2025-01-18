import pandas as pd
import sqlite3

def load_data(file_path):
    if file_path.endswith('.csv'):
        return pd.read_csv(file_path)
    elif file_path.endswith('.xlsx'):
        return pd.read_excel(file_path)
    elif file_path.endswith('.json'):
        return pd.read_json(file_path)
    elif file_path.endswith('.sqlite3'):
        return load_sqlite_data(file_path)
    else:
        raise ValueError("Неподдерживаемый формат файла.")

def load_sqlite_data(file_path):
    conn = sqlite3.connect(file_path)
    tables = pd.read_sql_query("SELECT name FROM sqlite_master WHERE type='table';", conn)
    if not tables.empty:
        table_name = tables.iloc[0]['name']
        return pd.read_sql_query(f"SELECT * FROM {table_name}", conn)
    else:
        raise ValueError("В базе данных нет таблиц.")