import requests
from linebot.models import *
from linebot.models.template import *
import json
from linebot import (
    LineBotApi, WebhookHandler
)
# line_bot_api = LineBotApi('8Q/36jEbtoR+8iEpTPd6t3wUzAwQQ5SXe6u8jRXLTAGBpreJuoBdSWguLxyPpHJ3EteJFaoU7Au1CpQbASQd7P7Vhoe94caQotwVkKg+xxQudC7NeO+plQx0Qch0MrKnFZyDwwKmff0J8SUU9XNeegdB04t89/1O/w1cDnyilFU=')
line_bot_api = LineBotApi('2P+U0QYQ8O7OlwBMEV1gzHRtNjLtRtEPeqj2wrhNmWpqbUdUxh6ArF0PzzFfBLHpIhbed+10m7dDzSdAOUZGJJEmEYXMu4NyWK5sFd30pu7TL7HSJ46iLMqOKEh7Dce/FEEyh3KsDs3/mYMGkVSq0AdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('7641cb5f9a109c3159ac2ce3505aa59c')

def generate_news_flex(nimg,nheader,ncontent):
  nflex = '''{
    "type": "bubble",
    "header": {
      "type": "box",
      "layout": "horizontal",
      "contents": [
        {
          "type": "text",
          "wrap":false,
          "text": "ข่าวกีฬา",
          "weight": "bold",
          "color": "#aaaaaa",
          "size": "sm"
        }
      ]
    },
    "hero": {
      "type": "image",
      "url": "%s",
      "size": "full",
      "aspectRatio": "20:13",
      "aspectMode": "cover",
      "action": {
        "type": "uri",
        "uri": "http://linecorp.com/"
      }
    },
    "body": {
      "type": "box",
      "layout": "horizontal",
      "spacing": "xl",
      "flex":4,
      "contents": [
        {
          "type": "box",
          "layout": "vertical",
          "margin": "lg",
          "contents": [
            {
              "type": "text",
              "wrap": true,
              "text": "%s",
              "size": "xs"
            },
            {
              "type": "filler"
            },
            {
              "type": "text",
              "wrap": true,
              "text": "%s",
              "size": "xs"
            }
          ]
        }
      ]
    }
  }'''%(nimg,nheader,ncontent)
  nflex = nflex.strip()
  return nflex

'''
"footer": {
  "type": "box",
  "layout": "horizontal",
  "contents": [
    {
      "type": "button",
      "action": {
        "type": "uri",
        "label": "More",
        "uri": "https://linecorp.com"
      }
    }
  ]
}
'''
# a = generate_news_flex(nimg,nheader,ncontent)
# print(nimg)

def create_news_flex():
  url = "https://news-botnoi-api.herokuapp.com/news?category=sports"
  res = requests.get(url).json()
  res = res[::-1][0:10]
  
  bubbleList = ''
  for i in range(len(res)):
    print(i)
    firstnews = res[i]
    ncontent = firstnews['Detail'].replace('"','')
    nheader = firstnews['Header'].replace('"','')
    nimage = firstnews['photolink'].replace('"','')
    print(nimage)
    if nimage == 'nonePhoto':
      nimage = 'https://www.zambianobserver.com/wp-content/uploads/2016/08/sportnews-e1470828995760.jpg'
    flexmsg = generate_news_flex(nimage,nheader,ncontent)
    #return flexmsg
    bubbleList = bubbleList+flexmsg+','
  bubbleList = bubbleList[0:-1]
  flexmsg = '''{
    "type": "carousel",
    "contents":[%s]
    }
  '''%bubbleList

  flexmsg = json.loads(flexmsg)
  flexobj = FlexSendMessage('alttext',flexmsg)
  return flexobj
a = create_news_flex()
print(a)
  #userId = 'Ue8dfc92bf6d5249f02c82147e2432ffb'
  #line_bot_api.push_message(userId,flexobj)
  #return flexobj
  #return ncontent,nheader,nimage




