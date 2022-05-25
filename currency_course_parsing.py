# парсинг актуального курса валюты
import urllib.request
import xml.dom.minidom as minidom
from datetime import datetime
import pandas as pd

def get_data(xml_url):
    try:
        web_file = urllib.request.urlopen(xml_url)
        return web_file.read()
    except:
        pass

# извлечение информации по курсам валют из xml-файла
def get_currencies_dictionary(xml_content):
    dom = minidom.parseString(xml_content)
    dom.normalize()

    elements = dom.getElementsByTagName("Valute")
    currency_dict = {}

    for node in elements:
        for child in node.childNodes:
            if child.nodeType == 1:
                if child.tagName == 'Value':
                    if child.firstChild.nodeType == 3:
                        value = float(child.firstChild.data.replace(',', '.'))
                if child.tagName == 'CharCode':
                    if child.firstChild.nodeType == 3:
                        char_code = child.firstChild.data
        currency_dict[char_code] = value

    # запишем текущую дату и время в переменную current_datetime
    current_datetime = datetime.now()

    # запишем информацию по курсам валют и текущей дате в dataframe pandas
    currency = []
    course_currency = []
    date = []
    for key in currency_dict.keys():
        currency.append(key)
        course_currency.append(currency_dict[key])
        date.append(current_datetime)
    df = pd.DataFrame({'currency': currency, 'course_currency': course_currency, 'date': date})
    return df

if __name__ == '__main__':
    url = 'http://www.cbr.ru/scripts/XML_daily.asp'
    currency_df = get_currencies_dictionary(get_data(url))
    # print(currency_df)
