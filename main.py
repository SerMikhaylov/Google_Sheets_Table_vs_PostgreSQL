# импортируем необходимые модули и библиотеки
from settings import cred_file, email
import httplib2
import googleapiclient.discovery
from oauth2client.service_account import ServiceAccountCredentials
from google_table_data_generate import data_generate_for_table
from google_table_read import gsheet2df
from create_postgresql_db import create_table_orders
from currency_course_parsing import get_currencies_dictionary, get_data
from create_table_course_currency_and_write_data import create_table_course_currency
from update_table_orders import update_orders
from add_column_table_orders_and_update import add_column_table_orders
from update_table_currency_course import pars_data_currency_cource, update_course_currency

import time

if __name__ == '__main__':
    # создаём Service-объект, для работы с Google-таблицами
    credentials_file = cred_file # имя файла с закрытым ключом google (его необходимо заменить на своё)

    # электронная почта google-аккаунта для предоставления доступа на чтение и запись к google-таблице
    email_user = email

    credentials = ServiceAccountCredentials.from_json_keyfile_name(credentials_file,
                                                                   ['https://www.googleapis.com/auth/spreadsheets',
                                                                    'https://www.googleapis.com/auth/drive'])
    httpAuth = credentials.authorize(httplib2.Http())
    service = googleapiclient.discovery.build('sheets', 'v4', http=httpAuth)

    # создаём Google-таблицу
    spreadsheet = service.spreadsheets().create(body={
        'properties': {'title': 'Заказы', 'locale': 'ru_RU'},
        'sheets': [{'properties': {'sheetType': 'GRID',
                                   'sheetId': 0,
                                   'title': 'Стоимость_заказов',
                                   'gridProperties': {'rowCount': 11, 'columnCount': 4}}}]
    }).execute()
    spreadsheetId = spreadsheet['spreadsheetId']  # сохраняем идентификатор файла
    print('[INFO] Link to google spreadsheet: https://docs.google.com/spreadsheets/d/' + spreadsheetId)

    # предоставление доступа к новому документу
    driveService = googleapiclient.discovery.build('drive', 'v3',
                                                   http=httpAuth)  # Выбираем работу с Google Drive и 3 версию API
    shareRes = driveService.permissions().create(
        fileId=spreadsheet['spreadsheetId'],
        # body={'type': 'anyone', 'role': 'reader'},  # доступ на чтение кому угодно
        body={'type': 'user', 'role': 'writer', 'emailAddress': email},
        # доступ на чтение и запись для конкретного пользователя
        fields='id'
    ).execute()
    print('[INFO] Google spreadsheet access granted successfully')

    # наполним, созданную, таблицу данными
    # зададим начальную и конечную даты для генерации сроков поставки
    start_date = '1.6.2022'
    end_date = '31.7.2022'

    values_data = data_generate_for_table(start_date, end_date)

    results = service.spreadsheets().values().batchUpdate(spreadsheetId=spreadsheetId, body={
        "valueInputOption": "USER_ENTERED",
        # Данные воспринимаются, как вводимые пользователем (считается значение формул)
        "data": [
            {"range": "Стоимость_заказов!A1:D11",
             "majorDimension": "ROWS",  # Сначала заполнять строки, затем столбцы
             "values": values_data}
        ]
    }).execute()
    print('[INFO] Data for google table generated succsessful')

    # # считываем данные из google-таблицы в dataframe pandas
    data_google_table = gsheet2df('Заказы', 0)
    print('[INFO] Google table read succsessful')

    # # создаем таблицу 'orders' в БД PostgreSQL
    import psycopg2
    from config import host, user, password, db_name
    connection = psycopg2.connect(
        host=host,
        user=user,
        password=password,
        database=db_name
    )
    create_table_orders(data_google_table)
    print("[INFO] Table orders created successfully")

    # парсим данные курса валют
    url = 'http://www.cbr.ru/scripts/XML_daily.asp'
    currency_df = get_currencies_dictionary(get_data(url))
    print('[INFO] The parsing operation of course currency was successful')

    # создаем таблицу 'course_currency' в БД PostgreSQL
    create_table_course_currency(currency_df)
    print("[INFO] Table course currency created successfully")

    # добавляем колонку в таблицу 'orders' и рассчитываем стоимость заказов в рублях по курсу ЦБ
    add_column_table_orders()
    print("[INFO] Column Стоимость_руб was successfully added and calculation successful")

    # постоянное обновление данных в таблицах по актуальному курсу валют с интервалом 1 мин
    while True:
        print('[INFO] Ждем 15 секунд до следующего обновления данных')
        time.sleep(15)  # останавливаем выполнение программы на 15 секунд

        # google-таблица могла быть обновлена другими пользователями, поэтому необходимо считать из нее все данные
        data_google_table = gsheet2df('Заказы', 0)
        print('[INFO] Google table read sucсsessful')

        # переименуем столбец "Стоимость, $" таблицы "orders" в "Стоимость_$"
        data_google_table.rename(columns={'Стоимость, $': 'Стоимость_$'}, inplace=True)

        # обновим информация в таблице 'orders' в БД PostgreSQL
        update_orders(data_google_table)

        # обновим информация курса валют в таблице 'course_currency' в БД PostgreSQL
        currency_df = pars_data_currency_cource(url)
        update_course_currency(currency_df)

        # обновляем расчет стомости заказов в рублях в таблице 'orders'
        add_column_table_orders()
