import undetected_chromedriver as uc
from selenium import webdriver

options = webdriver.ChromeOptions() 
options.add_argument("start-maximized")
driver = uc.Chrome(options=options)
driver.get('https://bet365.com')
