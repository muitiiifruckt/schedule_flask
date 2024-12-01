from processing_data import main as get_data
import pandas as pd

schedule_data = get_data()

def transform_schedule(schedule_data):
    """
    Преобразует список данных в таблицу расписания с днями недели в качестве столбцов и временем проведения пар как строки.
    Учитывается, что в день максимум 7 пар.
    
    :param schedule_data: Список с расписанием, включая дни недели и их значения.
    :return: DataFrame с преобразованным расписанием.
    """
    try:
        # Дни недели для группировки
        days = ['пн', 'вт', 'ср', 'чт', 'пт', 'сб', 'вс']
        
        # Создаем DataFrame из данных
        schedule_df = pd.DataFrame({'data': schedule_data})
        
        # Определяем индексы дней недели
        day_indices = schedule_df[schedule_df['data'].isin(days)].index.tolist()
        
        # Добавляем последний индекс, чтобы корректно обработать диапазон
        day_indices.append(len(schedule_df))
        
        # Формируем расписание по дням
        schedule_dict = {}
        for i in range(len(day_indices) - 1):
            day = schedule_df.iloc[day_indices[i]]['data']
            day_values = schedule_df.iloc[day_indices[i] + 1 : day_indices[i + 1]]['data'].tolist()
            schedule_dict[day] = day_values
        
        # Максимальное количество пар в день
        max_pairs_per_day = 7
        
        # Выравниваем расписание по количеству пар (максимум 7)
        for day in schedule_dict:
            # Если пар меньше 7, добавляем "Пусто"
            schedule_dict[day] += ['Пусто'] * (max_pairs_per_day - len(schedule_dict[day]))
            # Ограничиваем количество пар 7
            schedule_dict[day] = schedule_dict[day][:max_pairs_per_day]
        
        # Преобразуем в DataFrame
        transformed_df = pd.DataFrame(schedule_dict)
        transformed_df.index = [f"Пара {i + 1}" for i in range(max_pairs_per_day)]
        
        return transformed_df
    
    except Exception as e:
        return f"Ошибка преобразования: {e}"
result_df = transform_schedule(schedule_data)
print(result_df["вт"])