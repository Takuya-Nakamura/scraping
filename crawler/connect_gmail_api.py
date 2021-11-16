# https://developers.google.com/gmail/api/quickstart/python
# https://developers.google.com/gmail/api/reference/rest/v1/users.messages#Message
# pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib


import webbrowser
from pprint import pprint
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from gmail_credential import get_credential

import base64
import re
import sys
import time


def main():
    label_name = sys.argv[1]
    print('[start] label:', label_name)

    creds = get_credential()
    service = build('gmail', 'v1', credentials=creds, cache_discovery=False)

    label = search_label(service, label_name)
    if(not label):
        print('入力されたラベルはありません。', label_name)
        return

    messages = list_messages(service, '', [label['id']])

    for msg in messages:
        print('#### 件名: ', msg['subject'])
        urls = set(extract_url(msg['body']))  # unique

        for u in urls:
            print(u)
            time.sleep(1)
            webbrowser.open(u, new=2, autoraise=True)


def search_label(service, label_name):
    results = service.users().labels().list(userId='me').execute()
    labels = results.get('labels', [])
    elm = next(filter(lambda x: x['name'] == label_name, labels), None)
    return elm


def decode_base64url_data(data):
    decoded_bytes = base64.urlsafe_b64decode(data)
    decoded_message = decoded_bytes.decode('UTF-8')
    return decoded_message


def extract_url(text):
    # http://trelab.info/python/python-%E6%AD%A3%E8%A6%8F%E8%A1%A8%E7%8F%BE%E3%81%A7url%E3%81%AE%E4%B8%80%E8%87%B4%E3%83%81%E3%82%A7%E3%83%83%E3%82%AF%E3%80%81%E6%8A%BD%E5%87%BA%E3%82%92%E8%A1%8C%E3%81%86/
    return re.findall('https?://[\w/:%#\$&\?\(\)~\.=\+\-]+', text)


def list_messages(service, query, label_ids=[], count=2):
    message_ids = (
        service.users()
        .messages()
        .list(userId='me', maxResults=count, q=query, labelIds=label_ids)
        .execute()
    )
    if message_ids['resultSizeEstimate'] == 0:
        print('対象のメールはありません。')
        return []

    messages = []
    for message_id in message_ids['messages']:
        id = message_id['id']
        message_detail = (
            service.users()
            .messages()
            .get(userId='me', id=id)
            .execute()
        )

        # 詳細取得
        message = {}
        message['id'] = id
        subject = next(filter(
            lambda h: h['name'] == 'Subject', message_detail['payload']['headers']), None)
        message['subject'] = subject['value']

        # payloadがある場合はにaltanativeがあるか確認し、alternativeの場合はそこのpartsをpyloadと差し替える。
        # 上記のaltanetiveのpayloadがないpartsがあればその最初の
        #
        payload = {}
        if('parts' in message_detail['payload']):
            payload = next(filter(
                lambda part: part['mimeType'] == 'multipart/alternative', message_detail['payload']['parts']), None)

        if(not payload and 'parts' in message_detail['payload']):
            payload = message_detail['payload']['parts'][0]

        if(not payload):
            payload = message_detail['payload']

        message['body'] = getMessageBody(payload)

        messages.append(message)
    # for message_id in message_ids['messages']:

    return messages
# def list_messages


def getMessageBody(payload):
    '''
    message_detail['payload']['body']に値がある場合はそれを取得
    ない場合はmessage_detail['payload']['parts']の中を見てtext/plainの要素を取得する
    '''
    if 'body' in payload and 'data' in payload['body']:
        return decode_base64url_data(payload['body']['data'])
    else:
        payload = next(
            filter(lambda part: part['mimeType'] == 'text/plain', payload['parts']), None)
        if payload:
            return decode_base64url_data(payload['body']['data'])
        else:
            return '[抽出できず]'


##########################
main()
