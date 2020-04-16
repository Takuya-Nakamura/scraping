# https://gspread.readthedocs.io/en/latest/user-guide.html#updating-cells
# pip3 install gspread
# pip3 install oauth2client

import gspread
import json
from oauth2client.service_account import ServiceAccountCredentials

# TODO SET
SPREADSHEET_KEY = ''
KEY_JSON = ''


def main():
    #

    # spred_sheet書き込み
    client = login()
    sheet = getSheet(client)
    sheet.update_cell(1, 1, "test")


def login():
    # 2つのAPIを記述しないとリフレッシュトークンを3600秒毎に発行し続けなければならない
    scope = ['https://spreadsheets.google.com/feeds',
             'https://www.googleapis.com/auth/drive']

    # 認証情報設定
    # ダウンロードしたjsonファイル名をクレデンシャル変数に設定（秘密鍵、Pythonファイルから読み込みしやすい位置に置く）
    credentials = ServiceAccountCredentials.from_json_keyfile_name(
        KEY_JSON, scope)

    # OAuth2の資格情報を使用してGoogle APIにログインします。
    return gspread.authorize(credentials)


def getSheet(client):
    return client.open_by_key(SPREADSHEET_KEY).sheet1


main()
