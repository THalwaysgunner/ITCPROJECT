import pymysql
import numpy as np


def update_insert_db(*data):
    main_data = data[0]
    data_executives = data[1]
    financial_data = data[2]
    news_data = data[3]
    price_history = data[4]

    insert_data_news(news_data)
    insert_historical_prices(price_history)

    update_executive_table(data_executives)
    update_financial_table(financial_data)

    new_sym = main_data['Symbol']
    current_sym = get_symbol_list()
    sym_to_delete = np.setdiff1d(current_sym, new_sym)
    sym_to_insert = np.setdiff1d(new_sym, current_sym)
    update = np.setdiff1d(new_sym, sym_to_insert)

    delete_most_active(sym_to_delete)
    insert_main_data(sym_to_insert)
    update_data(update)
    return


def delete_most_active(data):
    connection = pymysql.connect(host='localhost',
                                 user='root',
                                 password='Haim8101040',
                                 database='stocks',
                                 cursorclass=pymysql.cursors.DictCursor)

    try:
        with connection.cursor() as cursor:
            for index, row in data.iterrows():
                symbol = str(row[0])

                query = 'DELETE FROM main_data WHERE symbol= "{}"'.format(symbol)
                cursor.execute(query)
                connection.commit()

    finally:
        connection.close()


def update_data(data):

    connection = pymysql.connect(host='localhost',
                                 user='root',
                                 password='Haim8101040',
                                 database='stocks',
                                 cursorclass=pymysql.cursors.DictCursor)

    try:
        with connection.cursor() as cursor:
            for index, row in data.iterrows() :
                symbol, price= str(row[2]), str(round(row[1],2))

                query = 'UPDATE main_data SET price = if(price <> {},{},price) WHERE symbol = "{}"'.format(price,price,symbol)
                cursor.execute(query)
                connection.commit()

    finally:
        connection.close()


def get_symbol_list():

    connection = pymysql.connect(host='localhost',
                                 user='root',
                                 password='Haim8101040',
                                 database='stocks',
                                 cursorclass=pymysql.cursors.DictCursor)


    try:
        with connection.cursor() as cursor:
                cursor.execute('SELECT symbol FROM main_data')
                list_of_symbol = list(map(lambda d: d['symbol'], cursor.fetchall()))
                return list_of_symbol
    finally:
        connection.close()


def insert_main_data(data):

    connection = pymysql.connect(host='localhost',
                                 user='root',
                                 password='Haim8101040',
                                 database='stocks',
                                 cursorclass=pymysql.cursors.DictCursor)

    commit_every = 20

    try:
        with connection.cursor() as cursor:
            for index, row in data.iterrows():
                symbol, name, price, volume, market, description = row[0], row[1], row[2], row[3], row[4], row[5]

                values = [symbol, name, price, volume, market, description]
                cursor.execute('INSERT INTO main_data (symbol,Name_of_asset,price,volume,market_cap,description) VALUES(%s,%s,%s,%s,%s,%s)',values)

                if index % commit_every == 0:
                    connection.commit()
            connection.commit()

    finally:
        connection.close()


def insert_data_executive(data):

    connection = pymysql.connect(host='localhost',
                                 user='root',
                                 password='Haim8101040',
                                 database='stocks',
                                 cursorclass=pymysql.cursors.DictCursor)

    commit_every = 20

    try:
        with connection.cursor() as cursor:
            for index, row in data.iterrows() :
                symbol,name_of_ex,title,salary= row[0],row[1],row[2],row[3]

                values = [symbol,name_of_ex,title,salary]
                cursor.execute('INSERT INTO data_executive (symbol,name_of_ex,title,salary) VALUES(%s,%s,%s,%s)',values)

                if index % commit_every == 0:
                    connection.commit()
            connection.commit()

    finally:
        connection.close()


def insert_data_news(data):

    connection = pymysql.connect(host='localhost',
                                 user='root',
                                 password='Haim8101040',
                                 database='stocks',
                                 cursorclass=pymysql.cursors.DictCursor)

    commit_every = 20

    try:
        with connection.cursor() as cursor:
            for index, row in data.iterrows():
                symbol, title, link = row[0], row[1], row[2]

                insert_q = 'INSERT INTO news_data (symbol,title,news_link) select DISTINCT "{}","{}","{}"  FROM news_data '.format(symbol,title,link)
                condition_q = 'WHERE NOT EXISTS(Select DISTINCT symbol ,title From news_data Where symbol = "{}" AND title = "{}")'.format(symbol, title)
                query = insert_q + condition_q
                cursor.execute(query)

                if index % commit_every == 0:
                    connection.commit()
            connection.commit()

    finally:
        connection.close()


