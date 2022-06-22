import json
import re
import traceback
import time

from selenium.webdriver import ActionChains, Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chromium.options import ChromiumOptions
from selenium import webdriver

from task.generator.key import Key
from task.settings import URL_WB_MAIN, SLEEP, WEBDRIVER_HEADLESS
from bs4 import BeautifulSoup  # ,ResultSet
from task.generator.base_task import BaseTask as Task

from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait

class TaskExe:

    def __init__(self):
        self.driver = None
        self.options = ChromiumOptions()

        self.base_url = URL_WB_MAIN

    def exe(self, task) -> Task:
        try:
            # self.parse_card(tasks)
            self.parse_foto(task)

        except Exception as e:
            # print(f"error: '{e.__traceback__}'")
            # print(tasks.url)
            # traceback_str = ''.join(traceback.format_tb(e.__traceback__))
            # traceback_str = ''.join(traceback.format_(e.__traceback__))
            # print(f"error: '{traceback_str}'")
            traceback.print_exc()

        # for i in range(random.randint(10, 20)):
        #     tasks.add_price(random.randint(100, 200))
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

    def parse_card(self, task: Task) -> Task:
        # print("работает:", tasks.get_value(Key.key, '123456'))
        url = f"https://www.wildberries.ru/catalog/{task.get_value(Key.key, '123456')}/detail.aspx?targetUrl=ST"

        self.driver.get(url)
        footer = self.driver.find_elements(by=By.ID, value='footer')
        if len(footer) > 0:
            # print("footer", footer)
            self.actions.move_to_element(footer[0])
            self.actions.perform()
            time.sleep(2)
            self.actions.move_to_element(footer[0])
            self.actions.perform()

        tabs_content = self.driver.find_elements(by=By.ID, value='tabs-content')
        btn = tabs_content[0].find_elements(by=By.CLASS_NAME, value='select-radio__btn-text')
        if len(btn) > 0:
            self.actions = ActionChains(self.driver, duration=250)
            self.actions.move_to_element_with_offset(btn[0], 5, 5).perform()
            self.actions.scroll(0, 0, 0, 450, duration=5).perform()
            self.actions.move_to_element_with_offset(btn[0], -5, -5).perform()
            self.actions.click(btn[0]).perform()
            select_radio__text = tabs_content[0].find_elements(by=By.CLASS_NAME, value='select-radio__text')
            if len(select_radio__text) > 1:
                self.actions = ActionChains(self.driver, duration=250)
                self.actions.move_to_element_with_offset(select_radio__text[1], 5, 5)
                # page=2
                # print(pagination_next[0].)

                # self.driver.get(f"{tasks.url}&page={steep}")
                #
                self.actions.click(select_radio__text[1])
                # self.actions.click(select_radio__text[1])
                self.actions.perform()
                time.sleep(SLEEP)

            else:
                pass

        container = self.driver.find_elements(by=By.ID, value='container')  # переделать
        # название,
        """ +наименование	+цена	+продано	    +Сумма отзывов	Ср рейтинг	-начало продаж	-дней в продаже	+Продавец
            +name	        +price	 count_sold	    +count_review   count_star	-sale_start	    -sale_days	    +seller"""

        if len(container) > 0:
            html = container[0].get_attribute("outerHTML")
            soup = BeautifulSoup(html, "html.parser")
            # print(html)
            comments = soup.findAll('li', class_='comments__item')
            if len(comments) > 0:
                sale_start = comments[0].find("span", class_='feedback__date').get("content")
                # <span class="feedback__date hide-desktop" itemprop="datePublished" content="2020-12-14T07:34:26Z">14 декабря 2020, 10:34</span>
                task.set_value("sale_start", sale_start)
                # from datetime import datetime
                # print(json.JSONDecoder(f"{sale_start}"))
                # def fromutcformat(utc_str, tz=None):
                #     iso_str = utc_str.replace('Z', '+00:00')
                #     return datetime.fromisoformat(iso_str).astimezone(tz)

                # print(datetime.now() - fromutcformat(sale_start))
            #  price
            price = soup.find("span", class_='price-block__final-price').text
            # price = "".join(re.findall(r'\d+', price))
            price = float("".join(re.findall(r'\d+', f"{price}")))
            task.set_value("price", price)
            # print(price)

            #   name
            name_brande = soup.find('h1', class_="same-part-kt__header").get_text()
            # print(name_brande)
            task.set_value("name", name_brande)
            #   seller

            # count_sold
            count_sold = soup.find('p', class_='same-part-kt__order-quantity j-orders-count-wrapper').span.get_text()
            count_sold = "".join(re.findall(r'\d+', count_sold))
            count_sold = float("".join(re.findall(r'\d+', f"{count_sold}")))
            task.set_value("count_sold", count_sold)
            # print(count_sold)

            # Отзывы count_review
            count_review = soup.find('a', id="a-Comments").get_text()
            # count_review = "".join(re.findall(r'\d+', count_review))
            count_review = float("".join(re.findall(r'\d+', f"{count_review}")))
            task.set_value("count_review", count_review)
            # print(count_review)

            # count_star \\
            count_star = soup.find('span', class_="same-part-kt__rating")
            count_star = count_star.get("class")
            count_star = float("".join(re.findall(r'\d+', f"{count_star}")))
            task.set_value("count_star", count_star)
            # print(count_star)

            # <div class="seller-details__info">
            seller = soup.find('div', class_="seller-details__info")
            seller = seller.find('a', class_="seller-details__title")
            seller = seller.get("href")
            seller = float("".join(re.findall(r'\d+', f"{seller}")))
            task.set_value("seller", seller)
            # print(seller)

        # time.sleep(SLEEP*10)
        return task

    def click_cbir_icon(self):
        cbir_icon = self.driver.find_elements(by=By.CLASS_NAME, value='cbir-icon')
        if len(cbir_icon) == 0:
            return task
        self.actions.move_to_element(cbir_icon[0]).perform()
        time.sleep(SLEEP * 0.3)
        self.actions.click().perform()
        time.sleep(SLEEP * 1)

    def mack_Popup2_visible(self, tr=0):
        #     Popup2 Popup2_visible Popup2_target_anchor Popup2_view_default CbirPanel-Popup
        # "body > header > div > div.serp-header__main > div.serp-header__search2 > form > div.search2__input > span > span > button > div"
        # "/html/body/header/div/div[1]/div[2]/form/div[1]/span/span/button/div"
        # "class="cbir-icon input__cbir-button-icon""
        tr += 1
        if tr > 5: return False

        popup2 = self.driver.find_elements(by=By.CLASS_NAME, value='Popup2_target_anchor')
        if len(popup2) == 0:
            self.click_cbir_icon()
            return self.mack_Popup2_visible(tr)

        popup2_class = popup2[0].get_attribute("class")
        # print(popup2_class)

        if "Popup2_visible" in popup2_class:
            # class ="Icon Icon_size_m Icon_hasGlyph Icon_glyph_x-sign Textinput-Icon Textinput-Clear Textinput-Clear_visible"
            form = self.driver.find_elements(by=By.CLASS_NAME, value='CbirPanel-UrlForm')
            if len(form) == 0:
                return False

            form = form[0]

            clear = form.find_elements(by=By.CLASS_NAME, value='Textinput-Clear')
            if len(clear) > 0:
                clear_class = clear[0].get_attribute("class")
                if "Textinput-Clear_visible" in clear_class:
                    self.actions.move_to_element(clear[0]).perform()
                    time.sleep(SLEEP * 1)
                    self.actions.click().perform()
                    time.sleep(SLEEP * 1)
            return True

        self.click_cbir_icon()
        return self.mack_Popup2_visible(tr)

    def insert_url(self, url):

        form = self.driver.find_elements(by=By.CLASS_NAME, value='CbirPanel-UrlForm')
        if len(form) == 0:
            return False

        form = form[0]

        input_text = form.find_elements(by=By.TAG_NAME, value='input')
        button = form.find_elements(by=By.TAG_NAME, value='button')

        if len(input_text) == 0: return False
        if len(button) == 0: return False

        # print("input", input_text)
        # print("button", button)
        # print("url", url)

        self.actions.move_to_element(input_text[0]).perform()
        time.sleep(SLEEP * 0.2)
        self.actions.click().perform()
        time.sleep(SLEEP * 0.2)
        input_text[0].send_keys(url)
        time.sleep(SLEEP * 0.5)
        self.actions.move_to_element(button[0]).perform()
        time.sleep(SLEEP * 1)
        self.actions.click().perform()
        time.sleep(SLEEP * 1)

        wait = WebDriverWait(self.driver, 60)
        wait.until(ec.presence_of_element_located((By.CLASS_NAME, "CbirSites-Items")))
        self.move_to_footer()
        return True


    def move_to_footer(self):

        # isDisplayed()
        footer = self.driver.find_elements(by=By.CLASS_NAME, value='footer')
        if len(footer) > 0:
            for i in range(10):
                # print("footer", footer)
                footer = self.driver.find_elements(by=By.CLASS_NAME, value='footer')
                # print(f"is_displayed={i}", footer[0].is_displayed())
                # time.sleep(SLEEP * 0.1 * 20)
                self.actions.move_to_element(footer[0])
                self.actions.perform()
                time.sleep(SLEEP * 0.1)

                # print(f"is_displayed={i}", footer[0].is_displayed())
                # if  footer[0].is_displayed() : break


    def extract_data(self, task: Task) -> Task:
        task.set_value("yandex", self.driver.current_url)
        items = self.driver.find_elements(by=By.CLASS_NAME, value='CbirSites-Items')
        if len(items)==0:
            return  task

        html = items[0].get_attribute("outerHTML")
        soup = BeautifulSoup(html, "html.parser")
        try:
            hrefs = []
            tests = []

            item_title = soup.findAll('div', class_='CbirSites-ItemTitle')
            for item in item_title:
            # if len(item_title) > 0:
                a = item.find("a", class_='Link_view_default')
                href = a.get("href")
                test = a.getText()
                # print(href)
                # print(test)
                hrefs.append(href)
                tests.append(test)
            task.set_value(Key.value, hrefs)
            # task.set_value("hrefs", hrefs)
            # task.set_value("tests", tests)
        except:
            pass

        return task

    def parse_foto(self, task: Task) -> Task:
        # print("работает:", tasks.get_value(Key.key, '123456'))
        # url = f"https://www.wildberries.ru/catalog/{tasks.get_value(Key.key, '123456')}/detail.aspx?targetUrl=ST"

        yandex_url = "https://yandex.ru/images/search"
        # print(self.driver.current_url)
        if not yandex_url in self.driver.current_url:
            self.driver.get(yandex_url)
            time.sleep(SLEEP * 2)

        url = f"{task.get_value(Key.url, '')}"
        self.driver.set_window_size(1200, 900)
        # time.sleep(SLEEP)
        # self.driver.get(url)
        # time.sleep(SLEEP * 2)

        # time.sleep(10)
        try:
            if not self.mack_Popup2_visible(): return task
            if not self.mack_Popup2_visible(): return task
            if not self.insert_url(url): return task


            return self.extract_data(task)

        except Exception as e:
            # traceback_str = ''.join(traceback.format_tb(e.__traceback__))
            # print(f"error: '{traceback_str}'")
            traceback.print_exc()
            time.sleep(SLEEP * 50)
            # time.sleep(SLEEP * (t + 1) * 10)
            self.driver.set_window_size(1200, 900)
            self.driver.get(url)
            pass

        return task

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
                    print(f"нажимаем {tt} | {task.get_value(Key.key, 'нет ключа')}")
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
    # pass
    img_url_list = [
        "https://images.wbstatic.net/big/new/38920000/38927524-1.jpg",
        "https://images.wbstatic.net/big/new/29020000/29026906-1.jpg",
        "https://images.wbstatic.net/big/new/29280000/29287500-2.jpg",
        "https://images.wbstatic.net/big/new/76940000/76948656-1.jpg"
    ]

    taskExe = TaskExe()
    taskExe.start()
    for url in img_url_list:
        obj = {
            Key.url: f"{url}",

        }

        task = Task(obj)
        # print(tasks.obj)
        taskExe.exe(task)
        print(task.obj)

    taskExe.end()
# """https://www.wildberries.ru/catalog/23361750/detail.aspx?targetUrl=ST"""
