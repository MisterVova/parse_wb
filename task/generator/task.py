class Task:
    def __init__(self, url):
        self.url = url
        self.prices = []

    def add_price(self, price):
        self.prices.append(price)


class TaskList:
    @staticmethod
    def get_tasks():
        for url in TaskList.get_urls():
            # print(url)
            yield Task(url)

    url_list = [
        "https://www.wildberries.ru/catalog/0/search.aspx?sort=popular&search=%D0%B0%D0%B9%D1%84%D0%BE%D0%BD+11",
        "https://www.wildberries.ru/catalog/0/search.aspx?sort=popular&search=%D0%BA%D1%80%D0%BE%D1%81%D1%81%D0%BE%D0%B2%D0%BA%D0%B8+%D0%BC%D1%83%D0%B6%D1%81%D0%BA%D0%B8%D0%B5",
        "https://www.wildberries.ru/catalog/igrushki/sbornye-modeli",
        "https://www.wildberries.ru/catalog/0/search.aspx?sort=popular&search=%D0%BA%D1%80%D0%BE%D1%81%D1%81%D0%BE%D0%B2%D0%BA%D0%B8+%D0%B6%D0%B5%D0%BD%D1%81%D0%BA%D0%B8%D0%B5+%D0%BB%D0%B5%D1%82%D0%BD%D0%B8%D0%B5+%D0%B4%D1%8B%D1%88%D0%B0%D1%89%D0%B8%D0%B5",
    ]

    @staticmethod
    def get_urls():
        for url in TaskList.url_list:
            # print("--")
            yield url



if __name__ == '__main__':
    for t in TaskList.get_tasks():
        print(t.__dict__)
