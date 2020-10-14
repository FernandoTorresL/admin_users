#Import selenium
from selenium import webdriver
from selenium.webdriver.support.select import Select

# Import config file
from common import config

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

  # Query all the accounts
  # Click on button
  alt_bntConsulta = config()['websites'][website_uid]['labels']['page04']['alt_bntConsulta']
  driver.find_element_by_xpath('//img[@alt="' + alt_bntConsulta + '"]').click()

  password = config()['wbsites']['admin_users']['password']


