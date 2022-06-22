import psycopg2
from config import host, user, password, db_name
import numpy as np
from psycopg2.extensions import register_adapter, AsIs

def create_table_course_currency(df):
    # адаптируем формат np.int64 в классический тип данных для распознавания модулем psycopg2
    psycopg2.extensions.register_adapter(np.int64, psycopg2._psycopg.AsIs)

    # разбиваем dataframe на столбцы
    currency = df['currency']
    course_currency = df['course_currency']
    date = df['date']

    # формируем кортеж для записи данных в БД
    values = []
    for elem in range(len(df.index)):
        tuple_values = (currency[elem], course_currency[elem], date[elem])
        values.append(tuple_values)

    try:
        # подключаемся к базе данных
        global connection
        connection = psycopg2.connect(
            host=host,
            user=user,
            password=password,
            database=db_name
        )
        connection.autocommit = True

        # создаем новую таблицу в базе данных для вставки в нее информации
        with connection.cursor() as cursor:
            cursor.execute(
                """CREATE TABLE course_currency(
                    cur_ID SERIAL PRIMARY KEY NOT NULL,
                    currency TEXT,
                    course_currency NUMERIC,
                    date VARCHAR(50)
                    );"""
            )

        # вносим в таблицу БД PostgreSQL данные курса валют
        with connection.cursor() as cursor:
            data = values
            query = """INSERT INTO course_currency (currency, course_currency, date) VALUES (%s,%s,%s)"""
            cursor.executemany(query, data)
            # print("[INFO] Data was successfully inserted")
    except Exception as _ex:
        print("[INFO] Error while working with PostgreSQL", _ex)
    finally:
        if connection:
            connection.close()
            # print("[INFO] PostgreSQL connection closed")