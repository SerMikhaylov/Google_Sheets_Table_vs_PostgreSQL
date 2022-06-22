from settings import cred_file
import gspread
from oauth2client.service_account import ServiceAccountCredentials as sac
import pandas as pd

# функция для извлечения данных из электронной таблицы
def gsheet2df(spreadsheet_name, sheet_num):
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    # создаём Service-объект, для работы с Google-таблицами
    credentials_file = cred_file  # имя файла с закрытым ключом (его необходимо заменить на своё)

    credentials = sac.from_json_keyfile_name(credentials_file, scope)
    client = gspread.authorize(credentials)

    sheet = client.open(spreadsheet_name).get_worksheet(sheet_num).get_all_records()
    df = pd.DataFrame.from_dict(sheet)

    return df