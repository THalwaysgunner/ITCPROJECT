#  packages and modules to import
import requests
from datetime import datetime
import time
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from insert_and_update_db import update_insert_db
from ID_GENERATOR import get_id
import config_logger as cfl
from api_s import *
import tags as t

options = Options()
options.headless = True
options.add_argument("--window-size=1920,1200")


class Scraper:
    def __init__(self, save=False):
        """initiate the structure,
        the function's default mode is only printing the output, without saving it"""
        self.soup = self.get_soup()
        self.save = save

    @staticmethod
    def get_soup():
        """
        this function gets the content from the page and converts it via BeautifulSoup
        """
        try:
            page = requests.get(t.URL)
            soup = BeautifulSoup(page.content, t.HTML_PARSER)
            return soup
        except ValueError:
            print('OOPS! ERROR {}'.format(page.status_code))

    def scrape_all(self, symbol_choice=None):
        """
        this function saves or prints (upon the CLI command) entered data
        into a database made out of numerous tables
        the function gets the data by calling "get_data" function.
        """
        table = self.get_table()

        main_data, data_executives, financial_data, news_data, price_history = self.get_data(table, symbol_choice)
        data_executives.drop(t.DROP_COL,axis=1,inplace=True)
        financial_data.drop(t.DROP_COL, axis=1, inplace=True)
        news_data.drop(t.DROP_COL, axis=1, inplace=True)
        price_history.drop(t.DROP_COL, axis=1, inplace=True)

        # self.save_df(main_data, 'main_data')
        # self.save_df(data_executives, 'data_executives')
        # self.save_df(financial_data, 'financial_data')
        # self.save_df(news_data, 'news_data')
        # self.save_df(price_history, 'history_data')

        update_insert_db(main_data, data_executives, financial_data, news_data, price_history)

        print(main_data.head())
        print(data_executives.head())
        print(financial_data.head())
        print(news_data.head())

        return

    def get_data(self, table, symbol_choice=None):  # symbol_choice= APPL
        """
        this function gets data from two places:
        1. pulls all the data from the main table in the main page, which contains stocks' general info
        2. pulls data from different subsections for current stock, by calling other implemented functions
        (e.g get_news, get_executive, get_description, get_financial)
        than the function sets data into different DataFrames with symbol as common value

        :param: table: gets table from main page by using implemented "get_table" function
        :optional param: symbol_choice: if wasn't chosen a specific symbol (e.g stock)
        default state - runs over all the existing stocks in the site
        :return: DataFrames containing all collected info for relevant stock (or stocks)
        with stock's name as common value for the DataFrames
        """
        Symbol = []
        Name = []
        Price = []
        Volume = []
        Market_cap = []
        Description = []
        Executives = []
        financial_data_series = []
        News = []

        body = table.find(t.TAG_BODY, attrs={t.TAG_REACTID : '72'})
        ts = datetime.now()
        for tr in body.find_all(t.TAG_TR):

            symbol = tr.find(t.TAG_TD, attrs={t.TAG_ARIALABEL : 'Symbol'}).text
            if (symbol_choice is None) or (symbol in symbol_choice) :  # choosing specific data
                Symbol.append(symbol)
                Name.append(tr.find(t.TAG_TD, attrs={t.TAG_ARIALABEL : 'Name'}).text)
                Price.append(tr.find(t.TAG_TD, attrs={t.TAG_ARIALABEL : 'Price (Intraday)'}).text)
                Volume.append(tr.find(t.TAG_TD, attrs={t.TAG_ARIALABEL : 'Volume'}).text)
                Market_cap.append(tr.find(t.TAG_TD, attrs={t.TAG_ARIALABEL : 'Market Cap'}).text)
                desc = self.get_description(symbol)
                Description.append(desc)
                executives = self.get_executive(symbol)
                Executives.append(executives)
                financial_data_series.append(self.get_financial(symbol))
                News.append(self.get_news(symbol))

        data = self.create_data_frame(Symbol, Name, Price, Volume, Market_cap, Description)
        financial_data = pd.DataFrame(financial_data_series)
        new_data_fin = get_id(financial_data)
        financial_data.insert(loc=0, column='ID', value=new_data_fin)

        executives_series_lst = []
        for list_series in Executives :
            for series in list_series :
                executives_series_lst.append(series)

        news_series_list = []
        for list_series in News :
            for series in list_series :
                news_series_list.append(series)

        data_news = pd.DataFrame(news_series_list)
        data_executive = pd.DataFrame(executives_series_lst)
        price_history = self.get_historical_price(data, ts)

        new_data_executive = get_id(data_executive)
        data_executive.insert(loc=0, column='stock_id', value=new_data_executive)

        new_data_news = get_id(data_news)
        data_news.insert(loc=0, column='stock_id', value=new_data_news)

        new_data_history = get_id(price_history)
        price_history.insert(loc=0, column='stock_id', value=new_data_history)

        return data, data_executive, financial_data, data_news, price_history

    @staticmethod
    def get_news(symbol):
        """
        this function enters the symbol (=stock) page through the link (NEWS_LINK)
        and collects related article links, based on the current symbol
        :param: symbol: current stock name
        :return: a series of lists, when each list contains symbol name, article name (title), link to the article
        if no articles were found - return N\A instead
        """
        news_link = t.NEWS_LINK.format(symbol, symbol)
        attr = 'js-content-viewer Fw(b) Fz(18px) Lh(23px) LineClamp(2,46px) Fz(17px)--sm1024 Lh(19px)--sm1024 ' \
               'LineClamp(2,38px)--sm1024 mega-item-header-link Td(n) C(#0078ff):h C(#000) not-isInStreamVideoEnabled' \
               ' wafer-destroyed'

        series_lst = []
        index = ['Symbol', 'Title', 'Article link']

        driver = webdriver.Chrome(options=options, executable_path=t.DRIVER_PATH)
        driver.get(news_link)
        source = driver.page_source
        time.sleep(5)
        soup = BeautifulSoup(source, t.HTML_PARSER)
        driver.quit()

        try:
            content = soup.find(t.TAG_UL, attrs={t.TAG_CLASS : 'My(0) Ov(h) P(0) Wow(bw)'})
            for tr in content.find_all(t.TAG_LI, attrs={t.TAG_CLASS : 'js-stream-content Pos(r)'}) :
                title = tr.find(t.TAG_A, attrs={t.TAG_CLASS : attr}, href=True).text
                link = tr.find(t.TAG_A, attrs={t.TAG_CLASS : attr}, href=True)[t.TAG_HREF]
                series_lst.append(pd.Series([symbol, title, link], index=index))

            return series_lst

        except:
            print('cannot extract the {} articles'.format(symbol))
            return [pd.Series([symbol, "N/A", "N/A"], index=index)]

    def get_description(self, symbol):
        """
        this function enters the symbol's (=stock) profile page, through the link (PROFILE_LINK)
        and returns description of current stock
        :param: symbol: current stock name
        :return: description of the current stock, if not exist - return 'no description' instead
        """
        try:

            PROFILE_LINK = t.URL_LINK.format(symbol, symbol)
            PAGE = self.get_html(PROFILE_LINK)
            CONTENT = PAGE.find(t.TAG_P, attrs={t.TAG_CLASS : 'Mt(15px) Lh(1.6)'}).text
            return CONTENT
        except:
            print('cannot extract the {} description'.format(symbol))
            return 'no description'

    def get_executive(self, symbol):
        """
        this function enters the symbol (=stock) profile page, through the link (PROFILE_LINK)
        and gets the stock's executives' names, title and salaries.
        :param: symbol: current stock name
        :return: series of lists, when each list contains:
        stock_name (for later DB organizing) executive name, title, salary.
        if no info were found, returns 'N\A' instead
        """
        series_lst = []
        index = ['Symbol', 'Name', 'Title', 'Salary']
        try:
            PROFILE_LINK = t.URL_LINK.format(symbol, symbol)
            PAGE = self.get_html(PROFILE_LINK)
            content = PAGE.find(t.TAG_TABLE, attrs={t.TAG_CLASS : 'W(100%)'})
            body = content.find(t.TAG_BODY)
            for tr in body.find_all(t.TAG_TR,
                                    attrs={t.TAG_CLASS : 'C($primaryColor) BdB Bdc($seperatorColor) H(36px)'}) :
                Name = tr.find(t.TAG_TD, attrs={t.TAG_CLASS : 'Ta(start)'}).text
                Title = tr.find(t.TAG_TD, attrs={t.TAG_CLASS : 'Ta(start) W(45%)'}).text
                Salary = tr.find(t.TAG_TD, attrs={t.TAG_CLASS : 'Ta(end)'}).text
                series_lst.append(pd.Series([symbol, Name, Title, Salary], index=index))

            return series_lst

        except:
            print('cannot extract the {} executives'.format(symbol))
            return [pd.Series([symbol, "N/A", "N/A", "N/A"], index=index)]

    def get_financial(self, symbol):
        """
        this function enters the symbol (=stock) financial section, through the link (FINANCIAL_LINK)
        and gets the stock's financial info.
        :param: symbol: current stock name
        :return: series of lists, when each list contains:
        stock_name (for later DB organizing) and some financial info (yearly revenue, profit, expenses etc).
        """

        total_yearly_revenue = 'no-data'
        total_yearly_Gross_Profit = 'no-data'
        total_yearly_expense = 'no-data'
        total_yearly_Cost_of_Revenue = 'no-data'
        index = ['Symbol', 'TTM revenue', 'TTM Gross Profit', 'TTM expense', 'TTM Cost_of_Revenue']
        attr = 'Ta(c) Py(6px) Bxz(bb) BdB Bdc($seperatorColor) Miw(120px) Miw(140px)--pnclg Bgc($lv1BgColor) fi-row:h_Bgc($hoverBgColor) D(tbc)'

        try:
            link = t.FINANCIAL_LINK.format(symbol, symbol)
            page = self.get_html(link)
            content = page.find(t.TAG_DIV, attrs={t.TAG_CLASS : 'D(tbrg)'})
            tr = content.find_all(t.TAG_DIV, attrs={t.TAG_DATATEST : 'fin-row'})
            total_yearly_revenue = tr[0].find(t.TAG_DIV, attrs={t.TAG_CLASS : attr}).text
            total_yearly_Gross_Profit = tr[2].find(t.TAG_DIV, attrs={t.TAG_CLASS : attr}).text
            total_yearly_expense = tr[11].find(t.TAG_DIV, attrs={t.TAG_CLASS : attr}).text
            total_yearly_Cost_of_Revenue = tr[1].find(t.TAG_DIV, attrs={t.TAG_CLASS : attr}).text

        except:
            print('cannot extract the {} financial info'.format(symbol))

        finally:
            return pd.Series([symbol, total_yearly_revenue, total_yearly_Gross_Profit, total_yearly_expense,
                              total_yearly_Cost_of_Revenue], index=index)

    def get_table(self):
        """
        this function gets the main stocks table from the page, using soup and html id
        """
        table = self.soup.find(t.TAG_TABLE, attrs={t.TAG_REACTID: '42'})
        return table

    @staticmethod
    def create_data_frame(symbol, name, price, volume, market_cap, description):
        """
        this function creates DataFrame by using all the collected general data from the main table per stock (symbol)
        """
        df = pd.DataFrame(list(zip(symbol, name, price, volume, market_cap, description)),
                          columns=['Symbol', 'Name', 'Price', 'Volume', 'Market_cap', 'Description'])
        new_data = get_id(df)

        df.insert(loc=0, column='ID', value=new_data)
        new_col_2 = [1 for i in range(len(df['Symbol']))]
        df.insert(loc=7, column='status', value=new_col_2)
        return df

    @staticmethod
    def save_df(data, name):
        """this function saves the data into a csv file, in case the user commanded to do so"""
        print('saving the csv...\n')
        data.to_csv(t.SAVE_PATH+'{}.csv'.format(name))
        print('succeed\n')

    @staticmethod
    def get_html(URL):
        """this function gets the page content using requests module and page's URL,
        than converts it to be more comfortable to use with BeautifulSoup module"""
        try:
            page = requests.get(URL)
            soup = BeautifulSoup(page.content, t.HTML_PARSER)
            return soup
        except ValueError:
            print('OOPS! ERROR {}'.format(page.status_code))

    @staticmethod
    def get_historical_price(main_data, ts):
        # """
        # this function gets the stock's price and timestamp in each scrape\update of the data from the website,
        # and restores it into a dictionary.
        # the purpose of this function is to show price changes (or non changes) of stocks over time.
        # :param main_data: the main table that scrapes all the info in each scrape\update
        # (scrapes, among others, the 'symbol' and 'Price' - which are relevant for the current function)
        # :param ts: timestamp (date and time) of the current scrape
        # :return: dictionary containing; stock's initials (=symbol), price, timestamp (of the current price scraping)"""

        historical_prices = main_data[['Symbol', 'Price']]
        historical_prices['TimeStamp'] = ts
        return historical_prices
