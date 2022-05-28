# импортируем библиотеки
import httplib2
import googleapiclient.discovery
from oauth2client.service_account import ServiceAccountCredentials

# создаём Service-объект, для работы с Google-таблицами
credentials_file = 'testproject-350906-c98595dad553.json'  # имя файла с закрытым ключом (его необходимо заменить на свой)

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
print('Ссылка на google-таблицу: https://docs.google.com/spreadsheets/d/' + spreadsheetId)

# предоставление доступа к новому документу
driveService = googleapiclient.discovery.build('drive', 'v3',
                                               http=httpAuth)  # Выбираем работу с Google Drive и 3 версию API
shareRes = driveService.permissions().create(
    fileId=spreadsheet['spreadsheetId'],
    # body={'type': 'anyone', 'role': 'reader'},  # доступ на чтение кому угодно
    body={'type': 'user', 'role': 'writer', 'emailAddress': 'ks.test.task@gmail.com'},
    # доступ на чтение и запись для конкретного пользователя
    fields='id'
).execute()
print('[INFO] Google spreadsheet access granted successfully')
