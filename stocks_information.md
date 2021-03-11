## ERD and information

![](stocks_info_ERD.png)

### Main Table

**stock_general_info:**
* Contains general data regarding current stock:
    * ID - unique ID per stock, serves as PK 
    * symbol - stock initials, uppercase letters - (also used in case of calling a specific symbol in the CLI) 
    * Name_of_asset - full stock name
    * price - stock's current price 
    * volume - stock's current volume
    * market_cap - stock's current market cap
    * description - stock's profile description
    * activity_status - boolean, can be changed in each update:
        * 1 : currently in the most active stocks' list, 
        * 0 : currently **not** in the most active stocks' list.

### Related Tables

**news:**
* Contains links to recent articles related to the current stock
    * stock_ID - serves as FK for a current stock
    * title - article headline    
    * news_link - link to the article
    
    
**stock_executives:**     
* Contains executives' information for a certain stock 
    * stock_ID - serves as FK for a current stock
    * name_of_ex - executive's full name
    * title - executive's position in the company
    * salary - executive's salary
    
 
**financial_info:**
* Contains financial information for a certain stock 
    * stock_ID - serves as FK for a current stock
    * TTM-revenue - monthly total revenue
    * TTM-gross-profit - monthly gross profit
    * TTM-expense - monthly expenses
    * TTM-cost-of-revenue - monthly cost of revenue
    
**historical_prices**
* Contains stock's price each update run of the scraping 
    * stock_ID - serves as FK for a current stock
    * price - stock's price
    * Date - the timestamp for when the price was scraped
    