![yahoo-finance-img](https://outwardhound.com/furtropolis/wp-content/uploads/2014/11/yahoo-finance.png)

# Welcome to Yahoo-Finance scraper!

#### This project is a part of [ITC](https://www.itc.tech/) DataScience course

This project scrapes wide range of information about currently most active market stocks.
Detailed Information regarding the stock's data and ERD can be found in the on [stocks_information.md](stocks_information.md) file.

The data is being scraped from https://finance.yahoo.com/most-active website.


## Prerequisites and Installation

in order to run the project, please make sure to follow the [requirements.txt](requirements.txt) file

For easy coordination of your environment, use the package manager [pip](https://pip.pypa.io/en/stable/) to install all the needed packages from [requirements.txt](requirements.txt):

```bash
pip --user install requirements.txt
```

## How to Run the Project?
* make sure your working environment is up to date with all the needed packages and installations.
for more detailed information - check 'Prerequisites and Installation' section.

* run the script from your Command Line Interface by calling [main_scraper.py](https://github.com/THalwaysgunner/ITCPROJECT/blob/master/main_scraper.py):
    ```bash
    >python3 main_scraper.py
    ```
  running it like that - sets up to default state.
  for output variations, please take a look at 'Running Features' section.
    
### Running Features:    
* Stocks information:
    * Default state - scrapes information of all the stocks currently exist in [most-active](https://finance.yahoo.com/most-active) page.  
    * if you are interested in pulling information of a specific stock\s - add stock symbol\s, delimited by spaces (if neccessery)  
    * command examples:
    ```bash
    >python3 main_scraper.py AAPL
    ```
    ```bash
    >python3 main_scraper.py AAPL NID
    ```

* Saving your scraped data
    * Default state - only displays the data on your screen    
    * To save the data - use the optional `-s` flag.
    * command examples:
    ```bash
    >python3 -s main_scraper.py 
    ```  
    ```bash
    >python3 -s main_scraper.py AAPL 
    ```  

## Stocks ERD:    

![name](stocks_info_ERD.png)

*_Detailed explanation of the data can be found on the  attached 'stocks_information.md' file_

## Authors

- Agur Inbal
- Attias Haim

