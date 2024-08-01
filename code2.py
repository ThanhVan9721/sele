import undetected_chromedriver as uc
from time import sleep
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

def scroll_to_bottom(driver):
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

def submit(driver, numVersion, url):
    try:
        time.sleep(2)
        driver.switch_to.default_content()
        url_elemen = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "url"))
        )
        url_elemen.send_keys(f"{url}{numVersion}.zip")
        driver.find_element(By.ID, "fetch-button").click()
        time.sleep(5)
        driver.switch_to.default_content()
        select = WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "[data-deselect-all]"))
        )
        select.click()
        driver.switch_to.default_content()
        driver.find_element(By.XPATH, "//span[text()='.exe']").click()
        driver.find_element(By.XPATH, "//*[@for='os:windows10-1703-x64']").click()
        driver.find_element(By.XPATH, "//*[@for='os:windows10-2004-x64']").click()
        driver.find_element(By.XPATH, "//*[@for='os:windows11-21h2-x64']").click()
        scroll_to_bottom(driver)
        driver.find_element(By.XPATH, "//*[@for='timeout-300']").click()
        driver.find_element(By.ID, "finish-submit").click()
        return True
    except Exception as e:
        print(e)
        return True

if __name__ == '__main__':
    url = input("Nhập URL: ")
    driver = uc.Chrome(headless=True)
    driver.get('https://tria.ge/auth?provider=google&return_to=')

    # add email
    driver.find_element(By.XPATH, '//*[@id="identifierId"]').send_keys("nakeemostwinkle375@gmail.com")
    driver.find_element(By.XPATH, '//*[@id="identifierNext"]/div/button/span').click()
    sleep(30)
    driver.find_element(By.XPATH, '//*[@id="password"]/div[1]/div/div[1]/input').send_keys("tfNtLjum5q")
    driver.find_element(By.XPATH, '//*[@id="passwordNext"]/div/button/span').click()
    sleep(2)
    try:
        driver.find_element(By.XPATH, "//button[.//span[text()='Continue']]").click()
    except:
        print("Đã cấp quyền")
    numVersion = 1
    submitJob = True
    print("Bắt đầu job")
    while submitJob:
        print(f"Lần: {numVersion}")
        driver.get('https://tria.ge/submit/file')
        time.sleep(5)
        result = submit(driver, numVersion, url)
        time.sleep(2)
        if numVersion == 19:
            numVersion = 0
        if result == False:
            submitJob = False
        numVersion += 1
    sleep(1000)
