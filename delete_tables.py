import psycopg2
from config import host, user, password, db_name

try:
    # подключаемся к базе данных
    # global connection
    connection = psycopg2.connect(
        host=host,
        user=user,
        password=password,
        database=db_name
    )
    connection.autocommit = True

    with connection.cursor() as cursor:
        cursor.execute(
            """DROP TABLE orders;"""
        )

    with connection.cursor() as cursor:
        cursor.execute(
            """DROP TABLE course_currency;"""
        )

except Exception as _ex:
    print("[INFO] Error while working with PostgreSQL", _ex)
finally:
    if connection:
        connection.close()
        print("[INFO] Tables delete successful")
        print("[INFO] PostgreSQL connection closed")