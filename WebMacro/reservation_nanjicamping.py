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


class NanjiCamping(Thread):
    def __init__(self, url, date):
        Thread.__init__(self)
        self.driver = self._get_webdriver()
        self._set_driver()
        self.url = url
        self.date = date

    def run(self):
        self.macro()

    def _get_webdriver(self):
        options = webdriver.ChromeOptions()
        # options.add_argument('headless')
        options.add_argument('window-size=1920,1080')
        driver = webdriver.Chrome(executable_path='chromedriver', options=options)
        return driver

    def _set_driver(self):
        # implicit waits
        self.driver.implicitly_wait(180)

    def login_from_main(self):
        self.driver.get(url='https://yeyak.seoul.go.kr/web/loginForm.do')
        login_btn = self.driver.find_element(By.XPATH, '//*[@id="header"]/div[1]/div/div[1]/a')
        login_btn.click()
        self._login_idpwd()
        self.driver.get(self.url)

    def login_from_reserv(self):
        self.driver.get(self.url)
        # initial popup window
        popup = self.driver.find_element(By.XPATH, '//*[@id="contents"]/div[1]/div/div[2]/button/span')
        popup.click()
        # initial screen
        # reserve_btn = self.driver.find_element(By.XPATH, '//*[@id="aform"]/div[1]/div[2]/div/div/a[1]')
        reserve_btn = self.driver.find_element(By.XPATH, '//*[@id="cal_20211104"]')
        reserve_btn.click()
        # login window
        Alert(self.driver).accept()
        self._login_idpwd()

    def _login_idpwd(self):
        userid, userpw = HandleIds('ids.txt').get_idpw('Seoul')
        self.driver.find_element(By.XPATH, '//*[@id="userid"]').send_keys(userid)
        self.driver.find_element(By.XPATH, '//*[@id="userpwd"]').send_keys(userpw)
        self.driver.find_element(By.XPATH, '//*[@id="addUserForm"]/div/button').click()

    def initial_screen(self):
        while True:
            # popup window
            popup = self.driver.find_element(By.XPATH, '//*[@id="contents"]/div[1]/div/div[2]/button/span')
            popup.click()
            # initail screen
            reserve_btn = self.driver.find_element(By.XPATH, '//*[@id="aform"]/div[1]/div[2]/div/div/a[1]')
            reserve_btn.click()
            # if (cond := EC.presence_of_element_located((By.XPATH, '//*[@id="contents"]/div[1]/div/a[1]'))) is True:
            if len(dates := self.driver.find_elements(By.XPATH, f'//*[@id="calendar_2021{self.date}"]')) > 0:
                dates[0].click()
                break
            else:
                self.driver.get(url=self.url)

            # # explicit waits for reservation btn
            # try:
            #     # initial reservation status window
            #     reserve_btn = WebDriverWait(self.driver, 5).until(
            #         EC.presence_of_element_located((By.XPATH, '//*[@id="aform"]/div[1]/div[2]/div/div/a[1]'))
            #     )
            #     reserve_btn.click()
            # finally:
            #     if EC.presence_of_element_located((By.XPATH, '//*[@id="contents"]/div[1]/div/a[1]')) is False:
            #         break
            #     else:
            #         self.driver.get(url=self.url)


    def macro(self):
        self.login_from_main()
        # self.login_from_reserv()
        self.initial_screen()

        # # popup window
        # popup = self.driver.find_element((By.XPATH, '//*[@id="contents"]/div[1]/div/div[2]/button/span')
        # popup.click()
        # # initial reservation status window
        # reserve_btn = self.driver.find_element((By.XPATH, '//*[@id="aform"]/div[1]/div[2]/div/div/a[1]'))
        # reserve_btn.click()

        # main reservation window
        # date = self.driver.find_element(By.XPATH, '//*[@id="calendar_20211020"]')
        # date.click()

        select_num_nite = Select(self.driver.find_element(By.NAME, 'form_cal'))
        all_nites = select_num_nite.all_selected_options
        if (avail := len(all_nites)) == 0:
            print("No availabe dates")
            exit(0)
        elif avail == 1:
            index = 1
        else:
            index = 2
        select_num_nite.select_by_index(index=index)

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
        sleep(30)

        self.driver.quit()


if __name__ == '__main__':
    urls = {
        '10_Dtype': 'https://yeyak.seoul.go.kr/web/reservation/selectReservView.do?rsv_svc_id=S210913093907438559',
        '11_deck': 'https://yeyak.seoul.go.kr/web/reservation/selectReservView.do?rsv_svc_id=S211014143810532855',
        '11_Dtype': 'https://yeyak.seoul.go.kr/web/reservation/selectReservView.do?rsv_svc_id=S211014144304124526',
        '11_barbecue': 'https://yeyak.seoul.go.kr/web/reservation/selectReservView.do?rsv_svc_id=S211014151656734620',
    }
    # NanjiCamping(url=urls['10_Dtype'], date='1020').start()

    # Friday
    for i in range(1):
        NanjiCamping(url=urls['11_Dtype'], date='1105').start()
        # NanjiCamping(url=urls['11_deck'], date='1105').start()
        # NanjiCamping(url=urls['11_Dtype'], date='1112').start()
        # NanjiCamping(url=urls['11_deck'], date='1112').start()
        # NanjiCamping(url=urls['11_Dtype'], date='1119').start()
        # NanjiCamping(url=urls['11_deck'], date='1119').start()
        # NanjiCamping(url=urls['11_Dtype'], date='1126').start()
        # NanjiCamping(url=urls['11_deck'], date='1126').start()
