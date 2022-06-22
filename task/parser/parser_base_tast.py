import re
import traceback
import time
from datetime import datetime
# from tasks import Task

from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.chromium.options import ChromiumOptions
from selenium import webdriver

from task.generator.base_task import BaseTask as Task
from task.generator.key import SheetNames, Key
from task.settings import URL_WB_MAIN, SLEEP, WEBDRIVER_HEADLESS, URL_WB_SEARCH
from bs4 import BeautifulSoup


class TaskExe:

    def __init__(self):
        self.driver = None
        self.options = ChromiumOptions()

        self.base_url = URL_WB_MAIN

    def exe(self, task: Task) -> Task:
        try:
            sheet_name = task.get_sheet_name()
            if sheet_name == SheetNames.НеОпределён:
                return self.exe_old(task)
            elif sheet_name == SheetNames.Задачи:
                self.parse_task(task)
            elif sheet_name == SheetNames.Карточки:
                self.parse_card(task)
            elif sheet_name == SheetNames.Предметы:
                self.parse_search(task)
            elif sheet_name == SheetNames.Продавцы:
                self.parse_seller(task)

        except Exception as e:
            # print(f"error: '{e.__traceback__}'")
            # print(tasks.url)
            traceback_str = ''.join(traceback.format_tb(e.__traceback__))
            print("\n", ">" * 150)
            print(f"error: '{traceback_str}'")
            print("\n", "<" * 150)
        # for i in range(random.randint(10, 20)):
        #     tasks.add_price(random.randint(100, 200))
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

    def exe_old(self, task) -> Task:
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
        #     tasks.add_price(random.randint(100, 200))
        # time.sleep(SLEEP * 1)
        return task

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

    def parse_task(self, task: Task):
        time.sleep(6 * 60)
        return task

    def parse_seller(self, task: Task):
        time.sleep(1 * 60)
        return task

    def parse_search(self, task: Task):
        values = []
        goods_count = 0
        self.driver.set_window_size(1200, 900)
        try:
            url = f"{URL_WB_SEARCH}{task.get_value(Key.key, '')}"
            self.driver.get(url)

            steep = 1
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
                    html = catalog[0].get_attribute("outerHTML")
                    soup = BeautifulSoup(html, "html.parser")
                    product_cards = soup.findAll('div', class_='product-card')

                    for card in product_cards:
                        article = card.get("data-popup-nm-id")
                        if article:
                            values.append(article)

                    goods_count = soup.find("span", class_="goods-count")
                    # print(goods_count)
                    # print(goods_count.get_text())
                    goods_count = float("".join(re.findall(r'\d+', f"{goods_count}")))
                    # print(goods_count)
                    # time.sleep(10)

                has_error = 0
                if len(values) > 100:
                    break
                steep += 1
                if steep > 30:
                    break
                pagination_next = self.driver.find_elements(by=By.CLASS_NAME, value='pagination-next')
                if len(pagination_next) > 0:
                    url = f"{URL_WB_SEARCH}{task.get_value(Key.key, '')}&page={steep}"
                    self.driver.get(url)
                else:
                    break


        except Exception as e:

            traceback_str = ''.join(traceback.format_tb(e.__traceback__))
            print(f"error: '{traceback_str}'")

        task.set_value(key=Key.goods_count, value=goods_count)

        task.set_value(key=Key.value, value=values)
        return task

    # def parse_card(self, tasks: Task) -> Task:
    #     # print("работает:", tasks.get_value(Key.key, '123456'))
    #     url = f"https://www.wildberries.ru/catalog/{tasks.get_value(Key.key, '123456')}/detail.aspx?targetUrl=ST"
    #     self.driver.set_window_size(700, 900)
    #     self.driver.get('chrome://settings/')
    #     self.driver.execute_script('chrome.settingsPrivate.setDefaultZoom(1.5);')
    #     self.driver.get("https://www.google.co.uk/")
    #     self.driver.get(url)
    #     time.sleep(SLEEP)
    #     for t in range(0, 2):
    #         try:
    #             footer = self.driver.find_elements(by=By.ID, value='footer')
    #             if len(footer) > 0:
    #                 # print("footer", footer)
    #                 self.actions.move_to_element(footer[0])
    #                 self.actions.perform()
    #                 time.sleep(SLEEP)
    #                 self.actions.move_to_element(footer[0])
    #                 self.actions.perform()
    #
    #                 "product-detail__user-activity user-activity"
    #             header = self.driver.find_elements(by=By.TAG_NAME, value='header')
    #             if len(header) > 0:
    #                 self.actions.move_to_element(header[0])
    #                 self.actions.perform()
    #                 time.sleep(SLEEP * (t + 0.5) * 0.5)
    #
    #             user_activity = self.driver.find_elements(by=By.CLASS_NAME, value='product-detail__user-activity')
    #             if len(user_activity) > 0:
    #                 self.actions.move_to_element(user_activity[0])
    #                 self.actions.perform()
    #                 time.sleep(SLEEP * (t + 0.5) * 0.5)
    #             # "#container > section.product-detail__user-activity.user-activity"
    #
    #             time.sleep(SLEEP * t)
    #             tabs_content = self.driver.find_elements(by=By.ID, value='tabs-content')
    #             if len(tabs_content) > 0:
    #                 btn = tabs_content[0].find_elements(by=By.CLASS_NAME, value='select-radio__btn-text')
    #                 if len(btn) > 0:
    #                     # self.actions = ActionChains(self.driver, duration=250)
    #                     self.actions.move_to_element_with_offset(btn[0], 5, 5).perform()
    #                     self.actions.scroll(0, 0, 0, 450, duration=5).perform()
    #                     time.sleep(SLEEP * (t + 1) * 0.5)
    #                     self.actions.move_to_element(btn[0]).perform()
    #                     self.actions.click(btn[0]).perform()
    #                     time.sleep(SLEEP * (t + 1) * 0.5)
    #                     # select_radio__text = btn[0].find_elements(by=By.CLASS_NAME, value='select-radio__text')
    #                     #  select_radio__text = tabs_content[0].find_elements(by=By.CLASS_NAME, value='select-radio__text')
    #                     select_radio__text = btn[0].find_elements(by=By.CLASS_NAME, value='select-radio__item')
    #                     if len(select_radio__text) > 1:
    #                         # self.actions = ActionChains(self.driver, duration=20)
    #                         time.sleep(SLEEP * (t + 1) * 0.5)
    #                         self.actions.move_to_element_with_offset(select_radio__text[1], 5, 5)
    #                         self.actions.click(select_radio__text[1])
    #                         self.actions.perform()
    #                         time.sleep(SLEEP * (t + 1) * 0.5)
    #                     else:
    #                         pass
    #             break
    #
    #         except Exception as e:
    #             # traceback_str = ''.join(traceback.format_tb(e.__traceback__))
    #             # print(f"error: '{traceback_str}'")
    #             traceback.print_exc()
    #             # time.sleep(SLEEP * 50)
    #             time.sleep(SLEEP * (t + 1))
    #             self.driver.set_window_size(700, 900)
    #             self.driver.get(url)
    #             pass
    #     container = self.driver.find_elements(by=By.ID, value='container')  # переделать
    #     # название,
    #     # """ наименование	цена	продано	    Сумма отзывов	Ср рейтинг	начало продаж	дней в продаже	Продавец
    #     #     name	        price	count_sold	count_review	count_star	sale_start	    sale_days	    seller"""
    #
    #     if len(container) > 0:
    #         html = container[0].get_attribute("outerHTML")
    #         soup = BeautifulSoup(html, "html.parser")
    #         # print(html)
    #
    #         try:
    #             comments = soup.findAll('li', class_='comments__item')
    #             if len(comments) > 0:
    #                 sale_start = comments[0].find("span", class_='feedback__date').get("content")
    #                 # <span class="feedback__date hide-desktop" itemprop="datePublished" content="2020-12-14T07:34:26Z">14 декабря 2020, 10:34</span>
    #                 tasks.set_value("sale_start", sale_start)
    #                 # datetime
    #                 # print(datetime.strftime())
    #         except:
    #             pass
    #
    #         try:
    #             #  price
    #             price = soup.find("span", class_='price-block__final-price').text
    #             # price = "".join(re.findall(r'\d+', price))
    #             price = float("".join(re.findall(r'\d+', f"{price}")))
    #             tasks.set_value("price", price)
    #             # print(price)
    #         except:
    #             pass
    #
    #         try:
    #             #   name
    #             name_brande = soup.find('h1', class_="same-part-kt__header").get_text()
    #             # print(name_brande)
    #             tasks.set_value("name", name_brande)
    #             #   seller
    #         except:
    #             pass
    #
    #         try:
    #             # count_sold
    #             count_sold = soup.find('p', class_='same-part-kt__order-quantity j-orders-count-wrapper').span.get_text()
    #             count_sold = "".join(re.findall(r'\d+', count_sold))
    #             count_sold = float("".join(re.findall(r'\d+', f"{count_sold}")))
    #             tasks.set_value("count_sold", count_sold)
    #             # print(count_sold)
    #         except:
    #             pass
    #
    #         try:
    #             # Отзывы count_review
    #             count_review = soup.find('a', id="a-Comments").get_text()
    #             count_review = "".join(re.findall(r'\d+', count_review))
    #             count_review = float("".join(re.findall(r'\d+', f"{count_review}")))
    #             tasks.set_value("count_review", count_review)
    #             # print(count_review)
    #
    #             # count_star \\
    #             count_star = soup.find('span', class_="same-part-kt__rating")
    #             count_star = count_star.get("class")
    #             count_star = float("".join(re.findall(r'\d+', f"{count_star}")))
    #             tasks.set_value("count_star", count_star)
    #             # print(count_star)
    #         except:
    #             pass
    #
    #         try:
    #             # <div class="seller-details__info">
    #             seller = soup.find('div', class_="seller-details__info")
    #             seller = seller.find('a', class_="seller-details__title")
    #             seller = seller.get("href")
    #             seller = float("".join(re.findall(r'\d+', f"{seller}")))
    #             tasks.set_value("seller", seller)
    #             # print(seller)
    #         except:
    #             pass
    #     tasks.set_value("value", url)
    #     # time.sleep(SLEEP*10)
    #     return tasks

    def confirm_age(self):

        # <button type="button" class="popup__btn-main j-confirm" data-link="{on confirm}" data-jsv="#358^/358^">Да, мне есть 18 лет</button>

        # footer = self.driver.find_elements(by=By.ID, value='footer')
        # popup-confirm-age
        popup_confirm_age = self.driver.find_elements(by=By.CLASS_NAME, value='popup-confirm-age')
        if len(popup_confirm_age) > 1:
            # print("18+ есть")
            popup__btn_main = popup_confirm_age[0].find_elements(by=By.CLASS_NAME, value="popup__btn-main")
            if len(popup__btn_main):
                self.actions.move_to_element(popup__btn_main[0]).perform()
                time.sleep(SLEEP * 2)
                self.actions.click().perform()
                time.sleep(SLEEP * 2)
                print("18+да")
        else:
            pass
            # print("18+ нет")

    def click_date(self, tt) -> bool:
        time.sleep(SLEEP)
        sorting__list = self.driver.find_elements(by=By.CLASS_NAME, value='sorting__list')
        if len(sorting__list) == 0:
            print(f"click_date sorting__list")
            return False
        # sorting__item
        # time.sleep(SLEEP)
        sorting__item = self.driver.find_elements(by=By.CLASS_NAME, value='sorting__item')
        if len(sorting__item) == 0:
            print(f"click_date sorting__item")
            return False

        a_link = sorting__item[0].find_elements(by=By.TAG_NAME, value="a")
        if len(a_link) == 0:
            print(f"click_date a_link")
            return False

        a_date = a_link[0]
        # try:
        self.actions.move_to_element(a_date).perform()
        time.sleep(SLEEP * (tt + 1))
        self.actions.click().perform()
        time.sleep(SLEEP * (tt + 1))
        # except:
        #     pass

        span = a_date.find_elements(by=By.TAG_NAME, value="span")
        if len(span) == 0:
            print(f"нажимаем span")
            return False

        # sorting__decor sorting__decor--up
        classes = span[0].get_attribute("class")
        # print("classes", f"{classes}")
        if not "sorting__decor--up" in f"{classes}":
            print(f"нажимаем classes")
            return False

        # print("Все по нажимали")
        return True

    def parse_card(self, task: Task) -> Task:
        # print("работает:", tasks.get_value(Key.key, '123456'))
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
                    print(f"нажимаем {tt} | {task.get_value(Key.key,'нет ключа')}")
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
