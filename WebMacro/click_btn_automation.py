import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

from selenium.webdriver.common.alert import Alert
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from time import sleep


class AutoClicking():
    def __init__(self):
        self.wait_time = 2
        self.driver = self._get_webdriver()

    def _get_webdriver(self):
        options = Options()
        options.add_experimental_option("detach", True)

        service = Service(executable_path='C:\\tools\\chromedriver-win64\\chromedriver.exe')
        # service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
        return driver

    def open_url(self):
        self.driver.get(url="https://www.neuralnine.com")
        self.driver.maximize_window()

    def click_btn(self):
        try:
            btn = WebDriverWait(self.driver, self.wait_time).until(
                EC.presence_of_element_located((By.XPATH,
                                                # '//*[@id="root"]/div/header/div[1]/div[2]/div[1]/button/div/p'))
                                                '//*[@id="masthead"]/div/section/div/div[4]/div/div/div/div/a/span/span'))
            )
            btn.click()
        except Exception as e:
            print(f'Exception{e} during clicking btn')
        else:
            print('Waiting ...')
            sleep(2)
            print('Ends.')

    def print_elements(self, elements):
        for elem in elements:
            print(elem.get_attribute("innerHTML"))

    def click_btn2(self):
        # finds s link which includes "Books"
        links = self.driver.find_elements("xpath", "//a[@href]")
        for link in links:
            if "Books" in link.get_attribute("innerHTML"):
                link.click()
                break

        # finds the book link
        book_links = self.driver.find_elements("xpath",
                                               "//div[contains(@class, 'elementor-column-wrap')][.//h2[text()[contains(., '7 IN 1')]]][count(.//a)=2]//a")
        self.print_elements(book_links)

        # opens a tab containing amazon by clicking the link
        book_links[0].click()

        # switch to another tab
        self.driver.switch_to.window(self.driver.window_handles[1])

        time.sleep(3)
        buttons = self.driver.find_elements("xpath", "//a[.//span[text()[contains(., 'Paperback')]]]//span[text()[contains(., '$')]]")
        for button in buttons:
            print(button.get_attribute("innerHTML"))


if __name__ == '__main__':
    autoclicking = AutoClicking()
    autoclicking.open_url()
    autoclicking.click_btn2()
