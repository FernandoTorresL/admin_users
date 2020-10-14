#Import selenium
from selenium import webdriver

# Import config file
from common import config

def navigate_to_data(host, website_uid, driver):

  # Locate the menu option
  text_menuCtrlUsuarios = config()['websites'][website_uid]['labels']['page02']['text_menuCtrlUsuarios']

  driver.find_element_by_xpath('//a[text()="' + text_menuCtrlUsuarios + '"]').click()

  password = config()['wbsites']['admin_users']['password']


