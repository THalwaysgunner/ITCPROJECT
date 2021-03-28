import pymysql
import numpy as np
import tags as t


def update_insert_db(*data):
    """
    this is a help function, and it's purpose is to insert and, or update all collected info from 'main_data' function
    (located on the 'scraper' script) into a DB.
    this function get help from helper functions as well (insert_data_news, insert_historical_prices,
    update_financial_table, update_executive_table, delete_most_active, insert_main_data, update_data)

    :param data: by running it in 'scraper.py'  -  the entered input is all the scraped data,
    already organized.
    :return: the database tables, containing up to date info
    """

    main_data = data[0]
    data_executives = data[1]
    financial_data = data[2]
    news_data = data[3]
    price_history = data[4]

    try:
        connection = pymysql.connect(host='localhost',
                                     user='root',
                                     password=t.DB_PASS,
                                     database='stocks',
                                     cursorclass=pymysql.cursors.DictCursor)

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
        insert_main_data(main_data.loc[main_data['Symbol'].isin(sym_to_insert)])
        update_data(main_data.loc[main_data['Symbol'].isin(update)])
        return

    finally:
        connection.close()


def delete_most_active(data,connection):
    """
    this function deletes stock's info in case the following scrape no longer consists
    the stock as one of the most active stocks (e.g the stock no longer exists in the most-active page's table)
    """

    try:
        with connection.cursor() as cursor:
            for i in data:
                symbol = i

                query = 'DELETE FROM stock_general_info WHERE symbol= "{}"'.format(symbol)
                cursor.execute(query)
                connection.commit()
    except:
        return 'No data to delete from most active table'


def update_data(data,connection):
    """
    this helper function replaces the price of a certain stock, received from the scraped data from 'main_data'
    function (in 'scraper.py' script).
    the function converts the price only if the new price is different from the one currently exists in
    'stock_general_info' table.
    :param connection: connection session to the local DB
    :param data: the current scraped data (incloding the price)
    :return: a full up to date 'stock_general_info' table, with updated prices, if necessary
    """

    try:
        with connection.cursor() as cursor:
            for index, row in data.iterrows():
                symbol, price = str(row[2]), str(round(row[1], 2))

                query = 'UPDATE stock_general_info SET price = if(price <> {},{},price) WHERE symbol = "{}"'.format(price, price, symbol)
                cursor.execute(query)
                connection.commit()
    except:
        return 'No data to update in most active table'


def get_symbol_list(connection):
    """
    this helper function calls all existing stocks (=symbols) from the DB, 'stock_general_info' table,
    and return a list of them
    """
    try:
        with connection.cursor() as cursor:
                cursor.execute('SELECT symbol FROM stock_general_info')
                list_of_symbol = list(map(lambda d: d['symbol'], cursor.fetchall()))
                return list_of_symbol

    except ValueError as e:
        print(f'{e}')


def insert_main_data(data,connection):
    """
    this helper function enters all the collected data into the DB's main table - 'stock_general_info'.
    the function commits the inserts every 20 rows
    :param connection: connection session to the local DB
    :param data: the current scraped data
    :return: a full up to date 'stock_general_info' table
    """

    try:
        with connection.cursor() as cursor:
            for index, row in data.iterrows():
                symbol, name, price, volume, market, description = row[0], row[1], row[2], row[3], row[4], row[5]

                values = [symbol, name, price, volume, market, description]
                cursor.execute('INSERT INTO stock_general_info (symbol,Name_of_asset,price,volume,market_cap,description) VALUES(%s,%s,%s,%s,%s,%s)',values)

                if index % t.COMMIT_EVERY == 0:
                    connection.commit()
            connection.commit()

    except:
        return 'No data to insert into most active table'


def insert_data_executive(data,connection):
    """
    this helper function enters all the collected data scraped from 'get_executive' function (in 'scraper.py' script)
    into 'stock_executive' table
    the function commits the inserts every 20 rows
    :param connection: connection session to the local DB
    :param data: the current scraped data
    :return: a full up to date 'stock_executive' table
    """

    try:
        with connection.cursor() as cursor:
            for index, row in data.iterrows() :
                symbol, name_of_ex, title, salary = row[0], row[1], row[2], row[3]

                values = [symbol, name_of_ex, title, salary]
                cursor.execute('INSERT INTO stock_executive (symbol,name_of_ex,title,salary) VALUES(%s,%s,%s,%s)', values)

                if index % t.COMMIT_EVERY == 0:
                    connection.commit()
            connection.commit()

    except ValueError as e:
        print(f'{e}')


def insert_data_news(data,connection):
    """
    this helper function enters all the collected data scraped from 'get_news' function (in 'scraper.py' script)
    into 'news' table
    the function commits the inserts every 20 rows
    :param connection: connection session to the local DB
    :param data: the current scraped data
    :return: a full up to date 'news' table
    """

    try:
        with connection.cursor() as cursor:
            for index, row in data.iterrows():
                symbol, title, link = str(row[0]), str(row[1]), str(row[2])

                insert_q = 'INSERT INTO news (symbol,title,news_link) select DISTINCT "{}","{}","{}"  FROM news '.format(symbol,title,link)
                condition_q = 'WHERE NOT EXISTS(Select DISTINCT symbol ,title From news Where symbol = "{}" AND title = "{}")'.format(symbol, title)
                query = insert_q + condition_q
                cursor.execute(query)

                if index % t.COMMIT_EVERY == 0:
                    connection.commit()
            connection.commit()

    except ValueError as e:
        print(f'{e}')


