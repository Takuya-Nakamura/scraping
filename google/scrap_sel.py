from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from pprint import pprint
import chromedriver_binary
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

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


def getSearchResultData():
    results = driver.find_elements_by_css_selector("#rso .r")
    res = ''
    for elem in results:
        title = elem.find_element_by_css_selector("h3").text
        url = elem.find_element_by_css_selector("a").get_attribute('href')
        res += '%s,%s\n' % (title, url)
    return res


###############
# main
###############
output = ''
search_word = "python scraping"

# driver
driver = getChromeDriver()
# driver = getHeadlessChromeDriver()

# 起動
driver.set_window_size(600, 700)
driver.get("https://www.google.com/")

# 検索画面でtext入力
form = driver.find_element_by_css_selector(
    "#tsf > div:nth-child(2) > div.A8SBwf > div.RNNXgb > div > div.a4bIc > input")
form.send_keys(search_word)

# 検索実行
button = driver.find_element_by_css_selector(
    "#tsf > div:nth-child(2) > div.A8SBwf > div.FPdoLc.tfB0Bf > center > input.gNO89b")
button.click()
WebDriverWait(driver, 15).until(EC.presence_of_all_elements_located)

for i in range(5):
    # データ取得
    output += getSearchResultData()
    # 次のページに遷移
    nextBUtton = driver.find_element_by_css_selector("#pnnext").click()
    WebDriverWait(driver, 15).until(EC.presence_of_all_elements_located)

print(output)
