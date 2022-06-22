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
from task.settings.settings_foto import URL_YA_MAIN, SLEEP, WEBDRIVER_HEADLESS, FILTER_FOTO
from bs4 import BeautifulSoup
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait


class TaskExe:

    def __init__(self):
        self.driver = None
        self.options = ChromiumOptions()

        self.base_url = URL_YA_MAIN

    def exe(self, task: Task) -> Task:
        try:
            sheet_name = task.get_sheet_name()
            if sheet_name == SheetNames.НеОпределён:
                return self.exe_old(task)
            elif sheet_name == SheetNames.Задачи:
                self.parse_task(task)
            elif sheet_name == SheetNames.Фото:
                self.parse_foto(task=task)

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
        time.sleep(6 * 60)
        return task

    def parse_task(self, task: Task):
        time.sleep(6 * 60)
        return task

    def click_cbir_icon(self):
        cbir_icon = self.driver.find_elements(by=By.CLASS_NAME, value='cbir-icon')
        if len(cbir_icon) == 0:
            return False
        self.actions.move_to_element(cbir_icon[0]).perform()
        time.sleep(SLEEP * 0.3)
        self.actions.click().perform()
        time.sleep(SLEEP * 1)
        return True

    def make_Popup2_visible(self, tr=0):
        #     Popup2 Popup2_visible Popup2_target_anchor Popup2_view_default CbirPanel-Popup
        # "body > header > div > div.serp-header__main > div.serp-header__search2 > form > div.search2__input > span > span > button > div"
        # "/html/body/header/div/div[1]/div[2]/form/div[1]/span/span/button/div"
        # "class="cbir-icon input__cbir-button-icon""
        tr += 1
        if tr > 5: return False

        popup2 = self.driver.find_elements(by=By.CLASS_NAME, value='Popup2_target_anchor')
        if len(popup2) == 0:
            self.click_cbir_icon()
            return self.make_Popup2_visible(tr)

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
        return self.make_Popup2_visible(tr)

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
        if len(items) == 0:
            return task

        html = items[0].get_attribute("outerHTML")
        soup = BeautifulSoup(html, "html.parser")
        try:
            def get_site(href: str, filer_foto: dict = FILTER_FOTO):
                for site in filer_foto.keys():
                    for reg in filer_foto.get(site):
                        if reg in href:
                            return site
                return None

            values = {}

            item_title = soup.findAll('div', class_='CbirSites-ItemTitle')
            for item in item_title:
                # if len(item_title) > 0:
                a = item.find("a", class_='Link_view_default')
                href = a.get("href")
                text = a.getText()
                # print(href)

                site = get_site(href)
                if not site:
                    continue
                # print(get_site(href), "|", href)
                if not site in values.keys():
                    values[site]=list()

                # v = {
                #     # "site": get_site(href),
                #     "text": text,
                #     "href": href,
                # }
                # values.get(site).append(v)
                values.get(site).append(href)

                # values.append(v)
                # print(v)

            task.set_value(Key.value, values)
            # task.set_value("hrefs", hrefs)
            # task.set_value("tests", tests)
            # FILTER_FOTO
        except:
            traceback.print_exc()
            time.sleep(SLEEP * 50)

        return task

    def parse_foto(self, task: Task) -> Task:
        # print("работает:", tasks.get_value(Key.key, '123456'))
        # url = f"https://www.wildberries.ru/catalog/{tasks.get_value(Key.key, '123456')}/detail.aspx?targetUrl=ST"

        yandex_url = URL_YA_MAIN
        # print(self.driver.current_url)
        if not yandex_url in self.driver.current_url:
            self.driver.get(yandex_url)
            time.sleep(SLEEP * 2)

        url = f"{task.get_value(Key.key, '')}"
        self.driver.set_window_size(1200, 900)
        # time.sleep(SLEEP)
        # self.driver.get(url)
        # time.sleep(SLEEP * 2)

        # time.sleep(10)
        try:
            if not self.make_Popup2_visible(): return task
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
