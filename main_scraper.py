from scraper import Scraper
from api_s import get_data_from_api
import inquirer



def main():
    questions = [
        inquirer.List('user_option',
                      message="in order to proceed please choose an option",
                      choices=["scraper", "immediate data"]
                      )
    ]

    question_scraper = [
        inquirer.Text('symbol',
                      message='if you like to scrape a specific symbol enter the the symbol\nplease please enter "ALL" for all the symbol ',
                      ),
        inquirer.Text('saving flag',
                      message='if you like to save the data locally please add True (default - False) '
                      ),

    ]

    answers = inquirer.prompt(questions)

    if answers.get("user_option") == "scraper" :
        answer_scraper = inquirer.prompt(question_scraper)
        symbol = answer_scraper.get("symbol")
        saving_flag = answer_scraper.get("saving flag")
        scraper = Scraper(save=saving_flag)
        scraper.scrape_all(symbol_choice=symbol)

    elif answers.get("user_option") == "immediate data" :
        get_data_from_api()


if __name__ == '__main__':
    main()
