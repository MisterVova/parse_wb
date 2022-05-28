# import chromedriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
import re
from generator import Task
import random
import traceback
from selenium import webdriver
from selenium.webdriver.chromium.options import ChromiumOptions
from selenium.webdriver.common.keys import Keys
import time

from selenium.webdriver.support.ui import Select

# import os
# import datetime
# import sys
# import pytest

SLEEP = 2


class TaskExe:

    def __init__(self):
        self.driver = None
        self.options = ChromiumOptions()
        # self.options.headless = True
        self.base_url = ("https://www.wildberries.ru/")

    def exe(self, task) -> Task:
        try:
            # print(task.url)
            self.driver.get(task.url)
            # self.driver.find_element()
            # catalog = self.driver.find_element(by=By.ID, value='catalog')
            # catalog = self.driver.find_elements(by=By.ID, value='catalog')
            # print(catalog)

            # pagination_next = self.driver.find_elements(by=By.CLASS_NAME, value='pagination-next pagination__next')
            steep = 0
            has_error = 0
            while True:
                time.sleep(SLEEP)
                footer = self.driver.find_elements(by=By.ID, value='footer')
                if len(footer) > 0:
                    self.actions.move_to_element(footer[0])
                    self.actions.perform()
                time.sleep(SLEEP + SLEEP * 2 * has_error)
                #
                # if has_error != 0:
                #     time.sleep(SLEEP * 2)

                catalog = self.driver.find_elements(by=By.ID, value='catalog')
                if len(catalog) > 0:
                    # print(catalog)
                    lower_prices = catalog[0].find_elements(by=By.CLASS_NAME, value='lower-price')
                    # print("lower_price", "len=", len(lower_prices))
                    for price in lower_prices:
                        try:
                            price_text = price.text
                            price_text = f"{price_text}".replace(' ', '')
                            # print(price_text)
                            nums = re.findall(r'\d+', price_text)
                            nums = [float(i) for i in nums]
                            # print(nums)
                            if len(nums) > 0:
                                task.add_price(nums[0])
                            # print(f"{price_text}".replace(' ', ''))
                            # print(int(price_text, base=10))
                        except:
                            print(price)
                            print(task.url)
                            if has_error == 0:
                                self.driver.refresh()
                                has_error += 1
                                continue
                has_error = 0

                pagination_next = self.driver.find_elements(by=By.CLASS_NAME, value='pagination-next')
                # pager_bottoms = self.driver.find_elements(by=By.CLASS_NAME, value='pager-bottom')

                # print(pagination_next)
                if len(pagination_next) > 0:
                    # import  selenium.webdriver.remote.webelement.WebElement
                    # print(pagination_next[0])
                    # print(pagination_next[0].text)
                    # print(pagination_next[0].get_attribute("href"))
                    # print(pagination_next[0].)
                    from selenium.webdriver import ActionChains
                    # self.actions = ActionChains(driver, duration=250)
                    # self.actions.move_to_element(pagination_next[0])
                    self.actions.click(pagination_next[0])
                    self.actions.perform()
                    # time.sleep(SLEEP)
                else:
                    break

                steep += 1
                if steep > 10:
                    break


        except Exception as e:
            # print(f"error: '{e.__traceback__}'")
            print(task.url)
            traceback_str = ''.join(traceback.format_tb(e.__traceback__))
            print(f"error: '{traceback_str}'")

        # for i in range(random.randint(10, 20)):
        #     task.add_price(random.randint(100, 200))
        # time.sleep(SLEEP * 1)
        return task

    def start(self):
        print("start - TaskExe")
        # self.options.headless = True
        self.driver = webdriver.Chrome(options=self.options)
        self.driver.maximize_window()
        self.driver.get(self.base_url)
        self.driver.implicitly_wait(10)
        self.actions = ActionChains(self.driver, duration=250)

        # time.sleep(10)

    def end(self):
        time.sleep(3)
        self.driver.quit()
        print("end - TaskExe OK ")


if __name__ == '__main__':
    # pass
    import time
    from selenium import webdriver

    # driver = webdriver.Chrome('/path/to/chromedriver')  # Optional argument, if not specified will search path.

    driver = webdriver.Chrome()  # Optional argument, if not specified will search path.
    driver.get('http://www.google.com/')
    time.sleep(5)  # Let the user actually see something!
    # search_box = driver.find_element_by_name('q')
    search_box = driver.find_element(by=By.NAME, value='q')
    search_box.send_keys('ChromeDriver')
    search_box.submit()
    time.sleep(50)  # Let the user actually see something!
    driver.quit()
