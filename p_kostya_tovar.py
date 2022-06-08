import re
import traceback
import time

from selenium.webdriver import ActionChains, Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chromium.options import ChromiumOptions
from selenium import webdriver

from task.generator.key import Key
from task.settings import URL_WB_MAIN, SLEEP, WEBDRIVER_HEADLESS
from bs4 import BeautifulSoup
from task.generator.base_task import BaseTask as Task


class TaskExe:

    def __init__(self):
        self.driver = None
        self.options = ChromiumOptions()

        self.base_url = URL_WB_MAIN

    def exe(self, task) -> Task:
        try:
            self.parse_card(task)

        except Exception as e:
            # print(f"error: '{e.__traceback__}'")
            # print(task.url)
            # traceback_str = ''.join(traceback.format_tb(e.__traceback__))
            # traceback_str = ''.join(traceback.format_(e.__traceback__))
            # print(f"error: '{traceback_str}'")
            traceback.print_exc()

        # for i in range(random.randint(10, 20)):
        #     task.add_price(random.randint(100, 200))
        # time.sleep(SLEEP * 1)

        # time.sleep(20)
        return task

    def start(self):

        self.options.headless = WEBDRIVER_HEADLESS
        # self.options.headless
        # self.driver = webdriver.Chrome(executable_path="chromedriver.exe",options=self.options)
        self.driver = webdriver.Chrome(options=self.options)
        # self.driver.set_window_size(700 ,700)
        self.driver.set_window_size(700, 900)
        # self.driver.minimize_window()
        # self.driver.maximize_window()

        self.driver.get(self.base_url)
        # self.driver.implicitly_wait(10)
        # self.driver.implicitly_wait(0)
        self.actions = ActionChains(self.driver, duration=250)
        print("start - webdriver")
        time.sleep(2)

    def end(self):
        time.sleep(3)
        self.driver.quit()
        print("end - webdriver")

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

    # def parse_card(self, task: Task) -> Task:
    #     # print("работает:", task.get_value(Key.key, '123456'))
    #     url = f"https://www.wildberries.ru/catalog/{task.get_value(Key.key, '123456')}/detail.aspx?targetUrl=ST"
    #
    #     self.driver.get(url)
    #     footer = self.driver.find_elements(by=By.ID, value='footer')
    #     if len(footer) > 0:
    #         # print("footer", footer)
    #         self.actions.move_to_element(footer[0])
    #         self.actions.perform()
    #         time.sleep(2)
    #         self.actions.move_to_element(footer[0])
    #         self.actions.perform()
    #
    #     tabs_content = self.driver.find_elements(by=By.ID, value='tabs-content')
    #     btn = tabs_content[0].find_elements(by=By.CLASS_NAME, value='select-radio__btn-text')
    #     if len(btn) > 0:
    #         self.actions = ActionChains(self.driver, duration=250)
    #         self.actions.move_to_element_with_offset(btn[0], 5, 5).perform()
    #         self.actions.scroll(0, 0, 0, 450, duration=5).perform()
    #         self.actions.move_to_element_with_offset(btn[0], -5, -5).perform()
    #         self.actions.click(btn[0]).perform()
    #         select_radio__text = tabs_content[0].find_elements(by=By.CLASS_NAME, value='select-radio__text')
    #         if len(select_radio__text) > 1:
    #             self.actions = ActionChains(self.driver, duration=250)
    #             self.actions.move_to_element_with_offset(select_radio__text[1], 5, 5)
    #             # page=2
    #             # print(pagination_next[0].)
    #
    #             # self.driver.get(f"{task.url}&page={steep}")
    #             #
    #             self.actions.click(select_radio__text[1])
    #             # self.actions.click(select_radio__text[1])
    #             self.actions.perform()
    #             time.sleep(SLEEP)
    #
    #         else:
    #             pass
    #
    #     container = self.driver.find_elements(by=By.ID, value='container')  # переделать
    #     # название,
    #     """ наименование	цена	продано	    Сумма отзывов	Ср рейтинг	начало продаж	дней в продаже	Продавец
    #         name	        price	count_sold	count_review	count_star	sale_start	    sale_days	    seller"""
    #
    #     if len(container) > 0:
    #         html = container[0].get_attribute("outerHTML")
    #         soup = BeautifulSoup(html, "html.parser")
    #         # print(html)
    #         comments = soup.findAll('li', class_='comments__item')
    #         if len(comments)>0:
    #             sale_start = comments[0].find("span",class_='feedback__date').get("content")
    #             # <span class="feedback__date hide-desktop" itemprop="datePublished" content="2020-12-14T07:34:26Z">14 декабря 2020, 10:34</span>
    #             task.set_value("sale_start", sale_start)
    #
    #     # time.sleep(SLEEP*10)
    #     return task

    def confirm_age(self):

        # <button type="button" class="popup__btn-main j-confirm" data-link="{on confirm}" data-jsv="#358^/358^">Да, мне есть 18 лет</button>

        # footer = self.driver.find_elements(by=By.ID, value='footer')
        # popup-confirm-age
        popup_confirm_age = self.driver.find_elements(by=By.CLASS_NAME, value='popup-confirm-age')
        if len(popup_confirm_age) > 1:
            print("18+ есть")
            popup__btn_main = popup_confirm_age[0].find_elements(by=By.CLASS_NAME, value="popup__btn-main")
            if len(popup__btn_main):
                self.actions.move_to_element(popup__btn_main[0]).perform()
                time.sleep(SLEEP * 2)
                self.actions.click().perform()
                time.sleep(SLEEP * 2)
                print("18+k")
        else:
            print("18+ нет")

    def click_date(self, tt) -> bool:
        time.sleep(SLEEP)
        sorting__list = self.driver.find_elements(by=By.CLASS_NAME, value='sorting__list')
        if len(sorting__list) == 0:
            print(f"нажимаем sorting__list")
            return False
        # sorting__item
        # time.sleep(SLEEP)
        sorting__item = self.driver.find_elements(by=By.CLASS_NAME, value='sorting__item')
        if len(sorting__item) == 0:
            print(f"нажимаем sorting__item")
            return False

        a_link = sorting__item[0].find_elements(by=By.TAG_NAME, value="a")
        if len(a_link) == 0:
            print(f"нажимаем a_link")
            return False

        a_date = a_link[0]
        # try:
        self.actions.move_to_element(a_date).perform()
        time.sleep(SLEEP * 2)
        self.actions.click().perform()
        time.sleep(SLEEP * 2)
        # except:
        #     pass

        span = a_date.find_elements(by=By.TAG_NAME, value="span")
        if len(span) == 0:
            print(f"нажимаем span")
            return False

        # sorting__decor sorting__decor--up
        classes = span[0].get_attribute("class")
        print("classes", f"{classes}")
        if not "sorting__decor--up" in f"{classes}":
            print(f"нажимаем classes")
            return False

        print("Все по нажимали")
        return True

    def parse_card(self, task: Task) -> Task:
        # print("работает:", task.get_value(Key.key, '123456'))
        url = f"https://www.wildberries.ru/catalog/{task.get_value(Key.key, '123456')}/detail.aspx?targetUrl=ST"
        self.driver.set_window_size(1200, 900)
        time.sleep(SLEEP)
        self.driver.get(url)
        time.sleep(SLEEP * 2)

        self.confirm_age()
        # print("вторая попытка")
        # self.confirm_age()

        for t in range(0, 2):
            try:
                footer = self.driver.find_elements(by=By.ID, value='footer')
                if len(footer) > 0:
                    # print("footer", footer)
                    self.actions.move_to_element(footer[0])
                    self.actions.perform()

                # time.sleep(SLEEP)
                # footer = self.driver.find_elements(by=By.ID, value='footer')
                # if len(footer) > 0:
                #     self.actions.move_to_element(footer[0])
                # self.actions.perform()

                time.sleep(SLEEP)
                header = self.driver.find_elements(by=By.TAG_NAME, value='header')
                if len(header) > 0:
                    self.actions.move_to_element(header[0]).perform()
                    time.sleep(SLEEP * (t + 0.5) * 0.5)

                # same-part-kt__common-info
                time.sleep(SLEEP)
                comments_reviews_link = self.driver.find_elements(by=By.ID, value='comments_reviews_link')
                if len(comments_reviews_link) > 0:
                    self.actions.move_to_element(comments_reviews_link[0]).perform()
                    time.sleep(SLEEP * (t + 0.5) * 0.5)
                    self.actions.click().perform()
                    # self.actions.perform()
                    time.sleep(SLEEP * (t + 0.5) * 0.5)

                for tt in range(0, 5):
                    if self.click_date(tt):
                        break
                    print(f"нажимаем {tt}")
                    time.sleep(SLEEP * (tt + 0.5) * 0.5)

                # time.sleep(SLEEP * (t + 0.5) * 50)

                break

            except Exception as e:
                # traceback_str = ''.join(traceback.format_tb(e.__traceback__))
                # print(f"error: '{traceback_str}'")
                traceback.print_exc()
                # time.sleep(SLEEP * 50)
                time.sleep(SLEEP * (t + 1) * 10)
                self.driver.set_window_size(1200, 900)
                self.driver.get(url)
                pass
        container = self.driver.find_elements(by=By.ID, value='container')  # переделать
        # название,
        # """ наименование	цена	продано	    Сумма отзывов	Ср рейтинг	начало продаж	дней в продаже	Продавец
        #     name	        price	count_sold	count_review	count_star	sale_start	    sale_days	    seller"""

        if len(container) > 0:
            html = container[0].get_attribute("outerHTML")
            soup = BeautifulSoup(html, "html.parser")
            # print(html)

            try:
                comments = soup.findAll('li', class_='comments__item')
                if len(comments) > 0:
                    sale_start = comments[0].find("span", class_='feedback__date').get("content")
                    # <span class="feedback__date hide-desktop" itemprop="datePublished" content="2020-12-14T07:34:26Z">14 декабря 2020, 10:34</span>
                    task.set_value("sale_start", sale_start)
                    # datetime
                    # print(datetime.strftime())
            except:
                pass

            try:
                #  price
                price = soup.find("span", class_='price-block__final-price').text
                # price = "".join(re.findall(r'\d+', price))
                price = float("".join(re.findall(r'\d+', f"{price}")))
                task.set_value("price", price)
                # print(price)
            except:
                pass

            try:
                #   name
                name_brande = soup.find('h1', class_="same-part-kt__header").get_text()
                # print(name_brande)
                task.set_value("name", name_brande)
                #   seller
            except:
                pass

            try:
                # count_sold
                count_sold = soup.find('p', class_='same-part-kt__order-quantity j-orders-count-wrapper').span.get_text()
                count_sold = "".join(re.findall(r'\d+', count_sold))
                count_sold = float("".join(re.findall(r'\d+', f"{count_sold}")))
                task.set_value("count_sold", count_sold)
                # print(count_sold)
            except:
                pass

            try:
                # Отзывы count_review
                count_review = soup.find('a', id="a-Comments").get_text()
                count_review = "".join(re.findall(r'\d+', count_review))
                count_review = float("".join(re.findall(r'\d+', f"{count_review}")))
                task.set_value("count_review", count_review)
                # print(count_review)

                # count_star \\
                count_star = soup.find('span', class_="same-part-kt__rating")
                count_star = count_star.get("class")
                count_star = float("".join(re.findall(r'\d+', f"{count_star}")))
                task.set_value("count_star", count_star)
                # print(count_star)
            except:
                pass

            try:
                # <div class="seller-details__info">
                seller = soup.find('div', class_="seller-details__info")
                seller = seller.find('a', class_="seller-details__title")
                seller = seller.get("href")
                seller = float("".join(re.findall(r'\d+', f"{seller}")))
                task.set_value("seller", seller)
                # print(seller)
            except:
                pass
        task.set_value("value", url)
        # time.sleep(SLEEP*10)
        return task


if __name__ == '__main__':
    art_list = [
        # "13975629",
        # "36195395",
        # "23361750",
        # "11977345",
        "71739953",
        "19029000",
        "64834786",
        "57906302",
        "27836036",
        "32249824",
        "17272711",
    ]
    # pass

    taskExe = TaskExe()
    taskExe.start()
    for art in art_list:
        obj = {
            Key.key: f"{art}",

        }

        task = Task(obj)
        # print(task.obj)
        taskExe.exe(task)
        print(task.obj)

    taskExe.end()
