# создадим таблицу с актуальными курсами валют в базе данных
from currency_course_parsing import get_currencies_dictionary, get_data
import psycopg2
from config import host, user, password, db_name
from sqlalchemy import create_engine
engine = create_engine('sqlite://', echo=False)

# адаптируем формат np.int64 в классический тип данных для распознавания модулем psycopg2
import numpy as np
from psycopg2.extensions import register_adapter, AsIs
psycopg2.extensions.register_adapter(np.int64, psycopg2._psycopg.AsIs)

# заполняем dataframe данными с сайта ЦБ
url = 'http://www.cbr.ru/scripts/XML_daily.asp'
currency_df = get_currencies_dictionary(get_data(url))

# разбиваем dataframe на столбцы
currency = currency_df['currency']
course_currency = currency_df['course_currency']
date = currency_df['date']

# формируем кортеж для записи данных в БД
values = []
for elem in range(len(currency_df.index)):
    tuple_values = (currency[elem], course_currency[elem], date[elem])
    values.append(tuple_values)

try:
    # подключаемся к базе данных
    connection = psycopg2.connect(
        host=host,
        user=user,
        password=password,
        database=db_name
    )
    connection.autocommit = True

    # создаем новую таблицу в базе данных для вставки в нее информации из google-таблицы
    # with connection.cursor() as cursor:
    #     cursor.execute(
    #         """CREATE TABLE course_currency(
    #             cur_ID SERIAL PRIMARY KEY NOT NULL,
    #             currency TEXT,
    #             course_currency TEXT,
    #             date TEXT
    #             );"""
    #     )
    #     print("[INFO] Table created successfully")

    # вносим в таблицу БД PostgreSQL данные курса валют
    # with connection.cursor() as cursor:
    #     data = values
    #     query = """INSERT INTO course_currency (currency, course_currency, date) VALUES (%s,%s,%s)"""
    #     cursor.executemany(query, data)
    #     print("[INFO] Data was successfully inserted")

    # обновим таблицу курса валют
    with connection.cursor() as cursor:
        currency_df.to_sql('course_currency', con=engine, if_exists='replace', index_label='ID')
    # with connection.cursor() as cursor:
    #     data = values
    #     query = """INSERT INTO course_currency (currency, course_currency, date) VALUES (%s,%s,%s)"""
    #     cursor.executemany(query, data)
        print("[INFO] Data was successfully updated")

except Exception as _ex:
    print("[INFO] Error while working with PostgreSQL", _ex)
finally:
    if connection:
        # cursor.close()
        connection.close()
        print("[INFO] PostgreSQL connection closed")