"""

    Returns:

    """

import argparse
import csv
import datetime
import logging
import time

# import chromedriver_binary
# Import config file
from common import config

# from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.support.select import Select
from webdriver_manager.firefox import GeckoDriverManager

# import chromedriver_autoinstaller


# Import selenium
# from selenium import webdriver
# from selenium.webdriver.chrome.service import Service as ChromeService
# from selenium.webdriver.chrome.service import Service as FirefoxService


# from webdriver_manager.chrome import ChromeDriverManager

# Get a reference to logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def get_access(website_uid, driver):
    """

    Returns:

    """

    # Get the credential data
    base_config = config()["websites"][website_uid]

    user = base_config["user"]
    password = base_config["password"]

    bnt_aceptar = base_config["labels"]["page01"]["bnt_aceptar"]

    # Login
    driver.find_element(
        "xpath",
        "//input[@name='usuario']",
    ).send_keys(user)
    driver.find_element(
        "xpath",
        "//input[@name='pwd']",
    ).send_keys(password)

    # Click to login...the element is an input without name ...
    # ...and an alt tag defined on config.yaml:
    driver.find_element(
        "xpath",
        "//input[@alt='" + bnt_aceptar + "']",
    ).click()

    return True


def navigate_to_data(website_uid, driver):
    """

    Returns:

    """

    # Locate the menu option
    base_config = config()["websites"][website_uid]["labels"]
    menu_ctrl = base_config["page02"]["menu_usuarios"]
    driver.find_element(
        "xpath",
        "//a[text()='" + menu_ctrl + "']",
    ).click()


def navigate_to_data2(website_uid, driver):
    """

    Returns:

    """

    # Now, the next element is a select menu...
    # ...first we get the name of the select menu
    base_config = config()["websites"][website_uid]["labels"]
    name_select_menu = base_config["page03"]["name_select_menu"]

    # ... Select the correct option
    test = Select(driver.find_element("name", name_select_menu))
    option_select_menu = base_config["page03"]["option_select_menu"]
    test.select_by_value(option_select_menu)

    # Now, we had selected the option on the menu, click on button "Aceptar"
    bnt_entra = base_config["page03"]["bnt_entra"]
    driver.find_element(
        "xpath",
        '//img[@alt="' + bnt_entra + '"]',
    ).click()


def navigate_to_data3(website_uid, driver):
    """

    Returns:

    """

    # Query all the accounts and click on button
    base_config = config()["websites"][website_uid]["labels"]
    bnt_cons = base_config["page04"]["bnt_cons"]
    driver.find_element(
        "xpath",
        '//img[@alt="' + bnt_cons + '"]',
    ).click()


def _count_pages(website_uid, driver):
    """

    Returns:

    """

    # Count the pages...
    base_config = config()["websites"][website_uid]["labels"]
    class_td = base_config["page05"]["class_td"]
    class_a = base_config["page05"]["class_a"]
    pages = driver.find_element(
        "xpath",
        "//td[@class='" + class_td + "']",
    ).find_elements(
        "xpath",
        "//a[@class='" + class_a + "']",
    )

    return pages


def _fetch_record(all_rows, field_number):
    """

    Returns:

    """

    record = dict(
        curp=all_rows[field_number].text,
        matricula=all_rows[field_number + 1].text,
        nombre=all_rows[field_number + 2].text,
        cuenta=all_rows[field_number + 3].text,
        grupo=all_rows[field_number + 4].text,
    )

    return record


def _get_record_details(driver, account):
    """_get_record_details _summary_

    _extended_summary_

    Returns:
        _type_: _description_
    """

    # time.sleep(1)

    try:
        input_curp = driver.find_element("name", "curp")
        curp = input_curp.get_attribute("value")

        matricula = driver.find_element(
            "name",
            "matricula",
        ).get_attribute("value")

        area = Select(
            driver.find_element("name", "area"),
        ).first_selected_option.text

        genero = Select(
            driver.find_element("name", "genero"),
        ).first_selected_option.text

        nombre = driver.find_element(
            "name",
            "nombre",
        ).get_attribute("value")

        apellido_pat = driver.find_element(
            "name",
            "apellidoPat",
        ).get_attribute("value")

        apellido_mat = driver.find_element(
            "name",
            "apellidoMat",
        ).get_attribute("value")

        telefono = driver.find_element(
            "name",
            "telefono",
        ).get_attribute("value")

        email = driver.find_element(
            "name",
            "email",
        ).get_attribute("value")

        grupo = Select(
            driver.find_element(
                "name",
                "idGrupo",
            )
        ).first_selected_option.text

        usrnametxt = driver.find_element(
            "name",
            "usrnametxt",
        ).get_attribute("value")

        detalle_cuenta = dict(
            curp=curp,
            matricula=matricula,
            area=area,
            genero=genero,
            nombre=nombre,
            apellido_p=apellido_pat,
            apellido_m=apellido_mat,
            telefono=telefono,
            email=email,
            grupo=grupo,
            usuario=usrnametxt,
        )
    except NoSuchElementException:
        detalle_cuenta = dict(
            curp="null",
            matricula="null",
            area="null",
            genero="null",
            nombre="null",
            apellido_p="null",
            apellido_m="null",
            telefono="null",
            email="null",
            grupo="null",
            usuario=account,
        )
        print("Account not found.")
        return detalle_cuenta

    return detalle_cuenta


