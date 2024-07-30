from selenium import webdriver
import time
from pathlib import Path
from pydub import AudioSegment
import speech_recognition as sr
import requests
from selenium.webdriver.common.by import By
import random
import string
import imaplib
import email
from bs4 import BeautifulSoup

def download(url, out_file="audio.mp3"):
    out_file = Path(f"{out_file}").expanduser()
    resp = requests.get(url)
    resp.raise_for_status()
    with open(out_file, "wb") as fout:
        fout.write(resp.content)


def convert():
    audio_file_path = 'audio.mp3' 
    audio = AudioSegment.from_file(audio_file_path)
    audio.export("converted_audio.wav", format="wav")
    r = sr.Recognizer()
    with sr.AudioFile('converted_audio.wav') as source:
        audio_data = r.record(source)
    text = r.recognize_google(audio_data, language='en-US')
    return text

def click_checkbox(driver):
    driver.switch_to.default_content()
    driver.switch_to.frame(driver.find_element(By.XPATH, ".//iframe[@title='reCAPTCHA']"))
    driver.find_element(By.ID, "recaptcha-anchor-label").click()
    driver.switch_to.default_content()

def request_audio_version(driver):
    time.sleep(1)
    driver.switch_to.default_content()
    driver.switch_to.frame(driver.find_element(By.XPATH, ".//iframe[@title='recaptcha challenge expires in two minutes']"))
    driver.find_element(By.ID, "recaptcha-audio-button").click()

def solve_audio_captcha(driver):
    text = driver.find_element(By.ID, "audio-source").get_attribute('src')
    download(text)
    text_input = convert()
    driver.find_element(By.ID, "audio-response").send_keys(text_input)
    driver.find_element(By.ID, "recaptcha-verify-button").click()

def scroll_to_top(driver):
    driver.execute_script("window.scrollTo(0, 0);")

def scroll_to_bottom(driver):
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

def generate_unique_string(base_string, length=5):
    # Tạo danh sách các ký tự không trùng lặp
    characters = string.ascii_letters + string.digits
    random_chars = ''.join(random.sample(characters, length))
    return f"{base_string}+{random_chars}@gmail.com"
    
def input_form_signup(driver, userName):
    try:
        driver.find_element(By.XPATH, "//button[contains(text(), 'Accept')]").click()
    except:
        print("Bỏ qua đồng ý cookie")
    driver.find_element(By.ID, "display-name").send_keys("Laru Beo")
    driver.find_element(By.ID, "email").send_keys(userName)
    driver.find_element(By.ID, "password").send_keys("Buithanhvan1!")
    driver.find_element(By.ID, "confirm_password").send_keys("Buithanhvan1!")
    scroll_to_bottom(driver)
    driver.find_element(By.CSS_SELECTOR, '[for="tos"]').click()

def veri_capcha(driver):
    click_checkbox(driver)
    time.sleep(3)
    try:
        request_audio_version(driver)
        time.sleep(1)
        solve_audio_captcha(driver)
    except Exception as e:
        driver.save_screenshot("/sdcard/download/veri.png")
        print(f"Không cần veri: {e}")

def signup_triage(driver, userName): 
    driver.get("https://tria.ge/signup/individual")
    input_form_signup(driver, userName)
    veri_capcha(driver)
    driver.switch_to.default_content()
    time.sleep(1)
    driver.find_element(By.XPATH, "//button[@type='submit'] | //input[@type='submit']").click()


def login_triage(driver, userName):
    input_form_login(driver, userName)
    veri_capcha(driver)
    driver.switch_to.default_content()
    time.sleep(1)
    driver.find_element(By.XPATH, "//button[@type='submit'] | //input[@type='submit']").click()


def input_form_login(driver, userName):
    driver.find_element(By.ID, "username-input").send_keys(userName)
    driver.find_element(By.CSS_SELECTOR, "[data-next]").click()
    driver.find_element(By.ID, "password-input").send_keys("Buithanhvan1!")
    
def check_mail():
    username = "buithanhvan21011997@gmail.com"
    password = "igvj wpfj nxqe yjot" 
    mail = imaplib.IMAP4_SSL("imap.gmail.com")
    mail.login(username, password)
    mail.select("inbox")
    status, messages = mail.search(None, 'FROM "noreply@hatching.io"')
    email_ids = messages[0].split()
    if email_ids:
        latest_email_id = email_ids[-1]
        status, msg_data = mail.fetch(latest_email_id, "(RFC822)")
        for response_part in msg_data:
            if isinstance(response_part, tuple):
                msg = email.message_from_bytes(response_part[1])
                body = msg.get_payload(decode=True).decode()
                soup = BeautifulSoup(body, "html.parser")
                mail.logout()
                return soup.find('a', href=True)['href']
    else:
        print("Không tìm thấy email từ nguồn này.")
    
def submit(driver, numVersion, url):
    try:
        time.sleep(2)
        driver.switch_to.default_content()
        driver.find_element(By.ID, "url").send_keys(f"{url}{numVersion}.zip")
        driver.find_element(By.ID, "fetch-button").click()
        time.sleep(5)
        driver.switch_to.default_content()
        driver.find_element(By.CSS_SELECTOR, "[data-deselect-all]").click()
        driver.find_element(By.XPATH, "//span[text()='.exe']").click()
        driver.find_element(By.XPATH, "//*[@for='os:windows10-1703-x64']").click()
        driver.find_element(By.XPATH, "//*[@for='os:windows10-2004-x64']").click()
        driver.find_element(By.XPATH, "//*[@for='os:windows11-21h2-x64']").click()
        driver.find_element(By.XPATH, "//*[@for='timeout-300']").click()
        driver.find_element(By.ID, "finish-submit").click()
        return True
    except Exception as e:
        print(e)
        driver.save_screenshot("/sdcard/download/folowjob.png")
        return False


def generate_user_agent():
    """Tạo chuỗi user-agent ngẫu nhiên cho Chrome."""
    # Phiên bản Chrome ngẫu nhiên từ 70 đến 100
    chrome_version = random.randint(70, 100)
    
    # Phiên bản Safari ngẫu nhiên
    safari_version = f"{random.randint(531, 537)}.{random.randint(0, 50)}"
    
    # Phiên bản Chrome Build ngẫu nhiên
    build_version = f"{chrome_version}.0.{random.randint(3000, 4000)}.{random.randint(0, 150)}"
    
    # Hệ điều hành ngẫu nhiên
    os_options = [
        "Windows NT 10.0; Win64; x64",
        "Windows NT 6.1; WOW64",
        "Macintosh; Intel Mac OS X 10_15_7",
        "X11; Linux x86_64"
    ]
    os_choice = random.choice(os_options)
    
    # Tạo chuỗi user-agent hoàn chỉnh
    user_agent = f"Mozilla/5.0 ({os_choice}) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{build_version} Safari/{safari_version}"
    return user_agent

if __name__ == "__main__":
    url = input("Nhập URL: ")
    while True:
        try:
            options = webdriver.ChromeOptions()
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
            options.add_argument("--headless=new")
            user_agent = generate_user_agent()
            options.add_argument(f"--user-agent={user_agent}")
            driver = webdriver.Chrome(options=options)
            userName = generate_unique_string("buithanhvan21011997", length=5)
            print(userName)
            signup_triage(driver, userName)
            mail_veri = check_mail()
            driver.get(mail_veri)
            # Test
            time.sleep(5)
            login_triage(driver, userName)
            time.sleep(5)
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
        except Exception as e:
            print(f"Lỗi: {e}")
            driver.save_screenshot("/sdcard/download/screenshot.png")
            driver.quit()
