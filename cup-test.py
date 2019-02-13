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
# listGroupAllLeague = ['GroupA','GroupB','GroupC','GroupD','GroupE','GroupF','GroupG','GroupH','GroupI','GroupJ','GroupK','GroupL']



listRankTopPage = []
listGameplayTopPage = []
listWinsTopPage = []
listDrawsTopPage = []
listLossesTopPage = []
listPointTopPage = []
listTeamTopPage = []

listRankBottomPage = []
listGameplayBottomPage = []
listWinsBottomPage = []
listDrawsBottomPage = []
listLossesBottomPage = []
listPointBottomPage = []
listTeamBottomPage = []
listAllButtom = []


teamGroupOneTop = []
RankGroupOneTop = []
GamePlayGroupOneTop = []
winsGroupOneTop = []
drawGroupOneTop = []
lossesGroupOneTop = []
pointGroupOneTop = []

teamGroupTwoTop = []
RankGroupTwoTop = []
GamePlayGroupTwoTop = []
winsGroupTwoTop = []
drawGroupTwoTop = []
lossesGroupTwoTop = []
pointGroupTwoTop = []

teamGroupThreeTop = []
RankGroupThreeTop = []
GamePlayGroupThreeTop = []
winsGroupThreeTop = []
drawGroupThreeTop = []
lossesGroupThreeTop = []
pointGroupThreeTop = []

teamGroupFourTop = []
RankGroupFourTop = []
GamePlayGroupFourTop = []
winsGroupFourTop = []
drawGroupFourTop = []
lossesGroupFourTop = []
pointGroupFourTop = []


teamGroupOne = []
RankGroupOne = []
GamePlayGroupOne = []
winsGroupOne = []
drawGroupOne = []
lossesGroupOne = []
pointGroupOne = []

teamGroupTwo = []
RankGroupTwo = []
GamePlayGroupTwo = []
winsGroupTwo = []
drawGroupTwo = []
lossesGroupTwo = []
pointGroupTwo = []

teamGroupThree = []
RankGroupThree = []
GamePlayGroupThree = []
winsGroupThree = []
drawGroupThree = []
lossesGroupThree = []
pointGroupThree = []

