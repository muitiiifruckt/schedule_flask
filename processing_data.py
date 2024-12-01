from request import main as get_data_from_link
import pandas as pd
from io import BytesIO
import openpyxl
from openpyxl import load_workbook

def get_schedule(data, group_name):
    """
    Извлекает расписание для заданной группы из файла Excel.

    :param file_path: Путь к файлу Excel.
    :param group_name: Название группы (например, "09-141").
    :return: Расписание на неделю в виде DataFrame или сообщение об ошибке.
    """
    try:
        # Загрузка файла

        sheet_name = "Расписание"  # Предположительно основной лист
        df = pd.read_excel(data, sheet_name=sheet_name)
        
        # Поиск группы
        for row_idx, row in df.iterrows():
            for col_idx, cell in enumerate(row):
                if pd.notna(cell) and group_name in str(cell):
                    return row_idx, col_idx

        return f"Группа '{group_name}' не найдена в файле."

    except Exception as e:
        return f"Ошибка обработки файла: {e}"
def split_merged_cells(file_data):
    # Загружаем рабочую книгу
    workbook = load_workbook(file_data)
    sheet = workbook.active  # Рабочий лист

    # Получаем все объединенные ячейки
    merged_cells = list(sheet.merged_cells)

    # Разделяем объединенные ячейки
    for merged_range in merged_cells:
        min_row, min_col, max_row, max_col = merged_range.bounds
        merged_value = sheet.cell(row=min_row, column=min_col).value
        
        # Присваиваем значение во все ячейки в объединенной области
        for row in range(min_row, max_row + 1):
            for col in range(min_col, max_col + 1):
                # Убедитесь, что ячейка не является частью объединенной области
                if sheet.cell(row=row, column=col).row != min_row or sheet.cell(row=row, column=col).column != min_col:
                    sheet.cell(row=row, column=col).value = merged_value

    # Сохраняем изменения в новый файл (или перезаписываем исходный)

    return workbook
def get_column_from_cell(workbook, start_row, col_index):
    # Загружаем рабочую книгу

    print(workbook)
    sheet = workbook.active  # Рабочий лист
    for row in sheet.iter_rows(values_only=True):
        if None not in row:
            print(row)
    # Список для хранения данных
    column_data = []

    # Преобразуем номер колонки в букву, если нужно
    for row in range(start_row, sheet.max_row + 1):
        cell_value = sheet.cell(row=row, column=col_index).value
        column_data.append(cell_value)
    
    return column_data
def main(group_name = "09-141"):
    data = get_data_from_link()
    
    row, column = (get_schedule(data,group_name ))
    workbook = split_merged_cells(data)
    result = get_column_from_cell(workbook, row, column)
    return result
if __name__ == ("__main__"):
    data = main()    
    