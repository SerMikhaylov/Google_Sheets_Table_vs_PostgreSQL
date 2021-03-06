# импортируем необходимые данные и библиотеки
import psycopg2
from config import host, user, password, db_name
import numpy as np
from psycopg2.extensions import register_adapter, AsIs

def create_table_orders(df):
    # адаптируем формат np.int64 в классический тип данных для распознавания модулем psycopg2
    psycopg2.extensions.register_adapter(np.int64, psycopg2._psycopg.AsIs)

    # разбиваем dataframe на столбцы
    number = df['№']
    zakaz = df['Заказ №']
    price = df['Стоимость, $']
    delivery_time = df['Срок поставки']

    # формируем кортеж для записи данных в БД
    values = []
    for elem in range(len(df.index)):
        tuple_values = (number[elem], zakaz[elem], price[elem], delivery_time[elem])
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

        # создаем новую таблицу в базе данных для вставки в нее информации из google-таблицы
        with connection.cursor() as cursor:
            cursor.execute(
                """CREATE TABLE orders(
                    Num_ SERIAL PRIMARY KEY NOT NULL,
                    Заказ INT,
                    Стоимость_$ INT,
                    Срок_поставки varchar (30)
                    );"""
            )

        # вносим в таблицу БД PostgreSQL данные из google-таблицы
        with connection.cursor() as cursor:
            data = values
            query = """INSERT INTO orders (num_, Заказ, Стоимость_$, Срок_поставки) VALUES (%s,%s,%s,%s)"""
            cursor.executemany(query, data)
            # print("[INFO] Data was successfully inserted")

    except Exception as _ex:
        print("[INFO] Error while working with PostgreSQL", _ex)
    finally:
        if connection:
            connection.close()
            # print("[INFO] PostgreSQL connection closed")