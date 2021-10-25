from datetime import datetime, time
import time
from time import sleep
import selenium
from selenium import webdriver
from selenium.webdriver.common.alert import Alert
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from handle_ids import HandleIds
from threading import Thread


def wait_start(runTime, action):
    startTime = time(*(map(int, runTime.split(':'))))
    # you can add here any additional variable to break loop if necessary
    while startTime > datetime.today().time():
        # you can change 1 sec interval to any other
        sleep(1)
    action()

class WebLogin(Thread):
    def __init__(self, url):
        Thread.__init__(self)
        self.wait_time = 5
        self.driver = self._get_webdriver()
        self._set_driver()
        self.url = url

    def run(self):
        self.macro()

    def _get_webdriver(self):
        options = webdriver.ChromeOptions()
        # options.add_argument('headless')
        options.add_argument('window-size=1920,1080')
        driver = webdriver.Chrome(executable_path='chromedriver', options=options)
        return driver

    def _set_driver(self):
        pass
        # implicit waits
        # self.driver.implicitly_wait(self.wait_time)

    def _wait_until_find_element(self, by, value):
        elem = WebDriverWait(self.driver, self.wait_time).until(
            EC.presence_of_element_located((by, value))
        )
        return elem

    def login_page(self):
        while True:
            self.driver.get(url=self.url)
            try:
                # login_btn = self._wait_until_find_element(By.XPATH, '//*[@id="container"]/div/ul/li[1]/a')
                # login_btn.click()
                self._login_idpwd()
            except:
                print('Exception login from main')
            else:
                print('Login successful')
                break

    def _login_idpwd(self):
        userid, userpw = HandleIds('ids.txt').get_idpw('IMedu')
        try:
            userid_form = self._wait_until_find_element(By.XPATH, '//*[@id="user_id"]')
            userid_form.send_keys(userid)
            self.driver.find_element(By.XPATH, '//*[@id="user_pass"]').send_keys(userpw)
            self.driver.find_element(By.XPATH, '//*[@id="container"]/div/div/div/div[2]/a').click()
            sleep(5)
        except:
            raise Exception

    def macro(self):
        # main screen for login
        self.login_page()

        # accept alert
        # sleep(1)
        Alert(self.driver).accept()
        sleep(2)

        while True:
            body = self._wait_until_find_element(By.CSS_SELECTOR, 'body')
            body.send_keys(Keys.PAGE_DOWN)
            body.send_keys(Keys.PAGE_DOWN)
            print('Page_down sent')

            try:
                btn_try = self._wait_until_find_element(By.XPATH, '//*[@id="schedule_btn_area_5"]/a[1]/em')
                print('found btn_try')
                btn_try.click()
                print('btn_try clicked')

                # btn1 = self.driver.find_element((By.XPATH, '//*[@id="schedule_btn_area_4"]/a[3]/em'))
                # wait_start('17:05', btn1.click)

                # sleep(1)
                # btn2 = self.driver.find_element(By.XPATH, '//*[@id="schedule_btn_area_5"]/a[2]/em')
                # btn2.click()
                #
                # sleep(1)
                # btn3 = self.driver.find_element(By.XPATH, '//*[@id="schedule_btn_area_5"]/a[3]/em')
                # wait_start('18:20', btn3.click)
                #
                # sleep(1)
                # btn4 = self.driver.find_element(By.XPATH, '//*[@id="header"]/div[1]/div[2]/a')
                # btn4.click()

            except:
                print('Not successful... trying again')
                sleep(10)
            else:
                print('Successful!!!')
                sleep(30)
                break

        # if (c := input()) == 'q':
        #     pass
        self.driver.quit()


if __name__ == '__main__':
    urls = {
        'site1': 'http://www.onsemina.com/_web/main/intro.php?kmc=2021yonginseverance',
    }
    WebLogin(url=urls['site1']).start()

    # test for wait_start
    # def act(x):
    #     print(x+10)
    # wait_start('15:46', lambda: act(100))
