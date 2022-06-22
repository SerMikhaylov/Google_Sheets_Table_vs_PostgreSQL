from currency_course_parsing import get_currencies_dictionary, get_data
from sqlalchemy import create_engine

# заполняем dataframe данными с сайта ЦБ
def pars_data_currency_cource(url):
    currency_df = get_currencies_dictionary(get_data(url))
    return currency_df

# обновим таблицу курса валют
def update_course_currency(currency_df):
    engine = create_engine('postgresql://postgres@localhost:5432/postgres')
    currency_df.to_sql('course_currency', con=engine, if_exists='replace')
    return print("[INFO] Data was successfully updated in table 'course_currency")