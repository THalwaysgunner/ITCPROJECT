
from prompt_toolkit.validation import Validator, ValidationError
import yfinance as yf
from datetime import datetime
import matplotlib.pyplot as plt
import config_logger as cfl
import time
import uuid
from datetime import datetime
import inquirer


class Validator(Validator):

    def validate(self, document):
        try:
            str(document.text)
            cfl.logging.info(f'valide parameter')
        except ValueError:
            raise ValidationError(message="Please enter a stock symbol",
                                  cursor_position=len(document.text))


questions = [
    inquirer.List('user_option',
                  message='in order to get stocks data please choose from the option bellow',
                  choices=["graph","holder","balance", "cash_flow","earning"]),

    inquirer.Text('symbol',
                  message='please enter a symbol')

]


question_graph = [

    inquirer.Text('start_date',
                  message="please add a start date (iso format) '2020-1-1"
                  ),
    inquirer.Text('end date',
                  message="please add a end date (iso format) '2021-1-1"
                  ),
    inquirer.Text('period',
                  message="please Enter period of time\nvalid periods: 1d,5d,1mo,3mo,6mo,1y,2y,5y,10y,ytd,max"
                  )

]


def get_from_scraper(symbol):
    """
    the function will retrieve new data and store it into local DB
    :param symbol: the data symbol
    :return: data frames with the new data.
    """
    data_major_holders, data_institutional_holders = get_stock_holder(symbol)
    data_balance = get_balance(symbol)
    data_cash_flow = get_cash_flow(symbol)
    data_earning = get_earning(symbol)


def get_stock_graph_in_range(tickers,sd,ed=None,p='1d'):
    """"
    the function get a start date and end date follow by a interval period of time
    and plot the stock price for the specific symbol and time interval"""

    ticker = tickers
    start_date = sd
    period = p

    if ed is None:
        end_date = datetime.today().isoformat()
    try:
        ticker_data = yf.Ticker(ticker)
        cfl.logging.info(f'retrieve data for {ticker} successfully before ploting ')
        data_hist = ticker_data.history(period=period, start=start_date, end=end_date[:10])

        data_hist['Close'].plot()
        plt.show()

    except ValueError as e:
        cfl.logging.error(f'failed to fetch data for {ticker} from api')
        print(e)


def get_stock_holder(ticker):
    try:
        data = yf.Ticker(ticker)
        cfl.logging.info(f'successful retrieve holders data for {ticker}  ')
        print(f'Holders representation for {ticker}')
        print(data.major_holders)
        print('\n')
        print(f'detailed Holders  for {ticker}')
        print(data.institutional_holders)
        return

    except ValueError as e :
        cfl.logging.error(f'failed to fetch holder data for {ticker} from api')
        print(e)


def get_balance(ticker):

    try:
        data = yf.Ticker(ticker)
        cfl.logging.info(f'successful retrieve balance data for {ticker}  ')
        print(f'balance for {ticker}')
        print(data.balance_sheet)
        return

    except ValueError as e :
        cfl.logging.error(f'failed to fetch balance data for {ticker} from api')
        print(e)


def get_cash_flow(ticker):

    try:
        data = yf.Ticker(ticker)
        cfl.logging.info(f'successful retrieve cash_flow data for {ticker}  ')
        print(f'cash flow for {ticker}')
        print(data.cashflow)
        return

    except ValueError as e :
        cfl.logging.error(f'failed to fetch cash_flow data for {ticker} from api')
        print(e)


def get_earning(ticker):

    try:
        data = yf.Ticker(ticker)
        cfl.logging.info(f'successful retrieve earning data for {ticker}  ')
        print(f'earnings for {ticker}')
        print(data.earnings)
        return

    except ValueError as e :
        cfl.logging.error(f'failed to fetch earning data for {ticker} from api')
        print(e)


def get_data_from_api():
    """
    the function will get a symbol and fetch the data from an api based on the user choice
    every api call will get a unique id so we can differ it from other call and a start/end time
    for every functions call log will be saved into the log file (log folder) with a main log
    and a specific log for the call
    :return:
    """
    s_date = datetime.now()
    uid = uuid.uuid1()
    start_time = time.time()
    cfl.logging.info(f'new session num  {uid} was created at {s_date} ')

    functions_dict = {'graph' : get_stock_graph_in_range, 'holder': get_stock_holder, 'balance': get_balance,
                      'cash_flow': get_cash_flow, 'earning': get_earning}

    answers = inquirer.prompt(questions)
    symbol = answers.get("symbol")

    func = functions_dict[answers.get('user_option')]

    if answers.get("user_option") == "graph" :
        answer_graph = inquirer.prompt(question_graph)
        start_date = answer_graph.get("start_date")
        end_date = answer_graph.get("end_date")
        period = answer_graph.get("period")
        e_date = datetime.now()
        end_time = time.time()
        print(f"{func(symbol, start_date, end_date, period)}\n")
        cfl.logging.info(f' session {uid} end at : {e_date}  ')
        cfl.logging.info(f'the time it took to get data from api for session {uid} is: {end_time - start_time}  ')
        return

    else:
        end_time = time.time()
        e_date = datetime.now()
        print(f"{func(symbol)}\n\n")
        cfl.logging.info(f' session {uid} end at : {e_date}  ')
        cfl.logging.info(f'the time it took to get data from api for session {uid} is: {end_time - start_time}  ')
        return

