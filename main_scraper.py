from project.scraper import Scraper
from project.api import get_data_from_api

import argparse


def main():

    parser = argparse.ArgumentParser(description="get stocks information\n \
    in order to get data / graph or immediate stocks info please ENTER 1 \
    TO scrape data ENTER 2")

    # optional - choose specific stocks to get info from
    parser.add_argument('--option',type=int , help='choosen option')
    args = parser.parse_args()
    option = args.option


    if args.s is True:
        scraper = Scraper(save=True)
        if len(args.stock) > 0 and args.stock != 'ALL':
            scraper.scrape_all(symbol_choice=args.stock)
        else:
            scraper.scrape_all(symbol_choice=None)


    elif option == 2:
        parser.add_argument('--stock', type=str, nargs='*', help=r'mention specific stock\s',
                            default='ALL')
        parser.add_argument('-s', action='store_true', help='saving the file locally')
        args = parser.parse_args()

        if args.s is True:
            scraper = Scraper(save=True)
            if len(args.stock) > 0 and args.stock != 'ALL':
                scraper.scrape_all(symbol_choice=args.stock)
            else :
                scraper.scrape_all(symbol_choice=None)

        else:
            scraper = Scraper()

            if len(args.stock) > 0 and args.stock != 'ALL':
                scraper.scrape_all(symbol_choice=args.stock)
            else:
                scraper.scrape_all(symbol_choice=None)


if __name__ == '__main__':
    main()


