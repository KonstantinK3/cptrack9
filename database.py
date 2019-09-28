from sqlalchemy import Table, Column, String, Date, Integer
from sqlalchemy import create_engine, MetaData, select, and_
import datetime

# создет таблицу, если её нет


def create_tables():
    engine = create_engine('sqlite:///data.sqlite')
    metadata = MetaData()
    codes = Table('codes', metadata,
                  Column('date', Date()),  # String(255)
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

# получить из базы коды на 30 дней до и 30 дней после


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


def get_code_by_date(date):
    data, connection = get_connect_codes()
    stmt = select([data])

    date = datetime.datetime.strptime(date, '%Y-%m-%d').date()

    stmt = stmt.where(data.columns.date == date)
    ans = connection.execute(stmt).fetchall()

    return ans[0][1]
