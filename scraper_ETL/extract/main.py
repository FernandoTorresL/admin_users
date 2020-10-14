import argparse
import logging

logging.basicConfig(level=logging.INFO)

# Import config file
from common import config

# Import login procedure
from login import get_access

# Get a reference to logging
logger = logging.getLogger(__name__)

def _website_scraper(website_uid):
    # Get the url of the website (parameter)
    host = config()['websites'][website_uid]['url']

    logging.info('Beginning scraper for {}'.format(host))
    get_access(host)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    # Build the list of choices
    websites_choices = list(config()['websites'].keys())
    parser.add_argument('website',
                        help='Argument: The website that you want to scrape',
                        type=str,
                        choices=websites_choices)

    # Parser the arguments
    args = parser.parse_args()
    _website_scraper(args.website)