teamGroupFour = []
RankGroupFour = []
GamePlayGroupFour = []
winsGroupFour = []
drawGroupFour = []
lossesGroupFour = []
pointGroupFour = []


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    carousel_container = CarouselContainer()
    if event.message.text[:4] == 'Cup ':
        splitLeagueCup = event.message.text.split(" ")
        categoryCup = splitLeagueCup[1]
        apiNameLeague = ('https://scrape-football-cup.herokuapp.com/cup?leagueName={}').format(categoryCup)
        allDataLinkCup = requests.get(apiNameLeague).json()
        listGroup = allDataLinkCup[0]
        if categoryCup in 'AFC-Asian-Cup':
            listTopPage = ['GroupA','GroupC','GroupE']
            lengthGroupTop = len(listTopPage)
            print(lengthGroupTop)
            listButtomPage = ['GroupB','GroupD','GroupF']
            lengthGroupBottom = len(listButtomPage)

        elif categoryCup in 'UEFA-Champions-League':
            listTopPage = ['GroupA','GroupC','GroupE','GroupG']
            lengthGroupTop = len(listTopPage)
            print(lengthGroupTop)
            listButtomPage = ['GroupB','GroupD','GroupF','GroupH']
            lengthGroupBottom = len(listButtomPage)
        elif categoryCup in 'UEFA-Europa-League' or 'African-Nations-Cup-Qualifying':      
            listTopPage = ['GroupA','GroupC','GroupE','GroupG','GroupI','GroupK']
            lengthGroupTop = len(listTopPage)
            print(lengthGroupTop)
            listButtomPage = ['GroupB','GroupD','GroupF','GroupH','GroupJ','GroupL']
            lengthGroupBottom = len(listButtomPage)

        

        for elementGroup in range(0,lengthGroupTop):
            for elementRank in range(1,5):
                GameplayTopPage = listGroup[listTopPage[elementGroup]]['{}'.format(elementRank)]['Gameplay']
                WinsTopPage = listGroup[listTopPage[elementGroup]]['{}'.format(elementRank)]['Wins']
                DrawsTopPage = listGroup[listTopPage[elementGroup]]['{}'.format(elementRank)]['Draws']
                LossesTopPage = listGroup[listTopPage[elementGroup]]['{}'.format(elementRank)]['Losses']
                pointTopPage = listGroup[listTopPage[elementGroup]]['{}'.format(elementRank)]['point']
                TeamTopPage = listGroup[listTopPage[elementGroup]]['{}'.format(elementRank)]['team_name']
                listRankTopPage.append(elementRank)
                listGameplayTopPage.append(GameplayTopPage)
                listWinsTopPage.append(WinsTopPage)
                listDrawsTopPage.append(DrawsTopPage)
                listLossesTopPage.append(LossesTopPage)
                listPointTopPage.append(pointTopPage)
                listTeamTopPage.append(TeamTopPage)

                GameplayBottomPage = listGroup[listButtomPage[elementGroup]]['{}'.format(elementRank)]['Gameplay']
                WinsBottomPage = listGroup[listButtomPage[elementGroup]]['{}'.format(elementRank)]['Wins']
                DrawsBottomPage = listGroup[listButtomPage[elementGroup]]['{}'.format(elementRank)]['Draws']
                LossesBottomPage = listGroup[listButtomPage[elementGroup]]['{}'.format(elementRank)]['Losses']
                pointBottomPage = listGroup[listButtomPage[elementGroup]]['{}'.format(elementRank)]['point']
                TeamBottomPage = listGroup[listButtomPage[elementGroup]]['{}'.format(elementRank)]['team_name']
                listRankBottomPage.append(elementRank)
                listGameplayBottomPage.append(GameplayBottomPage)
                listWinsBottomPage.append(WinsBottomPage)
                listDrawsBottomPage.append(DrawsBottomPage)
                listLossesBottomPage.append(LossesBottomPage)
                listPointBottomPage.append(pointBottomPage)
                listTeamBottomPage.append(TeamBottomPage)

                lengthTeamAllBottom = len(listTeamBottomPage)    
        
        for elementTeamBottom in range(0,lengthTeamAllBottom):
            allDataRankTop = listRankTopPage[elementTeamBottom]
            allDataGamePlayTop = listGameplayTopPage[elementTeamBottom]
            allDataWinsTop = listWinsTopPage[elementTeamBottom]
            allDataDrawsTop = listDrawsTopPage[elementTeamBottom]
            allDataLossesTop = listLossesTopPage[elementTeamBottom]
            allDataPointTop = listPointTopPage[elementTeamBottom]
            allDataTeamTop = listTeamTopPage[elementTeamBottom]

            allDataRankBottom = listRankBottomPage[elementTeamBottom]
            allDataGamePlayBottom = listGameplayBottomPage[elementTeamBottom]
            allDataWinsBottom = listWinsBottomPage[elementTeamBottom]
            allDataDrawsBottom = listDrawsBottomPage[elementTeamBottom]
            allDataLossesBottom = listLossesBottomPage[elementTeamBottom]
            allDataPointBottom = listPointBottomPage[elementTeamBottom]

            allDataTeamBottom = listTeamBottomPage[elementTeamBottom]
            if elementTeamBottom % 4 == 0:
                teamGroupOneTop.append(allDataTeamTop)
                RankGroupOneTop.append(allDataRankTop)
                GamePlayGroupOneTop.append(allDataGamePlayTop)
                winsGroupOneTop.append(allDataWinsTop)
                drawGroupOneTop.append(allDataDrawsTop)
                lossesGroupOneTop.append(allDataLossesTop)
                pointGroupOneTop.append(allDataPointTop)
            
                teamGroupOne.append(allDataTeamBottom)
                RankGroupOne.append(allDataRankBottom)
                GamePlayGroupOne.append(allDataGamePlayBottom)
                winsGroupOne.append(allDataWinsBottom)
                drawGroupOne.append(allDataDrawsBottom)
                lossesGroupOne.append(allDataLossesBottom)
                pointGroupOne.append(allDataPointBottom)
            elif elementTeamBottom % 4 == 1:
                teamGroupTwoTop.append(allDataTeamTop)
                RankGroupTwoTop.append(allDataRankTop)
                GamePlayGroupTwoTop.append(allDataGamePlayTop)
                winsGroupTwoTop.append(allDataWinsTop)
                drawGroupTwoTop.append(allDataDrawsTop)
                lossesGroupTwoTop.append(allDataLossesTop)
                pointGroupTwoTop.append(allDataPointTop)

                teamGroupTwo.append(allDataTeamBottom)
                RankGroupTwo.append(allDataRankBottom)
                GamePlayGroupTwo.append(allDataGamePlayBottom)
                winsGroupTwo.append(allDataWinsBottom)
                drawGroupTwo.append(allDataDrawsBottom)
                lossesGroupTwo.append(allDataLossesBottom)
                pointGroupTwo.append(allDataPointBottom)
            elif elementTeamBottom % 4 == 2:
                teamGroupThreeTop.append(allDataTeamTop)
                RankGroupThreeTop.append(allDataRankTop)
                GamePlayGroupThreeTop.append(allDataGamePlayTop)
                winsGroupThreeTop.append(allDataWinsTop)
                drawGroupThreeTop.append(allDataDrawsTop)
                lossesGroupThreeTop.append(allDataLossesTop)
                pointGroupThreeTop.append(allDataPointTop)


                teamGroupThree.append(allDataTeamBottom)
                RankGroupThree.append(allDataRankBottom)
                GamePlayGroupThree.append(allDataGamePlayBottom)
                winsGroupThree.append(allDataWinsBottom)
                drawGroupThree.append(allDataDrawsBottom)
                lossesGroupThree.append(allDataLossesBottom)
                pointGroupThree.append(allDataPointBottom)
            elif elementTeamBottom % 4 == 3:
                teamGroupFourTop.append(allDataTeamTop)
                RankGroupFourTop.append(allDataRankTop)
                GamePlayGroupFourTop.append(allDataGamePlayTop)
                winsGroupFourTop.append(allDataWinsTop)
                drawGroupFourTop.append(allDataDrawsTop)
                lossesGroupFourTop.append(allDataLossesTop)
                pointGroupFourTop.append(allDataPointTop)

                teamGroupFour.append(allDataTeamBottom)
                RankGroupFour.append(allDataRankBottom)
                GamePlayGroupFour.append(allDataGamePlayBottom)
                winsGroupFour.append(allDataWinsBottom)
                drawGroupFour.append(allDataDrawsBottom)
                lossesGroupFour.append(allDataLossesBottom)
                pointGroupFour.append(allDataPointBottom)
        for elementBubble in range(0,lengthGroupBottom):
    
            tableGroupTop = '''{"type":"bubble","styles":{"header":{"backgroundColor":"#c70039"}},"header":{"type":"box","layout":"horizontal","contents":[{"type":"text","text":"%s","color":"#FFFFFF","size":"lg"}]},"body":{"type":"box","layout":"vertical","contents":[{"type":"box","layout":"vertical","margin":"xxl","spacing":"sm","contents":[{"type":"text","text":"%s","size":"lg"},{"type":"separator","margin":"sm"},{"type":"box","layout":"horizontal","contents":[{"type":"text","text":"#","weight":"bold","flex":1,"gravity":"center"},{"type":"text","text":"Team","weight":"bold","flex":5,"gravity":"center"},{"type":"text","weight":"bold","text":"P","flex":1,"gravity":"center"},{"type":"text","weight":"bold","text":"W","flex":1,"gravity":"center"},{"type":"text","weight":"bold","text":"D","flex":1,"gravity":"center"},{"type":"text","weight":"bold","text":"L","flex":1,"gravity":"center"},{"type":"text","weight":"bold","text":"Pt","flex":1,"gravity":"center"}]},{"type":"separator","margin":"sm"},{"type":"box","layout":"horizontal","contents":[{"type":"text","text":"%s","flex":1,"gravity":"center"},{"type":"text","text":"%s","flex":5,"gravity":"center"},{"type":"text","text":"%s","flex":1,"gravity":"center"},{"type":"text","text":"%s","flex":1,"gravity":"center"},{"type":"text","text":"%s","flex":1,"gravity":"center"},{"type":"text","text":"%s","flex":1,"gravity":"center"},{"type":"text","text":"%s","flex":1,"gravity":"center"}]},{"type":"box","layout":"horizontal","contents":[{"type":"text","text":"%s","flex":1,"gravity":"center"},{"type":"text","text":"%s","flex":5,"gravity":"center"},{"type":"text","text":"%s","flex":1,"gravity":"center"},{"type":"text","text":"%s","flex":1,"gravity":"center"},{"type":"text","text":"%s","flex":1,"gravity":"center"},{"type":"text","text":"%s","flex":1,"gravity":"center"},{"type":"text","text":"%s","flex":1,"gravity":"center"}]},{"type":"box","layout":"horizontal","contents":[{"type":"text","text":"%s","flex":1,"gravity":"center"},{"type":"text","text":"%s","flex":5,"gravity":"center"},{"type":"text","text":"%s","flex":1,"gravity":"center"},{"type":"text","text":"%s","flex":1,"gravity":"center"},{"type":"text","text":"%s","flex":1,"gravity":"center"},{"type":"text","text":"%s","flex":1,"gravity":"center"},{"type":"text","text":"%s","flex":1,"gravity":"center"}]},{"type":"box","layout":"horizontal","contents":[{"type":"text","text":"%s","flex":1,"gravity":"center"},{"type":"text","text":"%s","flex":5,"gravity":"center"},{"type":"text","text":"%s","flex":1,"gravity":"center"},{"type":"text","text":"%s","flex":1,"gravity":"center"},{"type":"text","text":"%s","flex":1,"gravity":"center"},{"type":"text","text":"%s","flex":1,"gravity":"center"},{"type":"text","text":"%s","flex":1,"gravity":"center"}]}]},{"type":"separator","margin":"xl"},{"type":"box","layout":"vertical","margin":"xxl","spacing":"sm","contents":[{"type":"text","text":"%s","size":"lg"},{"type":"separator","margin":"sm"},{"type":"box","layout":"horizontal","contents":[{"type":"text","text":"#","weight":"bold","flex":1,"gravity":"center"},{"type":"text","text":"Team","weight":"bold","flex":5,"gravity":"center"},{"type":"text","weight":"bold","text":"P","flex":1,"gravity":"center"},{"type":"text","weight":"bold","text":"W","flex":1,"gravity":"center"},{"type":"text","weight":"bold","text":"D","flex":1,"gravity":"center"},{"type":"text","weight":"bold","text":"L","flex":1,"gravity":"center"},{"type":"text","weight":"bold","text":"Pt","flex":1,"gravity":"center"}]},{"type":"separator","margin":"sm"},{"type":"box","layout":"horizontal","contents":[{"type":"text","text":"%s","flex":1,"gravity":"center"},{"type":"text","text":"%s","flex":5,"gravity":"center"},{"type":"text","text":"%s","flex":1,"gravity":"center"},{"type":"text","text":"%s","flex":1,"gravity":"center"},{"type":"text","text":"%s","flex":1,"gravity":"center"},{"type":"text","text":"%s","flex":1,"gravity":"center"},{"type":"text","text":"%s","flex":1,"gravity":"center"}]},{"type":"box","layout":"horizontal","contents":[{"type":"text","text":"%s","flex":1,"gravity":"center"},{"type":"text","text":"%s","flex":5,"gravity":"center"},{"type":"text","text":"%s","flex":1,"gravity":"center"},{"type":"text","text":"%s","flex":1,"gravity":"center"},{"type":"text","text":"%s","flex":1,"gravity":"center"},{"type":"text","text":"%s","flex":1,"gravity":"center"},{"type":"text","text":"%s","flex":1,"gravity":"center"}]},{"type":"box","layout":"horizontal","contents":[{"type":"text","text":"%s","flex":1,"gravity":"center"},{"type":"text","text":"%s","flex":5,"gravity":"center"},{"type":"text","text":"%s","flex":1,"gravity":"center"},{"type":"text","text":"%s","flex":1,"gravity":"center"},{"type":"text","text":"%s","flex":1,"gravity":"center"},{"type":"text","text":"%s","flex":1,"gravity":"center"},{"type":"text","text":"%s","flex":1,"gravity":"center"}]},{"type":"box","layout":"horizontal","contents":[{"type":"text","text":"%s","flex":1,"gravity":"center"},{"type":"text","text":"%s","flex":5,"gravity":"center"},{"type":"text","text":"%s","flex":1,"gravity":"center"},{"type":"text","text":"%s","flex":1,"gravity":"center"},{"type":"text","text":"%s","flex":1,"gravity":"center"},{"type":"text","text":"%s","flex":1,"gravity":"center"},{"type":"text","text":"%s","flex":1,"gravity":"center"}]}]}]}}'''%(categoryCup,listTopPage[elementBubble],RankGroupOneTop[elementBubble],teamGroupOneTop[elementBubble],GamePlayGroupOneTop[elementBubble],winsGroupOneTop[elementBubble],drawGroupOneTop[elementBubble],lossesGroupOneTop[elementBubble],pointGroupOneTop[elementBubble],            
            RankGroupTwoTop[elementBubble],teamGroupTwoTop[elementBubble],GamePlayGroupTwoTop[elementBubble],winsGroupTwoTop[elementBubble],drawGroupTwoTop[elementBubble],lossesGroupTwoTop[elementBubble],pointGroupTwoTop[elementBubble],
            RankGroupThreeTop[elementBubble],teamGroupThreeTop[elementBubble],GamePlayGroupThreeTop[elementBubble],winsGroupThreeTop[elementBubble],drawGroupThreeTop[elementBubble],lossesGroupThreeTop[elementBubble],pointGroupThreeTop[elementBubble],
            RankGroupFourTop[elementBubble],teamGroupFourTop[elementBubble],GamePlayGroupFourTop[elementBubble],winsGroupFourTop[elementBubble],drawGroupFourTop[elementBubble],lossesGroupFourTop[elementBubble],pointGroupFourTop[elementBubble],            
            listButtomPage[elementBubble],RankGroupOne[elementBubble],teamGroupOne[elementBubble],GamePlayGroupOne[elementBubble],winsGroupOne[elementBubble],drawGroupOne[elementBubble],lossesGroupOne[elementBubble],pointGroupOne[elementBubble],
            RankGroupTwo[elementBubble],teamGroupTwo[elementBubble],GamePlayGroupTwo[elementBubble],winsGroupTwo[elementBubble],drawGroupTwo[elementBubble],lossesGroupTwo[elementBubble],pointGroupTwo[elementBubble],
            RankGroupThree[elementBubble],teamGroupThree[elementBubble],GamePlayGroupThree[elementBubble],winsGroupThree[elementBubble],drawGroupThree[elementBubble],lossesGroupThree[elementBubble],pointGroupThree[elementBubble],
            RankGroupFour[elementBubble],teamGroupFour[elementBubble],GamePlayGroupFour[elementBubble],winsGroupFour[elementBubble],drawGroupFour[elementBubble],lossesGroupFour[elementBubble],pointGroupFour[elementBubble])
            tableGroupTop = json.loads(tableGroupTop)
            carousel_container.contents.append(tableGroupTop)
        # del teamGroupOneTop[:]
        del listRankTopPage[:]
        del listGameplayTopPage[:]
        del listWinsTopPage[:]
        del listDrawsTopPage[:]
        del listLossesTopPage[:]
        del listPointTopPage[:]
        del listTeamTopPage[:]
        del listRankBottomPage[:]
        del listGameplayBottomPage[:]
        del listWinsBottomPage[:]
        del listDrawsBottomPage[:]
        del listLossesBottomPage[:]
        del listPointBottomPage[:]
        del listTeamBottomPage[:]



        

        del RankGroupOneTop[:]
        del teamGroupOneTop[:]
        del GamePlayGroupOneTop[:]
        del winsGroupOneTop[:]
        del drawGroupOneTop[:]
        del lossesGroupOneTop[:]
        del pointGroupOneTop[:]
        del RankGroupTwoTop[:]
        del teamGroupTwoTop[:]
        del GamePlayGroupTwoTop[:]
        del winsGroupTwoTop[:]
        del drawGroupTwoTop[:]
        del lossesGroupTwoTop[:]
        del pointGroupTwoTop[:]
        del RankGroupThreeTop[:]
        del teamGroupThreeTop[:]
        del GamePlayGroupThreeTop[:]
        del winsGroupThreeTop[:]
        del drawGroupThreeTop[:]
        del lossesGroupThreeTop[:]
        del pointGroupThreeTop[:]
        del RankGroupFourTop[:]
        del teamGroupFourTop[:]
        del GamePlayGroupFourTop[:]
        del winsGroupFourTop[:]
        del drawGroupFourTop[:]
        del lossesGroupFourTop[:]
        del pointGroupFourTop[:]        
        del listButtomPage[:]
        del RankGroupOne[:]
        del teamGroupOne[:]
        del GamePlayGroupOne[:]
        del winsGroupOne[:]
        del drawGroupOne[:]
        del lossesGroupOne[:]
        del pointGroupOne[:]
        del RankGroupTwo[:]
        del teamGroupTwo[:]
        del GamePlayGroupTwo[:]
        del winsGroupTwo[:]
        del drawGroupTwo[:]
        del lossesGroupTwo[:]
        del pointGroupTwo[:]
        del RankGroupThree[:]
        del teamGroupThree[:]
        del GamePlayGroupThree[:]
        del winsGroupThree[:]
        del drawGroupThree[:]
        del lossesGroupThree[:]
        del pointGroupThree[:]
        del RankGroupFour[:]
        del teamGroupFour[:]
        del GamePlayGroupFour[:]
        del winsGroupFour[:]
        del drawGroupFour[:]
        del lossesGroupFour[:]
        del pointGroupFour[:]
        # del listTopPage[:]
        # del listButtomPage[:]
        # print(listRankTopPage)
    
    # else:
    #     line_bot_api.reply_message(event.reply_token, TextSendMessage(text=event.message.text))
    
        
    line_bot_api.reply_message(event.reply_token, FlexSendMessage(alt_text='Fixtures', contents=carousel_container))
if __name__ == '__main__':
    app.run(debug=True, port=80)