from urllib.parse import urlparse
import requests
from bs4 import BeautifulSoup
from pprint import pprint
import time
import os

# TODO: 取得したURLが404だったら除外とかしたい..

# 特定URL以下のURL以下一覧を取得したい
# URL・起点ディレクトリを指定してhtmlを取得する
# 以下を繰り返す
# あるURLのHTMLを取得する。取得したらアクセス済みとする
# パースして linkを取得する。
# linkの中から同一ドメインで指定ディレクトリ配下のものに絞る
# linkをリストに追加順次、未アクセスのものだけ再度アクセスする。
# page_listがすべてアクセス済みになるまで繰り返す

# domain = 'http://doutsure.com'
# domain = 'https://ai-inter1.com'
domain = 'https://www.jackall.co.jp'
# https://ai-inter1.com/  key errorが出る
# https://railsguides.jp/ 
# https://www.javadrive.jp/ 相対パス解決が必要

main_hostname = ''

accessed_links = []
not_accessed_links = []

exclude_ext = ['jpg', 'jpeg', 'png', 'gif', 'pdf', 'csv', 'tsv', 'txt']
sleep_sec = 2

def main():
    # start_url = 'http://doutsure.com'
    start_url = 'https://www.jackall.co.jp'

    obj = urlparse(start_url)
    global main_hostname
    main_hostname = obj.hostname
    not_accessed_links.append(start_url)

    # getLinks('http://doutsure.com/blog/page-808')

    
    while not loopEnd():
        loopFunction()

    print('################## loop end')
    pprint(not_accessed_links)
    
    pprint(accessed_links)
    

def loopFunction():
    global not_accessed_links

    time.sleep(sleep_sec)

    print('################## loop start')
    print('##not_accessed_links:' + str(len(not_accessed_links)))
    print('##accessed_links:' + str(len(accessed_links)))

    target_link = not_accessed_links.pop()
    if not target_link :
      return 
   
    print('ターゲットURL:' + target_link)

    if(target_link in accessed_links):
        print('in accessed_links SKIP ')
        return

    new_links = getLinks(target_link)

    if new_links == False:
        return

    # accessed_linkに追加
    accessed_links.append(target_link)

    # 取得したリンクが既にリストされているものでなければ追加する
    for l in new_links:
        if(l not in accessed_links and l not in not_accessed_links):
            not_accessed_links.append(l)

    not_accessed_links = list(set(not_accessed_links))
    


def loopEnd():
    return len(not_accessed_links) == 0


def getLinks(link):
    try:
        res = requests.get(link)
        res.raise_for_status()
    except requests.exceptions.RequestException as e:
        ## accessedに入れない
        print('[SKIP]リクエストエラー', e)
        return False
    
    if 'text/html' not in res.headers['Content-Type']:
        ## accessedに入れない
        print('[SKIP]SKIP BECAUSE NOT HTML:', res.headers['Content-Type'])
        return False

    try:
        soup = BeautifulSoup(res.content, "html.parser")
        elems = soup.find_all("a")
        return set(list(map(linkCheck, elems)))

    except Exception as e:
        #accessedに入れる
        print("error", type(e))
        print(e.args)
        return [] #accessedに入れる


def linkCheck(elem):
    # ルート相対の場合ドメインを補完する
    #TODO: 位置相対の場合アクセスシテイルURLで補完する
    # 指定ディレクトリであるか
    # 画像やPDF除外
    if('href' not in elem.attrs):
        return

    link = elem.attrs['href']

    if (link[0:1] == '/'):
        link = domain + link

    urlObj = urlparse(link)
    hostname = urlObj.hostname

    ext = os.path.splitext(link)[1][1:]

    if(
        hostname != None and
        hostname == main_hostname and
        ext not in exclude_ext
    ):
        return link


# 実行
main()
