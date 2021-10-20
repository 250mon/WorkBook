import time

import selenium
from selenium import webdriver
from selenium.webdriver.common.alert import Alert
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from time import sleep
from handle_ids import HandleIds
from threading import Thread
import sys

class NanjiCamping(Thread):
    def __init__(self, url, date, type='camping'):
        Thread.__init__(self)
        self.wait_time = 5
        self.driver = self._get_webdriver()
        self._set_driver()
        self.url = url
        self.date = date
        self.type = type

    def run(self):
        self.macro()

    def _get_webdriver(self):
        options = webdriver.ChromeOptions()
        options.add_argument('headless')
        options.add_argument('window-size=1920,1080')
        driver = webdriver.Chrome(executable_path='chromedriver', options=options)
        return driver

    def _set_driver(self):
        pass
        # implicit waits
        # self.driver.implicitly_wait(self.wait_time)

    def login_from_main(self):
        while True:
            self.driver.get(url='https://yeyak.seoul.go.kr/web/loginForm.do')
            try:
                login_btn = WebDriverWait(self.driver, self.wait_time).until(
                    EC.presence_of_element_located((By.XPATH, '//*[@id="header"]/div[1]/div/div[1]/a'))
                )
                login_btn.click()
                self._login_idpwd()
            except:
                print('Exception login from main')
            else:
                print('Login successful')
                break

    def _login_idpwd(self):
        userid, userpw = HandleIds('ids.txt').get_idpw('Seoul')
        try:
            userid_form = WebDriverWait(self.driver, self.wait_time).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="userid"]'))
            )
            userid_form.send_keys(userid)
            self.driver.find_element(By.XPATH, '//*[@id="userpwd"]').send_keys(userpw)
            self.driver.find_element(By.XPATH, '//*[@id="addUserForm"]/div/button').click()
        except:
            raise Exception

    def initial_screen(self):
        while True:
            self.driver.get(url=self.url)
            try:
                popup = WebDriverWait(self.driver, self.wait_time).until(
                    EC.presence_of_element_located((By.XPATH, '//*[@id="contents"]/div[1]/div/div[2]/button/span'))
                )
                popup.click()
                # explicit waits for reservation btn
                # initial reservation status window
                reserve_btn = WebDriverWait(self.driver, self.wait_time).until(
                    EC.presence_of_element_located((By.XPATH, '//*[@id="aform"]/div[1]/div[2]/div/div/a[1]'))
                )
                reserve_btn.click()
            except:
                print('Initial_screen failed... reload the page')
            else:
                print('Initial_screen successful')
                break

    def macro(self):
        # main screen for login
        self.login_from_main()
        # after login, stand by
        # sys.stdin.read(1)

        while True:
            # initial reservation screen
            self.initial_screen()

            # main reservation screen
            try:
                # select date
                if len(dates := self.driver.find_elements(By.XPATH, f'//*[@id="calendar_2021{self.date}"]')) > 0:
                    dates[0].click()
                else:
                    continue

                if self.type == 'camping':
                    # select number of nights
                    select_num_nite = Select(self.driver.find_element(By.NAME, 'form_cal'))
                    all_nites = select_num_nite.all_selected_options
                    if (avail := len(all_nites)) == 0:
                        print("No availabe dates")
                        continue
                    elif avail == 1:
                        index = 1
                    else:
                        index = 2
                    select_num_nite.select_by_index(index=index)
                elif self.type == 'barbecue11':
                    timezone = self.driver.find_element(By.XPATH, '//*[@id="unit0"]/a')
                    timezone.click()
                else:  #self.type == 'barbecue17':
                    timezone = self.driver.find_element(By.XPATH, '//*[@id="unit1"]/a')
                    timezone.click()

                # For barbecue, select time zone 11~16 or 17~22
                usrchkbox = self.driver.find_element(By.XPATH, '//*[@id="aform"]/div[3]/div[2]/div[5]/h5/span/label/span')
                usrchkbox.click()

                user_cnt = self.driver.find_element(By.XPATH, '//*[@id="user_cnt_area"]/div/div[1]/div/div/div/button[2]')
                user_cnt.send_keys(Keys.ENTER)
                usrchkbox = self.driver.find_element(By.XPATH, '//*[@id="aform"]/div[3]/div[2]/div[5]/h5/span/label/span')
                usrchkbox.click()
                agrchkbox = self.driver.find_element(By.XPATH, '//*[@id="aform"]/div[3]/div[2]/div[6]/h5/span/label/span')
                agrchkbox.click()
                deal_btn = self.driver.find_element(By.XPATH, '//*[@id="aform"]/div[3]/div[3]/div/div[3]/button')
                deal_btn.click()

                # finalize the reservation
                Alert(self.driver).accept()
            except:
                print('Not successful... trying again')
                time.sleep(10)
            else:
                print('Successful!!!')
                break

        if (c := input()) == 'q':
            pass
        self.driver.quit()


if __name__ == '__main__':
    urls = {
        '10_Dtype': 'https://yeyak.seoul.go.kr/web/reservation/selectReservView.do?rsv_svc_id=S210913093907438559',
        '10_barbecue': 'https://yeyak.seoul.go.kr/web/reservation/selectReservView.do?rsv_svc_id=S210913095611524537',
        '11_deck': 'https://yeyak.seoul.go.kr/web/reservation/selectReservView.do?rsv_svc_id=S211014143810532855',
        '11_Dtype': 'https://yeyak.seoul.go.kr/web/reservation/selectReservView.do?rsv_svc_id=S211014144304124526',
        '11_barbecue': 'https://yeyak.seoul.go.kr/web/reservation/selectReservView.do?rsv_svc_id=S211014151656734620',
    }
    NanjiCamping(url=urls['10_Dtype'], date='1023').start()

    # Barbecue
    # NanjiCamping(url=urls['10_barbecue'], date='1024', type='barbecue11').start()

    # Friday
    NanjiCamping(url=urls['11_Dtype'], date='1105').start()
    NanjiCamping(url=urls['11_deck'], date='1105').start()
    # NanjiCamping(url=urls['11_Dtype'], date='1112').start()
    # NanjiCamping(url=urls['11_deck'], date='1112').start()
    # NanjiCamping(url=urls['11_Dtype'], date='1119').start()
    # NanjiCamping(url=urls['11_deck'], date='1119').start()
    # NanjiCamping(url=urls['11_Dtype'], date='1126').start()
    # NanjiCamping(url=urls['11_deck'], date='1126').start()

    # Thursday
    # # NanjiCamping(url=urls['11_deck'], date='1103').start()
    # # NanjiCamping(url=urls['11_deck'], date='1110').start()
    # # NanjiCamping(url=urls['11_deck'], date='1117').start()
    # NanjiCamping(url=urls['11_deck'], date='1124').start()
