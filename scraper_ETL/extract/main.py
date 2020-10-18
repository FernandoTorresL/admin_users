import argparse
import logging
import csv
import datetime
import time

# Import config file
from common import config

#Import selenium
from selenium import webdriver
from selenium.webdriver.support.select import Select

# Get a reference to logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_access(website_uid, driver):
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

def navigate_to_data(website_uid, driver):

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

def _count_pages(website_uid, driver):
    # Count the pages...
    class_td = config()['websites'][website_uid]['labels']['page05']['class_td']
    class_a = config()['websites'][website_uid]['labels']['page05']['class_a']
    pages = driver.find_element_by_xpath('//td[@class="' + class_td + '"]').find_elements_by_xpath('//a[@class="' + class_a + '"]')

    return pages

def _count_rows(website_uid, driver):
    # Count the rows...
    class_table = config()['websites'][website_uid]['labels']['page05']['class_table']
    class_td = config()['websites'][website_uid]['labels']['page05']['class_td']
    total_rows = driver.find_elements_by_xpath('//table[@class="' + class_table + '"]/tbody/tr/td/table/tbody/tr[not(@valign)]/td[contains(@class, "' + class_td + '")]')
    total_rows = int(len(total_rows))

    return total_rows

def _fetch_record(all_rows, field_number):

    record = dict (
        curp        = all_rows[field_number].text,
        matricula   = all_rows[field_number + 1].text,
        nombre      = all_rows[field_number + 2].text,
        cuenta      = all_rows[field_number + 3].text,
        grupo       = all_rows[field_number + 4].text
        )

    return record

def _save_records(website_uid, records):
    now = datetime.datetime.now().strftime('%Y_%m_%d_%H%M')
    out_file_name = '{website_uid}_{datetime}h_records.csv'.format(
        website_uid=website_uid,
        datetime=now)
    #csv_headers = list(filter(lambda property: not property.startswith('_'), dir(records[0])))
    csv_headers = records[0].keys()

    with open(out_file_name, mode='w+', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(csv_headers)

        for record in records:
            row = record.values()
            writer.writerow(row)

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
    login = get_access(website_uid, driver)
    if not login:
        logger.warning('Error on login', exc_info=False)
    else:
        logger.info('Successful login!!')
    print('')

    # Navigate to data
    navigate_to_data(website_uid, driver)

    logging.info('Finding number of pages...')
    pages = _count_pages(website_uid, driver)
    total_pages = int(pages[1].text)
    print('Total pages: ', total_pages)

    # Get the pagination...
    pagination01 = config()['websites'][website_uid]['labels']['page01']['url_pagination01']
    pagination02 = config()['websites'][website_uid]['labels']['page01']['url_pagination02']

    records = []

    # Recorriendo las páginas
    for i in range(1, total_pages + 1):
        logger.info('Start fetching records at page #{}'.format(i))
        time.sleep(1)
        # Count the rows...
        class_table = config()['websites'][website_uid]['labels']['page05']['class_table']
        class_td = config()['websites'][website_uid]['labels']['page05']['class_td']
        all_rows = driver.find_elements_by_xpath('//table[@class="' + class_table + '"]/tbody/tr/td/table/tbody/tr[not(@valign)]/td[contains(@class, "' + class_td + '")]')

        total_fields = int(len(all_rows))
        total_rows = int(total_fields / 5)

        for j in range(0, total_fields, 5):
            record = _fetch_record(all_rows, j)

            if record:
                #logger.info('Record #{} fetched!!'.format(int(j / 5 + 1)))
                records.append(record)
                #print('     ', record['cuenta'])
        print('Total rows: ', total_rows)
        print('')

        pagination = host + pagination01 + str(i - 1) + pagination02 + str(i)

        # Get the next page
        if i != total_pages + 1:
            driver.get(pagination)

    _save_records(website_uid, records)
    driver.close()

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
