import psycopg2
from config import host, user, password, db_name
import numpy as np
from psycopg2.extensions import register_adapter, AsIs

def add_column_table_orders():
    # адаптируем формат np.int64 в классический тип данных для распознавания модулем psycopg2
    psycopg2.extensions.register_adapter(np.int64, psycopg2._psycopg.AsIs)

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

        # добавим в таблицу 'orders' дополнительную колонку 'Стоимость_руб'
        with connection.cursor() as cursor:
            cursor.execute("""ALTER TABLE orders ADD Стоимость_руб NUMERIC;""")
        # print("[INFO] Column was successfully added")

        # рассчитаем стоимость заказов в рублях по курсу USD
        with connection.cursor() as cursor:
            cursor.execute(
                """UPDATE orders SET Стоимость_руб = ROUND(CAST ((Стоимость_$ * (SELECT course_currency FROM course_currency WHERE currency LIKE 'USD')) AS NUMERIC), 2);""")
            # print("[INFO] Calculation successful")
    except Exception as _ex:
        print("[INFO] Error while working with PostgreSQL", _ex)
    finally:
        if connection:
            connection.close()
            # print("[INFO] PostgreSQL connection closed")