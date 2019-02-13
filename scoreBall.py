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
    apiScoreBall = ('https://scrape-score-ball.herokuapp.com/scoreball?homeTeam=Alaves')
   
   
    homeTeamScoreBalls = requests.get(apiScoreBall).json()
   
    carousel_container = CarouselContainer()
    # T = new_eng
    # H = tablelLeague
    if 'B' in event.message.text:
        for homeTeamScoreBall in homeTeamScoreBalls:
            awayTeam = homeTeamScoreBall['match']['awayTeam']
            dateTime = homeTeamScoreBall['match']['dateTime']
            haveRedCardAway = homeTeamScoreBall['match']['haveRedCardAway']
            haveRedCardHome = homeTeamScoreBall['match']['haveRedCardHome']
            haveYellowCardAway = homeTeamScoreBall['match']['haveYellowCardAway']
            haveYellowCardHome = homeTeamScoreBall['match']['haveYellowCardHome']
            homeTeam = homeTeamScoreBall['match']['homeTeam']
            league = homeTeamScoreBall['match']['league']
            penalty = homeTeamScoreBall['match']['penalty']
            playerRedCardHome = homeTeamScoreBall['match']['playerRedCardHome']
            playerScoreAway = homeTeamScoreBall['match']['playerScoreAway']
            playerScoreHome = homeTeamScoreBall['match']['playerScoreHome']
            playerYellowCardAway = homeTeamScoreBall['match']['playerYellowCardAway']
            playerYellowCardHomes = homeTeamScoreBall['match']['playerYellowCardHome']
            redCardAway = homeTeamScoreBall['match']['redCardAway']
            teamAwayScore = homeTeamScoreBall['match']['teamAwayScore']
            teamHomeScore = homeTeamScoreBall['match']['teamHomeScore']
            teamVsAway = homeTeamScoreBall['match']['teamVsAway']
            timeStatus = homeTeamScoreBall['match']['timeStatus']
            print("----------------------------------------------")
            print("awayTeam:",awayTeam)
            print("dateTime:",dateTime)
            print("haveRedCardAway:",haveRedCardAway)
            print("haveRedCardHome:",haveRedCardHome)
            print("haveYellowCardAway:",haveYellowCardAway)
            print("haveYellowCardHome:",haveYellowCardHome)
            print("homeTeam:",homeTeam)
            print("league:",league)
            print("penalty:",penalty)
            print("playerRedCardHome:",playerRedCardHome)
            print("playerScoreAway:",playerScoreAway)
            print("playerScoreHome:",playerScoreHome)
            print("playerYellowCardAway:",playerYellowCardAway)
            print("playerYellowCardHome:",playerYellowCardHomes)
                
            print("redCardAway:",redCardAway)
            print("teamAwayScore:",teamAwayScore)
            print("teamHomeScore:",teamHomeScore)
            print("teamVsAway:",teamVsAway)
            print("timeStatus:",timeStatus)
            print("----------------------------------------------")
            commonentRedCard = """
,
          {
            "type": "box",
            "layout": "baseline",
            "spacing": "sm",
            "contents": [
              {
                "type": "text",
                "text": "40'",
                "color": "#aaaaaa",
                "size": "sm",
                "flex": 1
              },
              {
                "type": "icon",
                "url": "https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gold_star_28.png",
                "size": "sm"
              },
              {
                "type": "text",
                "text": "test player",
                "wrap": true,
                "color": "#666666",
                "size": "sm",
                "flex": 4
              }
            ]
          }            
            """
            
            componentYellowCard = """
,
          {
            "type": "box",
            "layout": "baseline",
            "spacing": "sm",
            "contents": [
              {
                "type": "text",
                "text": "40'",
                "color": "#aaaaaa",
                "size": "sm",
                "flex": 1
              },
              {
                "type": "icon",
                "url": "https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gold_star_28.png",
                "size": "sm"
              },
              {
                "type": "text",
                "text": "test player yellow",
                "wrap": true,
                "color": "#666666",
                "size": "sm",
                "flex": 4
              }
            ]
          }
            """
            componentScore ="""
,
          {
            "type": "box",
            "layout": "baseline",
            "spacing": "sm",
            "contents": [
              {
                "type": "text",
                "text": "4'",
                "color": "#aaaaaa",
                "size": "sm",
                "flex": 1
              },
              {
                "type": "text",
                "text": "1 - 0",
                "wrap": true,
                "color": "#666666",
                "size": "sm",
                "flex": 1
              },
              {
                "type": "icon",
                "url": "https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gold_star_28.png",
                "size": "sm"
              },
              {
                "type": "text",
                "text": "C.  Cristiano Ronaldo",
                "wrap": true,
                "color": "#666666",
                "size": "sm",
                "flex": 4
              }
            ]
          }
            """
            newsEng = """
{
  "type": "bubble",
  "body": {
    "type": "box",
    "layout": "vertical",
    "spacing": "md",
    "contents": [
      {
        "type": "text",
        "text": "%s",
        "wrap": true,
        "weight": "bold",
        "gravity": "center",
        "size": "lg"
      },
      {
        "type": "box",
        "layout": "baseline",
        "spacing": "sm",
        "contents": [
          {
            "type": "text",
            "text": "%s",
            "flex": 5,
            "align": "start"
          },
          {
            "type": "text",
            "text": "%s : %s",
            "flex": 2,
            "align": "center"
          },
          {
            "type": "text",
            "text": "%s",
            "flex": 5,
            "align": "end"
          }
        ]
      },
      {
        "type": "separator",
        "margin": "xxl"
      },
      {
        "type": "box",
        "layout": "vertical",
        "margin": "lg",
        "spacing": "sm",
        "contents": [
          {
            "type": "box",
            "layout": "baseline",
            "spacing": "sm",
            "contents": [
              {
                "type": "text",
                "text": "Scorer",
                "color": "#aaaaaa",
                "size": "sm",
                "weight": "bold"
              }
            ]
          }%s,
          {
            "type": "box",
            "layout": "baseline",
            "spacing": "sm",
            "contents": [
              {
                "type": "text",
                "text": "Yellow Card",
                "color": "#aaaaaa",
                "size": "sm",
                "weight": "bold"
              }
            ]
          }%s,
          {
            "type": "box",
            "layout": "baseline",
            "spacing": "sm",
            "contents": [
              {
                "type": "text",
                "text": "Red Card",
                "color": "#aaaaaa",
                "size": "sm",
                "weight": "bold"
              }
            ]
          }%s
        ]
      }
    ]
  },
  "footer": {
    "type": "box",
    "layout": "vertical",
    "contents": [
      {
        "type": "separator",
        "margin": "xxl"
      },
      {
        "type": "box",
        "layout": "baseline",
        "margin": "md",
        "contents": [
          {
            "type": "text",
            "text": "league",
            "color": "#aaaaaa",
            "size": "sm",
            "flex": 2
          },
          {
            "type": "text",
            "text": "%s",
            "wrap": true,
            "color": "#666666",
            "size": "sm",
            "flex": 4
          }
        ]
      },
      {
        "type": "box",
        "layout": "baseline",
        "spacing": "sm",
        "contents": [
          {
            "type": "text",
            "text": "Date",
            "color": "#aaaaaa",
            "size": "sm",
            "flex": 2
          },
          {
            "type": "text",
            "text": "%s",
            "wrap": true,
            "size": "sm",
            "color": "#666666",
            "flex": 4
          }
        ]
      }
    ]
  }
}
            """%(timeStatus,homeTeam,teamHomeScore,teamAwayScore,awayTeam,componentScore,componentYellowCard,commonentRedCard,league,dateTime)
            # %(league,timeStatus,homeTeam,teamHomeScore,teamAwayScore,awayTeam)
            newsEng = json.loads(newsEng)
            carousel_container.contents.append(newsEng)
            # seeMorePageNewEng = '''{"type":"bubble","body":{"type":"box","layout":"vertical","spacing":"sm","contents":[{"type":"button","flex":1,"gravity":"center","action":{"type":"uri","label":"See more","uri":"https://linecorp.com"}}]}}'''
            # seeMorePageNewEng = json.loads(seeMorePageNewEng)
            # carousel_container.contents.append(seeMorePageNewEng)
            line_bot_api.reply_message(event.reply_token, FlexSendMessage(alt_text='Fixtures', contents=carousel_container))
            # print("print message is:",event.message.text)
            # print("---------------success News Eng---------------")

    else:
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=event.message.text))

    
if __name__ == '__main__':
    app.run(debug=True, port=80)