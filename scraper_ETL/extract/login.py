#Import selenium
from selenium import webdriver

# Import config file
from common import config

def get_access(host):

  # Setup driver
  options = webdriver.ChromeOptions()
  options.add_argument('--incognito')
  driver = webdriver.Chrome(executable_path='../../driver/chromedriver', options=options)

  # Get the site
  driver.get(host)

  # Get the credential data
  user = config()['websites']['admin_users']['user']
  password = config()['websites']['admin_users']['password']

  alt_bntAceptarLogin = config()['websites']['admin_users']['labels']['page01']['alt_bntAceptarLogin']

  # Login
  driver.find_element_by_xpath('//input[@name="usuario"]').send_keys(user)
  driver.find_element_by_xpath('//input[@name="pwd"]').send_keys(password)

  # Click to login... the element is an input without name and an alt tag defined on config.yaml: 
      # <input type="image" name src="bt_aceptar.gif" alt="Entar al Sistema">
  driver.find_element_by_xpath('//input[@alt="' + alt_bntAceptarLogin + '"]').click()

  # password = config()['wbsites']['admin_users']['password']

