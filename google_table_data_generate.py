# импортируем библиотеки
import random
import time

# функция для генерирования данных, которыми можно заполнить ячейки google-таблицы
def data_generate_for_table(start_date, end_date):
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

    delivery_time = [randomDate(start_date, end_date, (random.randint(1, 100) / 100)) for i in range(len(number))]

    # группируем данные по строкам
    values_data.append(header_table)
    for elem in range(len(number)):
        row_values = [number[elem], zakaz[elem], price[elem], delivery_time[elem]]
        values_data.append(row_values)

    return values_data
