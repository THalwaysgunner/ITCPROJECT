from scraper import Scraper
from api import get_data_from_api
from PyInquirer import prompt
from examples import custom_style_2


  questions = [
    {
        'type': 'list',
        'name': 'user_option',
        'message': 'in order to proceed please choose an option ',
        'choices': ["scraper","immediate data"]
    }
]

question_scraper = [
    {
        'type': 'input',
        'name': 'symbol',
        'message': 'if you like to scrape a specific symbol enter the the symbol\n\
         please please enter "ALL" for all the symbol',

    },

    {
        'type' : 'input',
        'name' : 'saving flag',
        'message' : 'if you like to save the data locally please add True (default - False)  \
               ',

    }

]


def main():
    answers = prompt(questions, style=custom_style_2)
    if answers.get("user_option") == "scraper" :
        answer_scraper = prompt(question_scraper, style=custom_style_2)
        symbol = answer_scraper.get("symbol")
        saving_flag = answer_scraper.get("saving flag")
        scraper = Scraper(save=saving_flag)
        scraper.scrape_all(symbol_choice=symbol)

    elif answers.get("user_option") == "immediate data" :
        get_data_from_api()


if __name__ == '__main__':
    main()