def _save_cuentas_details(website_uid, detalle_cuentas):
    now = datetime.datetime.now().strftime("%Y_%m_%d_%H%M")

    out_file_name = f"./csv/{website_uid}_{now}h_detalle_cuentas.csv"

    out_file_name = out_file_name.format(
        website_uid=website_uid,
        datetime=now,
    )

    csv_headers = detalle_cuentas[0].keys()

    with open(out_file_name, mode="w+", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(csv_headers)

        for detalle_cuenta in detalle_cuentas:
            row = detalle_cuenta.values()
            writer.writerow(row)


def _save_records(website_uid, records):
    now = datetime.datetime.now().strftime("%Y_%m_%d_%H%M")

    out_file_name = f"./csv/{website_uid}_{now}h_records.csv"

    csv_headers = records[0].keys()

    with open(out_file_name, mode="w+", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(csv_headers)

        for record in records:
            row = record.values()
            writer.writerow(row)


def _accounts_scraper(website_uid):
    # Get the url of the website (parameter)
    host = config()["websites"][website_uid]["url"]

    logging.info("Beginning scraper for %s", host)

    # Testing with older version of Chrome
    # Check if the current version of chromedriver exists
    # chromedriver_autoinstaller.install()
    # and if it doesn't exist, download it automatically,
    # then add chromedriver to path

    # driver = webdriver.Chrome()
    # driver.get("http://www.python.org")
    # assert "Python" in driver.title
    # END of Testing with older version of Chrome

    # Setup
    # Con Windows
    # cls.driver =
    # webdriver.Chrome(executable_path = r'C://selenium/chromedriver.exe')

    # Con MacOs
    # driver = webdriver.Chrome(
    #    executable_path='../../../../chromedriver/mac64_m1/v105/chromedriver')
    # driver = webdriver.Chrome(executable_path='/usr/bin/brave-browser')

    # With driver download automaticaly
    # driver = webdriver.Chrome(service=ChromeService(
    #    ChromeDriverManager().install()))

    # Test #2
    # With driver download automaticaly
    # driver = webdriver.Chrome(service=ChromeService())
    # driver = webdriver.Firefox(service=ChromeService())

    # from selenium import webdriver
    # from selenium.webdriver.firefox.service import Service as FirefoxService
    # from webdriver_manager.firefox import GeckoDriverManager

    driver = webdriver.Firefox(
        service=FirefoxService(
            GeckoDriverManager().install(),
        ),
    )

    # Get the site (driver)
    driver.get(host)

    # Try login
    login = get_access(website_uid, driver)
    if not login:
        logger.warning("Error on login", exc_info=False)
    else:
        logger.info("Successful login!!")
    print("")

    # Navigate to data
    navigate_to_data(website_uid, driver)

    # Navigate to data part 2
    navigate_to_data2(website_uid, driver)

    # Navigate to data part 3
    navigate_to_data3(website_uid, driver)

    logging.info("Finding number of pages...")
    pages = _count_pages(website_uid, driver)
    total_pages = int(pages[1].text)
    print("Total pages: ", total_pages)

    # Get the pagination...
    base_config = config()["websites"][website_uid]["labels"]
    pagination01 = base_config["page01"]["url_pagination01"]
    pagination02 = base_config["page01"]["url_pagination02"]

    records = []
    cuentas = []
    lista_cuentas = []

    # Recorriendo las páginas
    for i in range(1, total_pages + 1):
        # for i in range(1, 2):
        logger.info("Start fetching records at page #%s", i)
        # time.sleep(1)
        # Count the rows...
        class_table = base_config["page05"]["class_table"]
        class_td = base_config["page05"]["class_td"]
        all_rows = driver.find_elements(
            "xpath",
            "//table[@class='"
            + class_table
            + "']/tbody/tr/td/table/tbody/"
            + "tr[not(@valign)]/td[contains(@class, '"
            + class_td
            + "')]",
        )

        total_fields = int(len(all_rows))
        total_rows = int(total_fields / 5)

        for j in range(0, total_fields, 5):
            record = _fetch_record(all_rows, j)

            if record:
                # logger.info('Record #{} fetched!!'.format(int(j / 5 + 1)))
                records.append(record)
                cuentas.append(record["cuenta"])
                # print("     ", record["cuenta"])
                lista_cuentas.append(record["cuenta"])
        print("Total rows: ", total_rows)
        print("")

        pagination = host + pagination01 + str(i - 1) + pagination02 + str(i)

        # Get the next page
        if i != total_pages + 1:
            driver.get(pagination)

    # Save account's list (without details)
    _save_records(website_uid, records)

    # Get details
    detalle_cuentas = _get_accounts_details(website_uid, driver, lista_cuentas)

    # Save details to file
    _save_cuentas_details(website_uid, detalle_cuentas)

    driver.close()


def _get_accounts_details(website_uid, driver, lista_cuentas):
    detalle_cuentas = []
    i = 0

    for account in lista_cuentas:
        i += 1

        print(f"Registro {account}, #{i} de {len(lista_cuentas)}")

        # Search an specific account:
        host = config()["websites"][website_uid]["url"]
        url_detail = config()["websites"][website_uid]["url_detail"]

        driver.get(host + url_detail + account)

        # driver.find_element("name", "id_login").send_keys(account)

        # navigate_to_data3(website_uid, driver)

        detalle_cuenta = _get_record_details(driver, account)

        detalle_cuentas.append(detalle_cuenta)

        # host = config()["websites"][website_uid]["url"]
        # url_consulta = config()["websites"][website_uid]["url_consulta"]

        # driver.get(host + url_consulta)

    return detalle_cuentas


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    # Build the list of choices
    websites_choices = list(config()["websites"].keys())
    parser.add_argument(
        "website",
        help="Argument: The website that you want to scrape",
        type=str,
        choices=websites_choices,
    )

    # Parser the arguments
    args = parser.parse_args()

    _accounts_scraper(args.website)
