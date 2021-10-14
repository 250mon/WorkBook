import selenium
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from time import sleep


options = webdriver.ChromeOptions()
options.add_argument('window-size=1920,1080')
driver = webdriver.Chrome(executable_path='chromedriver', options=options)
# implicit waits
driver.implicitly_wait(5)

URL = 'https://www.google.com/'
driver.get(url=URL)

# explicit waits
# try:
#     element = WebDriverWait(driver, 5).until(
#         EC.presence_of_element_located((By.CLASS_NAME, 'gLFyf'))
#     )
# finally:
#     driver.quit()

# print(driver.current_url)

search_box = driver.find_element_by_xpath('/html/body/div[1]/div[3]/form/div[1]/div[1]/div[1]/div/div[2]/input')
search_box.send_keys('python selenium')
search_box.send_keys(Keys.RETURN)

elements = driver.find_elements_by_xpath('//*[@id="rso"]/div[*]/div')

with open('gorio.txt', 'w+', encoding='utf-8') as f:
    for element in elements:
        print(element.text)
        print(element.text, file=f)

sleep(3)
driver.close()
