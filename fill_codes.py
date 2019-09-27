from sqlalchemy import Table, Column, String, Float, Date, Integer
from sqlalchemy import create_engine, MetaData, select, delete, insert
from datetime import datetime
import datetime
from database import create_tables
import random

# создает соединение с таблицей кодов
def get_connect_codes():
    create_tables()
    engine = create_engine('sqlite:///data.sqlite')
    metadata = MetaData()
    data = Table('codes', metadata, autoload=True, autoload_with=engine)
    connection = engine.connect()
    return data, connection

#заполнение кодов по заданным датам
def fill_codes(start_date, days):

    data, connection = get_connect_codes()

    start_date = datetime.datetime.strptime(start_date, "%Y-%m-%d").date()
    values_list = []

    for i in range(days):
        current_date = (start_date + datetime.timedelta(days=i)) #str
        current_code = random.randint(10000,99999)
        values_list.append({'date': current_date, 'code': current_code})

    stmt = insert(data)
    results = connection.execute(stmt, values_list)

    print(results.rowcount)
    return

fill_codes('2019-01-01', 1000)
