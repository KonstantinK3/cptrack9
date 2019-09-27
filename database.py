from sqlalchemy import Table, Column, String, Float, Date, Integer
from sqlalchemy import create_engine, MetaData, select, delete, insert, and_
import datetime

# создет таблицу, если её нет

def create_tables():
    engine = create_engine('sqlite:///data.sqlite')
    metadata = MetaData()
    codes = Table('codes', metadata,
                  Column('date', Date()), #String(255)
                  Column('code', Integer()))
    tickets = Table('tickets', metadata,
                    Column('number', String(255)),
                    Column('name', String(255)),
                    Column('surname', String(255)),
                    Column('passport', String(255)),
                    Column('issueDate', String(255)),
                    Column('dueDate', String(255)),
                    Column('areas', String(255)),
                    Column('hash', String(255)))
    metadata.create_all(engine)

# создает соединение с таблицей кодов
def get_connect_codes():
    create_tables()
    engine = create_engine('sqlite:///data.sqlite')
    metadata = MetaData()
    data = Table('codes', metadata, autoload=True, autoload_with=engine)
    connection = engine.connect()
    return data, connection

# создает соединение с таблицей билетов
def get_connect_tickets():
    create_tables()
    engine = create_engine('sqlite:///data.sqlite')
    metadata = MetaData()
    data = Table('tickets', metadata, autoload=True, autoload_with=engine)
    connection = engine.connect()
    return data, connection

#получить из базы коды на 30 дней до и 30 дней после
def get_codes_from_base(days):
    data, connection = get_connect_codes()
    stmt = select([data])

    max_date = (datetime.datetime.now() + datetime.timedelta(days=days))
    min_date = (datetime.datetime.now() - datetime.timedelta(days=days))

    stmt = stmt.where(and_(data.columns.date <= max_date,
         data.columns.date >= min_date))
    ans = connection.execute(stmt).fetchall()
    ans_list = []
    for i in ans:
        ans_list.append((str(i[0]), i[1]))
    return ans_list



# #проверка, если ли город в таблице
# def city_in_da_base(city):

#     data, connection = get_connect()

#     stmt = select([data])
#     stmt = stmt.where(data.columns.city == city)
#     results = connection.execute(stmt).fetchall()
#     if len(results) == 0:
#         return False
#     else:
#         last_time = datetime.strptime(results[0][-1], "%Y-%m-%d %H:%M:%S.%f")
#         current_time = datetime.now()
#         difference = (current_time - last_time).total_seconds()/60
#         if difference >= 30:
#             stmt_del = delete(data)
#             stmt_del = stmt_del.where(data.columns.city == city)
#             results = connection.execute(stmt_del)
#             return False
#         else:
#             return True

# #получение города из таблицы
# def get_city_from_base(city):

#     data, connection = get_connect()

#     stmt = select([data])
#     stmt = stmt.where(data.columns.city == city)
#     results = connection.execute(stmt).fetchall()[0]
#     ans = {}
#     ans["city"] = results[0]
#     ans["pressure"] = results[1]
#     ans["temp"] = results[2]
#     ans["wind"] = results[3]

#     return ans

# #запись города в таблицу
# def write_city_to_base(ans):

#     data, connection = get_connect()

#     stmt = insert(data).values(city=ans["city"], temp=ans["temp"],
#                  pressure=ans["pressure"], wind=ans["wind"],
#                  last_request=str(datetime.now()))
#     results = connection.execute(stmt)
#     return