def insert_financial_data(data,connection):
    """
    this helper function enters all the collected data scraped from 'get_financial' function (in 'scraper.py' script)
    into 'financial_info' table
    the function commits the inserts every 20 rows
    :param connection: connection session to the local DB
    :param data: the current scraped data
    :return: a full up to date 'financial_info' table
    """

    try:
        with connection.cursor() as cursor:
            for index, row in data.iterrows() :
                symbol,TTM_revenue,TTM_gross_profit,TTM_expense,TTM_cost_of_revenue = row[0],row[1],row[2],row[3],row[4]

                values = [symbol,TTM_revenue,TTM_gross_profit,TTM_expense,TTM_cost_of_revenue]
                cursor.execute('INSERT INTO financial_info (symbol,TTM_revenue,TTM_gross_profit,TTM_expense,TTM_cost_of_revenue) VALUES(%s,%s,%s,%s,%s)',values)

                if index % t.COMMIT_EVERY == 0:
                    connection.commit()
            connection.commit()

    except ValueError as e :
        print(f'{e}')


def insert_historical_prices(data,connection):
    """
    this helper function enters current collected data scraped from 'get_historical_prices' function
    (in 'scraper.py' script) into 'historical_prices' table
    the function commits the inserts every 20 rows
    :param connection: connection session to the local DB
    :param data: the current scraped data
    :return: a full up to date 'financial_info' table
    """

    try:
        with connection.cursor() as cursor:
            for index, row in data.iterrows():
                Symbol, Price, Date = row[0], row[1], row[2]

                values = [Symbol, Date, Price]
                cursor.execute('INSERT INTO historical_prices (Symbol,Date,Price) VALUES(%s,%s,%s)',values)

                if index % t.COMMIT_EVERY == 0:
                    connection.commit()
            connection.commit()

    except ValueError as e :
        print(f'{e}')


def update_financial_table(data,connection):
    """
    this helper function replaces some updated data scraped from 'get_financial' function (in 'scraper.py' script)
    the function converts the data only if the new scraped data changed from the one currently exists in
    'financial_info' table.
    :param connection: connection session to the local DB
    :param data: the current scraped data
    :return: a full up to date 'financial_info' table, with some updated features, if exist
    """

    try:
        with connection.cursor() as cursor:
            for index, row in data.iterrows() :
                symbol, revenue , gross_profit, expense , cost = row[0], row[1],row[2],row[3],row[4]

                query_revenue = 'UPDATE financial_info SET TTM_revenue = if(TTM_revenue <> "{}","{}",TTM_revenue) WHERE symbol = "{}"'.format(revenue,revenue,symbol)
                query_gross_profit = 'UPDATE financial_info SET TTM_gross_profit = if(TTM_gross_profit <> "{}","{}",TTM_gross_profit) WHERE symbol = "{}"'.format(gross_profit, gross_profit, symbol)
                query_expense = 'UPDATE financial_info SET TTM_expense = if(TTM_expense <> "{}","{}",TTM_expense) WHERE symbol = "{}"'.format(expense, expense, symbol)
                query_cost = 'UPDATE financial_info SET TTM_cost_of_revenue = if(TTM_cost_of_revenue <> "{}","{}",TTM_cost_of_revenue) WHERE symbol = "{}"'.format(cost, cost, symbol)

                cursor.execute(query_revenue)
                cursor.execute(query_gross_profit)
                cursor.execute(query_expense)
                cursor.execute(query_cost)
                connection.commit()

    except ValueError as e :
        print(f'{e}')


def update_executive_table(data, connection):
    """
    this helper function replaces some updated data scraped from 'get_executive' function (in 'scraper.py' script).
    the function converts the data only if the new scraped data changed from the one currently exists in
    'stock_executive' table.
    :param connection session to the local DB
    :param data: the current scraped data
    :return: a full up to date 'stock_executive' table, with some updated features, if exist
    """
    try:
        with connection.cursor() as cursor:
            for index, row in data.iterrows():
                symbol, name, title, salary,  = row[0], str(row[1]), str(row[2]), str(row[3])

                query_name_of_ex = 'UPDATE stock_executive SET name_of_ex = if(name_of_ex <> "{}","{}",name_of_ex) WHERE symbol = "{}" AND title = "{}"'.format(name, name, symbol, title)
                query_salary = 'UPDATE stock_executive SET salary = if(salary <> "{}","{}",salary) WHERE symbol = "{}" AND name_of_ex = "{}"'.format(salary, salary, symbol, name)

                cursor.execute(query_name_of_ex)
                cursor.execute(query_salary)

                connection.commit()

    except ValueError as e:
        print(f'{e}')



