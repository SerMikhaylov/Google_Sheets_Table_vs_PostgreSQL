from currency_course_parsing import get_currencies_dictionary, get_data
from sqlalchemy import create_engine

# заполняем dataframe данными с сайта ЦБ
url = 'http://www.cbr.ru/scripts/XML_daily.asp'
currency_df = get_currencies_dictionary(get_data(url))

# обновим таблицу курса валют
engine = create_engine('postgresql://postgres@localhost:5432/postgres')
currency_df.to_sql('course_currency', con=engine, if_exists='replace')
print("[INFO] Data was successfully updated")