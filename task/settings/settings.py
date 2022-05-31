import json

# URL_SERVER = "https://script.google.com/macros/s/AKfycbx2Jm6G5vZLIgOYE8Bd2FWRevyn6KQKAGgEU4OTV4TUeIEYZ_RBFaJ7Ldau9MNz??????/exec"
URL_SERVER = "https://script.google.com/macros/s/AKfycbyM_?????/exec"
URL_WB_MAIN = "https://www.wildberries.ru/"
URL_WB_SEARCH = "https://www.wildberries.ru/catalog/0/search.aspx?sort=popular&search="
THREADS_COUNT = 4
WEBDRIVER_HEADLESS = False
SLEEP = 2

settings = {}
try:
    with open('settings.json', encoding='utf-8') as f:
        settings = json.load(f)
except:
    settings["URL_SERVER"] = URL_SERVER
    settings["URL_WB_MAIN"] = URL_WB_MAIN
    settings["URL_WB_SEARCH"] = URL_WB_SEARCH
    settings["THREADS_COUNT"] = THREADS_COUNT
    settings["WEBDRIVER_HEADLESS"] = WEBDRIVER_HEADLESS
    settings["SLEEP"] = SLEEP
    with open('settings.json', 'w') as outfile:
        json.dump(settings, outfile,indent=4 )


value = settings.get("URL_SERVER")
if value:
    URL_SERVER = value
value = settings.get("URL_WB_MAIN")
if value:
    URL_WB_MAIN = value
value = settings.get("URL_WB_SEARCH")
if value:
    URL_WB_SEARCH = value
value = settings.get("THREADS_COUNT")
if value:
    THREADS_COUNT = value
value = settings.get("WEBDRIVER_HEADLESS")
if value:
    WEBDRIVER_HEADLESS = value
value = settings.get("SLEEP")
if value:
    SLEEP = value

#
# URL_SERVER = settings["URL_SERVER"] if settings["URL_SERVER"] else URL_SERVER
# URL_WB_MAIN = settings["URL_WB_MAIN"] if settings["URL_WB_MAIN"] else URL_WB_MAIN
# URL_WB_SEARCH = settings["URL_WB_SEARCH"] if settings["URL_WB_SEARCH"] else URL_WB_SEARCH
# THREADS_COUNT = settings["THREADS_COUNT"] if settings["THREADS_COUNT"] else THREADS_COUNT
# WEBDRIVER_HEADLESS = settings["WEBDRIVER_HEADLESS"] if settings["WEBDRIVER_HEADLESS"] else WEBDRIVER_HEADLESS
# SLEEP = settings["SLEEP"] if settings["SLEEP"] else SLEEP

# python3 -m pip freeze > requirements.txt
# pip3 install -r requirements.txt
