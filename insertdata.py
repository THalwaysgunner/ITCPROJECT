import pymysql


def insert_main_data(data):

    connection = pymysql.connect(host='localhost',
                                 user='root',
                                 password='Haim8101040',
                                 database='stocks',
                                 cursorclass=pymysql.cursors.DictCursor)

    commit_every = 20

    try:
        with connection.cursor() as cursor:
            for index, row in data.iterrows() :
                symbol,name,price,volume,market,description = row[0],row[1],row[2],row[3],row[4],row[5]

                values = [symbol,name,price,volume,market,description]
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
            for index, row in data.iterrows() :
                symbol,title,link = row[0],row[1],row[2]

                values = [symbol,title,link]
                cursor.execute('INSERT INTO news_data (symbol,title,news_link) VALUES(%s,%s,%s)',values)

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

