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
    api = ('https://scrape-news-football-eng.herokuapp.com/')
    allDatas = requests.get(api).json()
    # print("all json is =",allDatas)
    for allData in allDatas[:2]:
        category = allData['category']
        dayTimeNews = allData['dayTimeNews']
        description = allData['description']
        header = allData['header']
        linkWeb = allData['linkWeb']
        minuesNewTimes = allData['minuesNewTimes']
        photo = allData['photo']
        print(category)
 
    carousel_container = CarouselContainer()

    # bubble = '''{"type":"bubble","hero":{"type":"image","url":"https://scdn.line-apps.com/n/channel_devcenter/img/fx/01_1_cafe.png","size":"full","aspectRatio":"20:13","aspectMode":"cover","action":{"type":"uri","uri":"http://linecorp.com/"}},"body":{"type":"box","layout":"vertical","contents":[{"type":"text","text":"Brown Cafe","weight":"bold","size":"xl"},{"type":"box","layout":"baseline","margin":"md","contents":[{"type":"icon","size":"sm","url":"https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gold_star_28.png"},{"type":"icon","size":"sm","url":"https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gold_star_28.png"},{"type":"icon","size":"sm","url":"https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gold_star_28.png"},{"type":"icon","size":"sm","url":"https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gold_star_28.png"},{"type":"icon","size":"sm","url":"https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gray_star_28.png"},{"type":"text","text":"4.0","size":"sm","color":"#999999","margin":"md","flex":0}]},{"type":"box","layout":"vertical","margin":"lg","spacing":"sm","contents":[{"type":"box","layout":"baseline","spacing":"sm","contents":[{"type":"text","text":"Place","color":"#aaaaaa","size":"sm","flex":1},{"type":"text","text":"Miraina Tower, 4-1-6 Shinjuku, Tokyo","wrap":true,"color":"#666666","size":"sm","flex":5}]},{"type":"box","layout":"baseline","spacing":"sm","contents":[{"type":"text","text":"Time","color":"#aaaaaa","size":"sm","flex":1},{"type":"text","text":"10:00 - 23:00","wrap":true,"color":"#666666","size":"sm","flex":5}]}]}]},"footer":{"type":"box","layout":"vertical","spacing":"sm","contents":[{"type":"button","style":"link","height":"sm","action":{"type":"uri","label":"CALL","uri":"https://linecorp.com"}},{"type":"button","style":"link","height":"sm","action":{"type":"uri","label":"open","uri":"https://linecorp.com"}},{"type":"spacer","size":"sm"}],"flex":0}}'''
    bubble2 = '''{"type":"bubble","hero":{"type":"image","url":"https://scdn.line-apps.com/n/channel_devcenter/img/fx/01_3_movie.png","size":"full","aspectRatio":"20:13","aspectMode":"cover","action":{"type":"uri","uri":"http://linecorp.com/"}},"body":{"type":"box","layout":"vertical","spacing":"md","contents":[{"type":"text","text":"BROWN'S ADVENTUREIN MOVIE","wrap":true,"weight":"bold","gravity":"center","size":"xl"},{"type":"box","layout":"baseline","margin":"md","contents":[{"type":"icon","size":"sm","url":"https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gold_star_28.png"},{"type":"icon","size":"sm","url":"https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gold_star_28.png"},{"type":"icon","size":"sm","url":"https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gold_star_28.png"},{"type":"icon","size":"sm","url":"https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gold_star_28.png"},{"type":"icon","size":"sm","url":"https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gray_star_28.png"},{"type":"text","text":"4.0","size":"sm","color":"#999999","margin":"md","flex":0}]},{"type":"box","layout":"vertical","margin":"lg","spacing":"sm","contents":[{"type":"box","layout":"baseline","spacing":"sm","contents":[{"type":"text","text":"Date","color":"#aaaaaa","size":"sm","flex":1},{"type":"text","text":"Monday 25, 9:00PM","wrap":true,"size":"sm","color":"#666666","flex":4}]},{"type":"box","layout":"baseline","spacing":"sm","contents":[{"type":"text","text":"Place","color":"#aaaaaa","size":"sm","flex":1},{"type":"text","text":"7 Floor, No.3","wrap":true,"color":"#666666","size":"sm","flex":4}]},{"type":"box","layout":"baseline","spacing":"sm","contents":[{"type":"text","text":"Seats","color":"#aaaaaa","size":"sm","flex":1},{"type":"text","text":"C Row, 18 Seat","wrap":true,"color":"#666666","size":"sm","flex":4}]}]},{"type":"box","layout":"vertical","margin":"xxl","contents":[{"type":"spacer"},{"type":"image","url":"https://scdn.line-apps.com/n/channel_devcenter/img/fx/linecorp_code_withborder.png","aspectMode":"cover","size":"xl"},{"type":"text","text":"You can enter the theater by using this code instead of a ticket","color":"#aaaaaa","wrap":true,"margin":"xxl","size":"xs"}]}]}}'''
    # bubble3 = '''{"type":"carousel","contents":[{"type":"bubble","hero":{"type":"image","size":"full","aspectRatio":"20:13","aspectMode":"cover","url":"https://scdn.line-apps.com/n/channel_devcenter/img/fx/01_5_carousel.png"},"body":{"type":"box","layout":"vertical","spacing":"sm","contents":[{"type":"text","text":"Arm Chair, White","wrap":true,"weight":"bold","size":"xl"},{"type":"box","layout":"baseline","contents":[{"type":"text","text":"$49","wrap":true,"weight":"bold","size":"xl","flex":0},{"type":"text","text":".99","wrap":true,"weight":"bold","size":"sm","flex":0}]}]},"footer":{"type":"box","layout":"vertical","spacing":"sm","contents":[{"type":"button","style":"primary","action":{"type":"uri","label":"Add to Cart","uri":"https://linecorp.com"}},{"type":"button","action":{"type":"uri","label":"Add to wishlist","uri":"https://linecorp.com"}}]}},{"type":"bubble","hero":{"type":"image","size":"full","aspectRatio":"20:13","aspectMode":"cover","url":"https://scdn.line-apps.com/n/channel_devcenter/img/fx/01_6_carousel.png"},"body":{"type":"box","layout":"vertical","spacing":"sm","contents":[{"type":"text","text":"Metal Desk Lamp","wrap":true,"weight":"bold","size":"xl"},{"type":"box","layout":"baseline","flex":1,"contents":[{"type":"text","text":"$11","wrap":true,"weight":"bold","size":"xl","flex":0},{"type":"text","text":".99","wrap":true,"weight":"bold","size":"sm","flex":0}]},{"type":"text","text":"Temporarily out of stock","wrap":true,"size":"xxs","margin":"md","color":"#ff5551","flex":0}]},"footer":{"type":"box","layout":"vertical","spacing":"sm","contents":[{"type":"button","flex":2,"style":"primary","color":"#aaaaaa","action":{"type":"uri","label":"Add to Cart","uri":"https://linecorp.com"}},{"type":"button","action":{"type":"uri","label":"Add to wish list","uri":"https://linecorp.com"}}]}},{"type":"bubble","body":{"type":"box","layout":"vertical","spacing":"sm","contents":[{"type":"button","flex":1,"gravity":"center","action":{"type":"uri","label":"See more","uri":"https://linecorp.com"}}]}}]}'''
    bubble4 = '''{"type":"bubble","header":{"type":"box","layout":"vertical","contents":[{"type":"text","wrap":true,"text":"วันที่:2019/05/02 เวลา:18.00","weight":"bold","color":"#aaaaaa","size":"sm"},{"type":"filler"},{"type":"text","wrap":true,"text":"ข่าวกีข่าวกีข","weight":"bold","color":"#aaaaaa","size":"xl"}]},"hero":{"type":"image","url":"https://scdn.line-apps.com/n/channel_devcenter/img/fx/01_4_news.png","size":"full","aspectRatio":"20:13","aspectMode":"cover","action":{"type":"uri","uri":"http://linecorp.com/"}},"body":{"type":"box","layout":"horizontal","spacing":"sm","flex":4,"contents":[{"type":"box","layout":"vertical","margin":"lg","spacing":"md","contents":[{"type":"text","wrap":false,"text":"headerheaderheaderheaderheaderheaderheaderheaderheaderheader","size":"lg"},{"type":"filler"},{"type":"text","wrap":true,"text":"detaildetaildetaildetaildetaildetaildetaildetaildetaildetaildetaildetail","size":"md"}]}]},"footer":{"type":"box","layout":"vertical","spacing":"sm","contents":[{"type":"button","style":"primary","action":{"type":"uri","label":"Add to Cart","uri":"https://linecorp.com"}}]}}'''
    # bubble = json.loads(bubble)
    bubble2 = json.loads(bubble2)
    # bubble3 = json.loads(bubble3)
    bubble4 = json.loads(bubble4)
    # carousel_container.contents.append(bubble)
    carousel_container.contents.append(bubble2)
    # carousel_container.contents.append(bubble3)
    carousel_container.contents.append(bubble4)

    # print(type(bubble))
    print("test success",event.message.text)

        # print(event.message.text)
        # print(type(event.message.text))
    line_bot_api.reply_message(event.reply_token, FlexSendMessage(alt_text='Fixtures', contents=carousel_container))

if __name__ == '__main__':
    app.run(debug=True, port=80)