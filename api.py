from PyInquirer import prompt
from examples import custom_style_2
from prompt_toolkit.validation import Validator, ValidationError
import yfinance as yf
from datetime import datetime
import matplotlib.pyplot as plt


class Validator(Validator):

    def validate(self, document):
        try:
            str(document.text)
        except ValueError:
            raise ValidationError(message="Please enter a stock symbol",
                                  cursor_position=len(document.text))


questions = [
    {
        'type': 'list',
        'name': 'user_option',
        'message': 'in order to get stocks data please choose from the option bellow',
        'choices': ["graph","holder","balance", "cash_flow","earning"]
    },

    {
        'type': "input",
        "name": "symbol",
        "message": "please enter a symbol",
        "validate": Validator,
        "filter": lambda val: str(val)
    }
]

question_graph = [
    {
        'type': "input",
        "name": "start_date",
        "message": "please add a start date (iso format) '2020-1-1",
        "validate": Validator,
        "filter": lambda val: str(val)
    },


    {
        'type' : "input",
        "name" : "end date",
        "message" : "please add a end date (iso format) '2020-1-1",
        "validate" : Validator,
        "filter" : lambda val : str(val)
    },


    {
        'type' : "input",
        "name" : "period",
        "message" : "please Enter period of time"
                    "valid periods: 1d,5d,1mo,3mo,6mo,1y,2y,5y,10y,ytd,max,",
        "validate" : Validator,
        "filter" : lambda val : str(val)
    }

]


def get_from_scraper(symbol):
    data_major_holders, data_institutional_holders = get_stock_holder(symbol)
    data_balance = get_balance(symbol)
    data_cash_flow = get_cash_flow(symbol)
    data_earning = get_earning(symbol)


def get_stock_graph_in_range(tickers,sd,ed=None,p='1d'):

    ticker = tickers
    start_date = sd
    period = p

    if ed is None:
        end_date = datetime.today().isoformat()
    try:
        ticker_data = yf.Ticker(ticker)
        data_hist = ticker_data.history(period=period, start=start_date, end=end_date[:10])

        data_hist['Close'].plot()
        plt.show()

    except ValueError as e:
        print(e)


def get_stock_holder(ticker):
    data = yf.Ticker(ticker)
    return data.major_holders, data.institutional_holders


def get_balance(ticker):
    data = yf.Ticker(ticker)
    return data.balance_sheet


def get_cash_flow(ticker):
    data = yf.Ticker(ticker)
    return data.cashflow


def get_earning(ticker):
    data = yf.Ticker(ticker)
    return data.earnings


def get_data_from_api():
    functions_dict = {'graph' : get_stock_graph_in_range, 'holder': get_stock_holder, 'balance': get_balance,
                      'cash_flow': get_cash_flow, 'earning': get_earning}

    answers = prompt(questions, style=custom_style_2)
    symbol = answers.get("symbol")

    func = functions_dict[answers.get('user_option')]

    if answers.get("user_option") == "graph" :
        answer_graph = prompt(question_graph, style=custom_style_2)
        start_date = answer_graph.get("start_date")
        end_date = answer_graph.get("end_date")
        period = answer_graph.get("period")
        print(func(symbol, start_date, end_date, period))
    else:
        print(func(symbol))

