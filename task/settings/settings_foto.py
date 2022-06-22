import json

URL_SERVER = "https://script.google.com/macros/s/AKfycbzvKtZYbc7S7i9V7Cz6UNaDjbFx0gYzW8vFPCtAWUITB0oy3Ws-yDiTYK4z6MnHEKIYGw/exec"
URL_YA_MAIN = "https://yandex.ru/images/search"

THREADS_COUNT = 1
WEBDRIVER_HEADLESS = False
SLEEP = 2

# Если в ответе поиска нет карточек товара с сайтов wb, ozon, яндексмаркет, исбермегамаркет, возвращаем значение не найдено совпадений
FILTER_FOTO = {
    "ozon": ["/www.ozon.ru/product/", ],
    "wb": ["/www.wildberries.ru/catalog/",".wildberries.ru/catalog/"],
    "market_yandex": ["/market.yandex.ru/product","/market.yandex."],
    "sbermegamarket": ["/sbermegamarket.ru/", "/sbermegamarket.ru/catalog/"],
}


settings = {}
try:
    with open('settings_foto.json', encoding='utf-8') as f:
        settings = json.load(f)
        print(settings)
except:
    settings["URL_SERVER"] = URL_SERVER
    settings["URL_YA_MAIN"] = URL_YA_MAIN
    settings["THREADS_COUNT"] = THREADS_COUNT
    settings["WEBDRIVER_HEADLESS"] = WEBDRIVER_HEADLESS
    settings["SLEEP"] = SLEEP
    settings["FILTER_FOTO"] = FILTER_FOTO
    with open('settings_foto.json', 'w') as outfile:
        json.dump(settings, outfile, indent=4)

value = settings.get("URL_SERVER")
if value:
    URL_SERVER = value
value = settings.get("URL_YA_MAIN")
if value:
    URL_YA_MAIN = value
value = settings.get("THREADS_COUNT")
if value:
    THREADS_COUNT = value
value = settings.get("WEBDRIVER_HEADLESS")
if value:
    WEBDRIVER_HEADLESS = value
value = settings.get("SLEEP")
if value:
    SLEEP = value
value = settings.get("FILTER_FOTO")
if value:
    FILTER_FOTO = value



#
# URL_SERVER = settings["URL_SERVER"] if settings["URL_SERVER"] else URL_SERVER
# URL_WB_MAIN = settings["URL_WB_MAIN"] if settings["URL_WB_MAIN"] else URL_WB_MAIN
# URL_WB_SEARCH = settings["URL_WB_SEARCH"] if settings["URL_WB_SEARCH"] else URL_WB_SEARCH
# THREADS_COUNT = settings["THREADS_COUNT"] if settings["THREADS_COUNT"] else THREADS_COUNT
# WEBDRIVER_HEADLESS = settings["WEBDRIVER_HEADLESS"] if settings["WEBDRIVER_HEADLESS"] else WEBDRIVER_HEADLESS
# SLEEP = settings["SLEEP"] if settings["SLEEP"] else SLEEP

# python3 -m pip freeze > requirements.txt
# pip3 install -r requirements.txt
