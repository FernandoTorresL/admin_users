import argparse
import logging

# Import config file
from common import config

#Import selenium
from selenium import webdriver
from selenium.webdriver.support.select import Select

# Get a reference to logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_access(host, website_uid, driver):
    # Get the credential data
    user = config()['websites'][website_uid]['user']
    password = config()['websites'][website_uid]['password']

    alt_bntAceptarLogin = config()['websites'][website_uid]['labels']['page01']['alt_bntAceptarLogin']

    # Login
    driver.find_element_by_xpath('//input[@name="usuario"]').send_keys(user)
    driver.find_element_by_xpath('//input[@name="pwd"]').send_keys(password)

    # Click to login... the element is an input without name and an alt tag defined on config.yaml:
    driver.find_element_by_xpath('//input[@alt="' + alt_bntAceptarLogin + '"]').click()

    return True

def navigate_to_data(host, website_uid, driver):

    # Locate the menu option
    text_menuCtrlUsuarios = config()['websites'][website_uid]['labels']['page02']['text_menuCtrlUsuarios']
    driver.find_element_by_xpath('//a[text()="' + text_menuCtrlUsuarios + '"]').click()

    # Now, the next element is a select menu...
    # ...first we get the name of the select menu
    name_selectMenu = config()['websites'][website_uid]['labels']['page03']['name_selectMenu']

    # ... Select the correct option
    test = Select(driver.find_element_by_name(name_selectMenu))
    option_selectMenu = config()['websites'][website_uid]['labels']['page03']['option_selectMenu']
    test.select_by_value(option_selectMenu)

    # Now, we had selected the option on the menu, click on button "Aceptar"
    alt_bntAceptarSelect = config()['websites'][website_uid]['labels']['page03']['alt_bntAceptarSelect']
    driver.find_element_by_xpath('//img[@alt="' + alt_bntAceptarSelect + '"]').click()

    # Query all the accounts and click on button
    alt_bntConsulta = config()['websites'][website_uid]['labels']['page04']['alt_bntConsulta']
    driver.find_element_by_xpath('//img[@alt="' + alt_bntConsulta + '"]').click()

    # password = config()['wbsites']['admin_users']['password']

def _accounts_scraper(website_uid):
    # Get the url of the website (parameter)
    host = config()['websites'][website_uid]['url']
    logging.info('Beginning scraper for {}'.format(host))

    # Setup
    options = webdriver.ChromeOptions()
    options.add_argument('--incognito')
    driver = webdriver.Chrome(executable_path='../../driver/chromedriver', options=options)

    # Get the site (driver)
    driver.get(host)

    # Try login
    login = get_access(host, website_uid, driver)
    if not login:
        logger.warning('Error on login', exc_info=False)
    else:
        logger.info('Successful login!!')
    print('')

    # Navigate to data
    navigate_to_data(host, website_uid, driver)

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
    _accounts_scraper(args.website)
