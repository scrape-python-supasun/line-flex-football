from flask import Flask, request, abort
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *
import requests

from datetime import datetime,tzinfo,timedelta
import json
import test_news_eng
class Zone(tzinfo):
    def __init__(self,offset,isdst,name):
        self.offset = offset
        self.isdst = isdst
        self.name = name
    def utcoffset(self, dt):
        return timedelta(hours=self.offset) + self.dst(dt)
    def dst(self, dt):
            return timedelta(hours=1) if self.isdst else timedelta(0)
    def tzname(self,dt):
         return self.name
datetimeUtc = datetime.utcnow().strftime('%d/%m/%Y')
# datetimeUtc = datetime.utcnow().strftime('%Y/%m/%d')


app = Flask(__name__)



line_bot_api = LineBotApi('2P+U0QYQ8O7OlwBMEV1gzHRtNjLtRtEPeqj2wrhNmWpqbUdUxh6ArF0PzzFfBLHpIhbed+10m7dDzSdAOUZGJJEmEYXMu4NyWK5sFd30pu7TL7HSJ46iLMqOKEh7Dce/FEEyh3KsDs3/mYMGkVSq0AdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('7641cb5f9a109c3159ac2ce3505aa59c')


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    # ball = requests.get('https://scrape-news-football-eng.herokuapp.com/time?dayTimeNews={}').format(datetimeUtc).json()
    apiNewEng = ('https://scrape-news-football-eng.herokuapp.com/')
   
   
    allDataNewsEngs = requests.get(apiNewEng).json()
   
    carousel_container = CarouselContainer()
    # T = new_eng
    # H = tablelLeague
    if 'B' in event.message.text:
        for allDataNewsEng in allDataNewsEngs[0:5]:
            categoryNewsEng = allDataNewsEng['category']
            dayTimeNewsEng = allDataNewsEng['dayTimeNews']
            descriptionNewsEng = allDataNewsEng['description']
            headerNewsEng = allDataNewsEng['header']
            linkWebNewsEng = allDataNewsEng['linkWeb']
            minuesTimesNewsEng = allDataNewsEng['minuesNewTimes']
            photoNewEng = allDataNewsEng['photo']
            print(allDataNewsEng)
            # เข้าไปเปลี่ยนเป็นบรรทัดเดียวได้ทีได้ที่ https://codebeautify.org/jsonviewer/cb7f415d
            newsEng = """{"type":"bubble","styles":{"header":{"backgroundColor":"#c70039"}},"header":{"type":"box","layout":"vertical","contents":[{"type":"text","wrap":true,"text":"Day:%s Time:%s","weight":"bold","color":"#FFFFFF","size":"sm"},{"type":"filler"},{"type":"text","wrap":true,"text":"%s","weight":"bold","color":"#FFFFFF","size":"xl"}]},"hero":{"type":"image","url":"%s","size":"full","aspectRatio":"20:13","aspectMode":"cover","action":{"type":"uri","uri":"http://linecorp.com/"}},"body":{"type":"box","layout":"horizontal","spacing":"sm","flex":4,"contents":[{"type":"box","layout":"vertical","margin":"lg","spacing":"xl","contents":[{"type":"text","wrap":false,"text":"%s","size":"lg"},{"type":"filler"},{"type":"text","wrap":true,"text":"%s","size":"md"}]}]},"footer":{"type":"box","layout":"vertical","spacing":"sm","contents":[{"type":"button","style":"primary","action":{"type":"uri","label":"See more","uri":"%s"}}]}}"""%(dayTimeNewsEng,minuesTimesNewsEng,categoryNewsEng,photoNewEng,headerNewsEng,descriptionNewsEng,linkWebNewsEng)
            newsEng = json.loads(newsEng)
            carousel_container.contents.append(newsEng)
        seeMorePageNewEng = '''{"type":"bubble","body":{"type":"box","layout":"vertical","spacing":"sm","contents":[{"type":"button","flex":1,"gravity":"center","action":{"type":"uri","label":"See more","uri":"https://linecorp.com"}}]}}'''
        seeMorePageNewEng = json.loads(seeMorePageNewEng)
        carousel_container.contents.append(seeMorePageNewEng)
        line_bot_api.reply_message(event.reply_token, FlexSendMessage(alt_text='Fixtures', contents=carousel_container))
            # print(type(bubble))
        print("print message is:",event.message.text)
        print("---------------success News Eng---------------")
    # elif 'Table {}'.format('Italian-Serie-B') in event.message.text:
    #     apiTableLeague = ('https://scrape-league-ball.herokuapp.com/')
    #     allDataLinkTables = requests.get(apiTableLeague).json()
    #     for allDataLinkTable in allDataLinkTables:
    #         leagueNameApi = allDataLinkTable['leagueName']
    #         # allDataLinkTable = requests.get(leagueNameApi).json()
    #         apiNameLeague = ('https://scrape-league-ball.herokuapp.com/league?leagueName={}').format('Italian-Serie-B')
    #         allDataLinkTables = requests.get(apiNameLeague).json()
    #     print(allDataLinkTables)

    else:
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=event.message.text))

    
if __name__ == '__main__':
    app.run(debug=True, port=80)