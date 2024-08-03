from seleniumbase import BaseCase
from time import sleep

def submit(self, numVersion, url):
    try:
        sleep(2)
        self.type("#url", f"{url}{numVersion}.zip")
        self.click('#fetch-button')
        sleep(5)
        self.click('[data-deselect-all]')
        self.click("//span[text()='.exe']")
        self.click("//*[@for='os:windows10-1703-x64']")
        self.click("//*[@for='os:windows10-2004-x64']")
        self.click("//*[@for='os:windows11-21h2-x64']")
        self.click("//*[@for='timeout-300']")
        self.click("#finish-submit")
        sleep(3)
        return True
    except Exception as e:
        print(e)
        return True
    
class TestSimpleLogin(BaseCase):
    def test_simple_login(self):
        url = "https://github.com/ThanhVan9721/cz/archive/refs/heads/x"
        self.open("https://tria.ge/auth?provider=google&return_to=")
        sleep(2)
        self.type("input#identifierId", "nakeemostwinkle375@gmail.com")
        self.click('//*[contains(text(), "Next")]')
        sleep(5)
        self.type('input#password', "tfNtLjum5q")
        self.click('//*[@id="passwordNext"]/div/button/span')
        try:
            self.click("//button[.//span[text()='Continue']]")
        except:
            print("Đã cấp quyền")
        numVersion = 1
        submitJob = True
        print("Bắt đầu job")
        while submitJob:
            print(f"Lần: {numVersion}")
            self.open("https://tria.ge/submit/file")
            sleep(5)
            submit(self, numVersion, url)
            sleep(2)
            if numVersion == 19:
                numVersion = 0
            numVersion += 1


