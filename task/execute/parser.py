import re
import traceback
import time

from task import Task

from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.chromium.options import ChromiumOptions
from selenium import webdriver
from task.settings import URL_WB_MAIN, SLEEP, WEBDRIVER_HEADLESS


class TaskExe:

    def __init__(self):
        self.driver = None
        self.options = ChromiumOptions()

        self.base_url = URL_WB_MAIN

    def exe(self, task) -> Task:
        try:
            self.driver.get(task.url)
            steep = 1
            has_error = 0
            while True:
                time.sleep(SLEEP + SLEEP * 2 * has_error)
                # time.sleep(SLEEP)
                footer = self.driver.find_elements(by=By.ID, value='footer')
                if len(footer) > 0:
                    self.actions.move_to_element(footer[0])
                    self.actions.perform()
                self.parse_V2(has_error, task)
                # catalog = self.driver.find_elements(by=By.ID, value='catalog')
                # if len(catalog) > 0:
                #     # print(catalog)
                #     # print(catalog[0].get_attribute("outerHTML"))
                #     catalog[0].get_attribute("outerHTML")
                #
                #
                #     break
                #     product_cards = catalog[0].find_elements(by=By.CLASS_NAME, value='product-card')
                #     for card in product_cards:
                #         # time.sleep(5)
                #         # print("--------------")
                #         # print(card.text)
                #
                #         try:
                #
                #             p = 0
                #             s = 0
                #             r = 0
                #
                #             # # "product-card__action"
                #             try:
                #                 card.find_element(by=By.CLASS_NAME, value='product-card__action')
                #                 continue
                #             except:
                #                 pass
                #
                #             try:
                #                 stars = card.find_element(by=By.CLASS_NAME, value='product-card__rating')
                #                 # product-card__rating stars-line star5
                #                 star = stars.get_attribute("class")
                #                 star = f"{star}".replace(' ', '')
                #                 nums = re.findall(r'\d+', star)
                #                 nums = [float(i) for i in nums]
                #                 if len(nums) > 0:
                #                     s = nums[0]
                #             except:
                #                 pass
                #
                #             try:
                #                 rating = card.find_element(by=By.CLASS_NAME, value='product-card__count')
                #                 rating_text = rating.text
                #                 rating_text = f"{rating_text}".replace(' ', '')
                #                 nums = re.findall(r'\d+', rating_text)
                #                 nums = [float(i) for i in nums]
                #                 if len(nums) > 0:
                #                     r = nums[0]
                #             except:
                #                 pass
                #
                #             try:
                #                 price = card.find_element(by=By.CLASS_NAME, value='lower-price')
                #                 price_text = price.text
                #                 price_text = f"{price_text}".replace(' ', '')
                #                 nums = re.findall(r'\d+', price_text)
                #                 nums = [float(i) for i in nums]
                #                 if len(nums) > 0:
                #                     p = nums[0]
                #             except:
                #                 pass
                #             prs = {"p": p, "r": r, "s": s}
                #             if p:
                #                 task.add_price(prs)
                #
                #         except Exception as e:
                #             traceback_str = ''.join(traceback.format_tb(e.__traceback__))
                #             print(f"error: '{traceback_str}'")
                #             if has_error == 0:
                #                 self.driver.refresh()
                #                 has_error += 1
                #                 continue

                has_error = 0

                if len(task.get_prices()) > 1000:
                    break

                steep += 1
                if steep > 30:
                    break

                pagination_next = self.driver.find_elements(by=By.CLASS_NAME, value='pagination-next')

                if len(pagination_next) > 0:

                    # self.actions = ActionChains(driver, duration=250)
                    # self.actions.move_to_element(pagination_next[0])
                    # page=2
                    # print(pagination_next[0].)

                    self.driver.get(f"{task.url}&page={steep}")
                    #
                    # self.actions.click(pagination_next[0])
                    # self.actions.perform()
                    # time.sleep(SLEEP)
                else:
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

        self.options.headless = WEBDRIVER_HEADLESS
        # self.options.headless
        # self.driver = webdriver.Chrome(executable_path="chromedriver.exe",options=self.options)
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

    def parse_V1(self, has_error, task):
        catalog = self.driver.find_elements(by=By.ID, value='catalog')
        if len(catalog) > 0:
            # print(catalog)
            # print(catalog[0].get_attribute("outerHTML"))
            # catalog[0].get_attribute("outerHTML")

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

    def parse_V2(self, has_error, task):
        from bs4 import BeautifulSoup
        catalog = self.driver.find_elements(by=By.ID, value='catalog')
        if len(catalog) > 0:
            # print(catalog)
            # print(catalog[0].get_attribute("outerHTML"))
            html = catalog[0].get_attribute("outerHTML")

            soup = BeautifulSoup(html, "html.parser")
            # print(soup)
            # product_cards = catalog[0].find_elements(by=By.CLASS_NAME, value='product-card')
            product_cards = soup.findAll('div', class_='product-card')
            # print(len(product_cards))
            for card in product_cards:
                # time.sleep(1)
                # print("--------------")
                # print(card)

                # continue
                try:

                    p = 0
                    s = 0
                    r = 0

                    # # "product-card__action"
                    try:
                        card__action = card.find('div', class_='product-card__action')
                        # print("card__action", card__action)
                        if card__action:
                            continue
                    except:
                        pass

                    try:
                        stars = card.find('span', class_='product-card__rating')
                        # print("stars", stars.text, stars)
                        # product-card__rating stars-line star5
                        # star = stars.get_attribute("class")
                        star = stars['class']
                        star = f"{star}".replace(' ', '')
                        nums = re.findall(r'\d+', star)
                        nums = [float(i) for i in nums]
                        if len(nums) > 0:
                            s = nums[0]
                    except:
                        pass

                    try:
                        # rating = card.find_element(by=By.CLASS_NAME, value='product-card__count')
                        rating = card.find('span', class_='product-card__count')
                        if rating:
                            # print("rating", rating)
                            # print("rating.text", rating.text)
                            rating_text = rating.text
                            # rating_text = f"{rating_text}".strip().replace(' ', '')
                            rating_text = "".join(re.findall(r'\d+', rating_text))
                            r = float(rating_text)

                    except Exception as e:
                        # print("rating", "err")
                        # traceback_str = ''.join(traceback.format_tb(e.__traceback__))
                        # print(f"error: '{traceback_str}'")
                        pass

                    try:
                        # price = card.find_element(by=By.CLASS_NAME, value='lower-price')
                        price = card.find('ins', class_='lower-price')
                        if not price:
                            price = card.find('span', class_='lower-price')
                        if price:
                            # print("price", price)
                            # print("price.text", price.text)
                            price_text = price.text  # getText()

                            price_text = "".join(re.findall(r'\d+', price_text))
                            p = float(price_text)

                    except Exception as e:
                        # print("price", "err")
                        # traceback_str = ''.join(traceback.format_tb(e.__traceback__))
                        # print(f"error: '{traceback_str}'")
                        pass
                    prs = {"p": p, "r": r, "s": s}
                    # print(prs)
                    if p:
                        task.add_price(prs)

                except Exception as e:
                    traceback_str = ''.join(traceback.format_tb(e.__traceback__))
                    print(f"error: '{traceback_str}'")
                    if has_error == 0:
                        self.driver.refresh()
                        has_error += 1
                        continue
        # time.sleep(1000)

if __name__ == '__main__':
    pass
    #
    # # driver = webdriver.Chrome('/path/to/chromedriver')  # Optional argument, if not specified will search path.
    #
    # driver = webdriver.Chrome()  # Optional argument, if not specified will search path.
    # driver.get('http://www.google.com/')
    # time.sleep(5)  # Let the user actually see something!
    # # search_box = driver.find_element_by_name('q')
    # search_box = driver.find_element(by=By.NAME, value='q')
    # search_box.send_keys('ChromeDriver')
    # search_box.submit()
    # time.sleep(50)  # Let the user actually see something!
    # driver.quit()
