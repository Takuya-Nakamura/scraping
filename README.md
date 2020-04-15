# python Scrapingツール群

## 初期設定

```
pip install requests
pip install beautifulsoup4

pip install selenium 
pip install chromedriver-binary

※コマンドは環境に応じてpip3の場合もある。
```


## フォルダ

### yahoo_news(request, selenium)
ヤフーニュースのトップページにアクセスして、各カテゴリのトップ記事リストのカテゴリ、タイトル、URLをCSV形式で出力する。

<img width="600" src="https://user-images.githubusercontent.com/1549408/79186200-f4a41200-7e53-11ea-987e-120057be15ba.gif">

### google
Googleでの検索結果数ページについて、タイトルとリンクを取得する
<img width="600" src="https://user-images.githubusercontent.com/1549408/79190849-3fc42200-7e60-11ea-9052-797a89d34dbf.gif">


### gas
google app script でのAmazon商品ページから商品名取得

<img width="400" src="https://user-images.githubusercontent.com/1549408/79284648-41d8c000-7ef6-11ea-8a59-d9106c8514b9.gif">