def insert_financial_data(data):

    connection = pymysql.connect(host='localhost',
                                 user='root',
                                 password='Haim8101040',
                                 database='stocks',
                                 cursorclass=pymysql.cursors.DictCursor)

    commit_every = 20

    try:
        with connection.cursor() as cursor:
            for index, row in data.iterrows() :
                symbol,TTM_revenue,TTM_gross_profit,TTM_expense,TTM_cost_of_revenue = row[0],row[1],row[2],row[3],row[4]

                values = [symbol,TTM_revenue,TTM_gross_profit,TTM_expense,TTM_cost_of_revenue]
                cursor.execute('INSERT INTO financial_data (symbol,TTM_revenue,TTM_gross_profit,TTM_expense,TTM_cost_of_revenue) VALUES(%s,%s,%s,%s,%s)',values)

                if index % commit_every == 0:
                    connection.commit()
            connection.commit()

    finally:
        connection.close()


def insert_historical_prices(data):

    connection = pymysql.connect(host='localhost',
                                 user='root',
                                 password='Haim8101040',
                                 database='stocks',
                                 cursorclass=pymysql.cursors.DictCursor)

    commit_every = 20

    try:
        with connection.cursor() as cursor:
            for index, row in data.iterrows():
                Symbol, Price, Date = row[0], row[1], row[2]

                values = [Symbol, Date, Price]
                cursor.execute('INSERT INTO historical_prices (Symbol,Date,Price) VALUES(%s,%s,%s)',values)

                if index % commit_every == 0:
                    connection.commit()
            connection.commit()

    finally:
        connection.close()


connection = pymysql.connect(host='localhost',
                             user='root',
                             password='Haim8101040',
                             database='stocks',
                             cursorclass=pymysql.cursors.DictCursor)

def update_financial_table(data):

    connection = pymysql.connect(host='localhost',
                                 user='root',
                                 password='Haim8101040',
                                 database='stocks',
                                 cursorclass=pymysql.cursors.DictCursor)

    try:
        with connection.cursor() as cursor:
            for index, row in data.iterrows() :
                symbol, revenue , gross_profit, expense , cost = row[0], str(round(row[1],3)),str(round(row[2],3)),str(round(row[3],3)),str(round(row[4],3))

                query_revenue = 'UPDATE financial_data SET TTM_revenue = if(TTM_revenue <> {},{},TTM_revenue) WHERE symbol = "{}"'.format(revenue,revenue,symbol)
                query_gross_profit = 'UPDATE financial_data SET TTM_gross_profit = if(TTM_gross_profit <> {},{},TTM_gross_profit) WHERE symbol = "{}"'.format(gross_profit, gross_profit, symbol)
                query_expense = 'UPDATE financial_data SET TTM_expense = if(TTM_expense <> {},{},TTM_expense) WHERE symbol = "{}"'.format(expense, expense, symbol)
                query_cost = 'UPDATE financial_data SET TTM_cost_of_revenue = if(TTM_cost_of_revenue <> {},{},TTM_cost_of_revenue) WHERE symbol = "{}"'.format(cost, cost, symbol)

                cursor.execute(query_revenue)
                cursor.execute(query_gross_profit)
                cursor.execute(query_expense)
                cursor.execute(query_cost)
                connection.commit()

    finally:
        connection.close()


def update_executive_table(data):

    connection = pymysql.connect(host='localhost',
                                 user='root',
                                 password='Haim8101040',
                                 database='stocks',
                                 cursorclass=pymysql.cursors.DictCursor)

    try:
        with connection.cursor() as cursor:
            for index, row in data.iterrows() :
                symbol, name , title, salary ,  = row[0], str(row[1]) ,str(row[2]),str(row[3])

                query_name_of_ex = 'UPDATE data_executive SET name_of_ex = if(name_of_ex <> {},{},name_of_ex) WHERE symbol = "{}" AND title = "{}"'.format(name,name,symbol,title)
                query_salary = 'UPDATE data_executive SET salary = if(salary <> {},{},salary) WHERE symbol = "{}" AND name_of_ex = "{}"'.format(salary, salary, symbol,name)

                cursor.execute(query_name_of_ex)
                cursor.execute(query_salary)

                connection.commit()

    finally:
        connection.close()


