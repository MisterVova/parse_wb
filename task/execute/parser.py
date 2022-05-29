import re
import traceback
import time

from task import Task

from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.chromium.options import ChromiumOptions
from selenium import webdriver

SLEEP = 2


class TaskExe:

    def __init__(self):
        self.driver = None
        self.options = ChromiumOptions()
        # self.options.headless = True
        self.base_url = ("https://www.wildberries.ru/")

    def exe(self, task) -> Task:
        try:
            self.driver.get(task.url)
            steep = 0
            has_error = 0
            while True:
                time.sleep(SLEEP + SLEEP * 2 * has_error)
                # time.sleep(SLEEP)
                footer = self.driver.find_elements(by=By.ID, value='footer')
                if len(footer) > 0:
                    self.actions.move_to_element(footer[0])
                    self.actions.perform()

                catalog = self.driver.find_elements(by=By.ID, value='catalog')
                if len(catalog) > 0:
                    # print(catalog)

                    product_cards = catalog[0].find_elements(by=By.CLASS_NAME, value='product-card')
                    for card in product_cards:
                        # time.sleep(5)
                        # print("--------------")
                        # print(card.text)

                        try:

                            p = 0
                            s = 0
                            r = 0

                            # # "product-card__action"
                            try:
                                card.find_element(by=By.CLASS_NAME, value='product-card__action')
                                continue
                            except:
                                pass

                            try:
                                stars = card.find_element(by=By.CLASS_NAME, value='product-card__rating')
                                # product-card__rating stars-line star5
                                star = stars.get_attribute("class")
                                star = f"{star}".replace(' ', '')
                                nums = re.findall(r'\d+', star)
                                nums = [float(i) for i in nums]
                                if len(nums) > 0:
                                    s = nums[0]
                            except:
                                pass

                            try:
                                rating = card.find_element(by=By.CLASS_NAME, value='product-card__count')
                                rating_text = rating.text
                                rating_text = f"{rating_text}".replace(' ', '')
                                nums = re.findall(r'\d+', rating_text)
                                nums = [float(i) for i in nums]
                                if len(nums) > 0:
                                    r = nums[0]
                            except:
                                pass

                            try:
                                price = card.find_element(by=By.CLASS_NAME, value='lower-price')
                                price_text = price.text
                                price_text = f"{price_text}".replace(' ', '')
                                nums = re.findall(r'\d+', price_text)
                                nums = [float(i) for i in nums]
                                if len(nums) > 0:
                                    p = nums[0]
                            except:
                                pass
                            prs = {"p": p, "r": r, "s": s}
                            if p:
                                task.add_price(prs)

                        except Exception as e:
                            traceback_str = ''.join(traceback.format_tb(e.__traceback__))
                            print(f"error: '{traceback_str}'")
                            if has_error == 0:
                                self.driver.refresh()
                                has_error += 1
                                continue
                has_error = 0

                pagination_next = self.driver.find_elements(by=By.CLASS_NAME, value='pagination-next')

                if len(pagination_next) > 0:

                    # self.actions = ActionChains(driver, duration=250)
                    # self.actions.move_to_element(pagination_next[0])
                    self.actions.click(pagination_next[0])
                    self.actions.perform()
                    # time.sleep(SLEEP)
                else:
                    break

                if len(task.get_prices()) > 1000:
                    break

                steep += 1
                if steep > 30:
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

        # self.options.headless = True
        self.driver = webdriver.Chrome(options=self.options)
        self.driver.maximize_window()
        self.driver.get(self.base_url)
        # self.driver.implicitly_wait(10)
        # self.driver.implicitly_wait(0)
        self.actions = ActionChains(self.driver, duration=25)
        print("start - webdriver")
        # time.sleep(10)

    def end(self):
        time.sleep(3)
        self.driver.quit()
        print("end - webdriver")


if __name__ == '__main__':
    # pass

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
