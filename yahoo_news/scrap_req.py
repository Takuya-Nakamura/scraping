import requests
from bs4 import BeautifulSoup
from pprint import pprint

data = [
    'https://news.yahoo.co.jp',
    'https://news.yahoo.co.jp/categories/domestic',
    'https://news.yahoo.co.jp/categories/world',
    'https://news.yahoo.co.jp/categories/business',
    'https://news.yahoo.co.jp/categories/entertainment',
    'https://news.yahoo.co.jp/categories/sports',
    'https://news.yahoo.co.jp/categories/it',
    'https://news.yahoo.co.jp/categories/science',
    'https://news.yahoo.co.jp/categories/local',
]


def main():
    output = ''
    for url in data:
        res = requests.get(url)
        html = res.content
        output += getNewsListCsv(html)

    print(output)


def getNewsListCsv(html):
    soup = BeautifulSoup(html, "html.parser")

    # カテゴリ
    category_elem = soup.select_one("#snavi li.current a")
    category_text = category_elem.contents[0]

    # newslist
    a_list = soup.select(".topicsListItem a")

    text = ''
    for elem in a_list:
        text += "%s,%s,%s\n" % (category_text, elem.contents[0], elem['href'])

    return text


# 実行
main()
