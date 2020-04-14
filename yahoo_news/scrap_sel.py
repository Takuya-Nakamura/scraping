from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from pprint import pprint
import chromedriver_binary


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

###############
# functions
###############


def getNewsListCsv(html):
    html = html.get_attribute("innerHTML")
    soup = BeautifulSoup(html, "html.parser")

    # category
    category_elem = soup.select_one("#snavi li.current a")
    category_text = category_elem.contents[0]

    # newslist
    a_list = soup.select(".topicsListItem a")

    text = ''
    for elem in a_list:
        text += "%s,%s,%s\n" % (category_text, elem.contents[0], elem['href'])
    return text


def getChromeDriver():
    return webdriver.Chrome()


def getHeadlessChromeDriver():
    options = Options()
    options.add_argument('--headless')
    return webdriver.Chrome(options=options)


###############
# main
###############
output = ''

driver = getChromeDriver()
# driver = getHeadlessChromeDriver()

driver.get('https://news.yahoo.co.jp')

for url in data:
    driver.get(url)
    html = driver.find_element_by_tag_name("html")
    output += getNewsListCsv(html)

print(output)
