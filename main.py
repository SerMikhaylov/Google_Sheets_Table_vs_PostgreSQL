# импортируем необходимые модули и библиотеки
from google_table_create import *
from google_table_data_generate import results
from google_table_read import data_google_table
from create_postgresql_db import connection
from modules_for_work_postgresql_db import connection_db

if __name__ == '__main__':
    # создаем google-таблицу
    spreadsheet

    # предоставление доступа к новому документу
    driveService

    # заполняем, созданную, таблицу данными
    results

    # считываем данные из google-таблицы в dataframe pandas
    data_google_table

    # создаем таблицу 'orders' в БД PostgreSQL
    connection

    # парсим данные курса валют, создаем таблицу 'course_currency' в БД PostgreSQL
    # и рассчитываем стоимость заказов в рублях по курсу ЦБ
    connection_db

    # постоянное обновление данных в таблицах по актуальному курсу валют с интервалом 2 мин
