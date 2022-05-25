# импортируем библиотеки
import httplib2
import googleapiclient.discovery
from oauth2client.service_account import ServiceAccountCredentials
import random
# import datetime
import time


# создаём Service-объект, для работы с Google-таблицами
credentials_file = 'testproject-350906-c98595dad553.json'  # имя файла с закрытым ключом (его необходимо заменить на свое)

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
print('https://docs.google.com/spreadsheets/d/' + spreadsheetId)

# предоставление доступа к новому документу
driveService = googleapiclient.discovery.build('drive', 'v3', http=httpAuth) # Выбираем работу с Google Drive и 3 версию API
shareRes = driveService.permissions().create(
    fileId=spreadsheet['spreadsheetId'],
    # body={'type': 'anyone', 'role': 'reader'},  # доступ на чтение кому угодно
    # body={'type': 'user', 'role': 'writer', 'emailAddress': 'ks.test.task@gmail.com'},
    body={'type': 'user', 'role': 'writer', 'emailAddress': 'irbispro10@gmail.com'},
    # доступ на запись для конкретного пользователя
    fields='id'
).execute()

# Заполнение ячеек таблицы данными
values_data = []
header_table = ['№', 'Заказ №', 'Стоимость, $', 'Срок поставки']
number = []
zakaz = []
price = []
delivery_time = []

# генерируем числа для заполнения первого столбца таблицы "№"
for i in range(10):
    number.append(i + 1)

# генерируем случайные числа для столбца "Заказ №"
zakaz = [random.randint(1000000, 2000000) for i in range(len(number))]

# генерируем случайные числа для столбца "Стоимость $"
price = [random.randint(100, 2000) for i in range(len(number))]

# генерируем случайные даты поставок для столбца "Срок поставки"
def strTimeProp(start, end, format, prop):
    """start и end должны быть строками, указывающими время в заданном формате (стиль strftime),
    определяющими интервал [start, end].
    prop - коэффициент, необходимый для генерации случайной даты.
    Возвращаемое время будет в указанном формате.
    """

    stime = time.mktime(time.strptime(start, format))
    etime = time.mktime(time.strptime(end, format))

    ptime = stime + prop * (etime - stime)

    return time.strftime(format, time.localtime(ptime))

def randomDate(start, end, prop):
    return strTimeProp(start, end, '%d.%m.%Y', prop)

start_date = '1.5.2022'
end_date = '31.5.2022'
delivery_time = [randomDate(start_date, end_date, (random.randint(1, 100) / 100)) for i in range(len(number))]

# группируем данные по строкам
values_data.append(header_table)
for elem in range(len(number)):
    row_values = [number[elem], zakaz[elem], price[elem], delivery_time[elem]]
    values_data.append(row_values)

# заполняем таблицу данными
results = service.spreadsheets().values().batchUpdate(spreadsheetId = spreadsheetId, body = {
    "valueInputOption": "USER_ENTERED", # Данные воспринимаются, как вводимые пользователем (считается значение формул)
    "data": [
        {"range": "Стоимость_заказов!A1:D11",
         "majorDimension": "ROWS",     # Сначала заполнять строки, затем столбцы
         "values": values_data}
    ]
}).execute()
