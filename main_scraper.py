from project.scraper import Scraper
import argparse


def main():
    parser = argparse.ArgumentParser()

    # parser.add_argument('stock',type=str,nargs='?', help='mention a specific stock',default='ALL')
    parser.add_argument('-s', action='store_true', help='saving the file localy')
    args = parser.parse_args()

    if args.s is True:
        scraper = Scraper(save=True)
        scraper.scrape_all()

    else:
        scraper = Scraper()
        scraper.scrape_all()


if __name__ == '__main__':
    main()
