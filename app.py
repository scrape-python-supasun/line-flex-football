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
# import test_news_eng
# class Zone(tzinfo):
#     def __init__(self,offset,isdst,name):
#         self.offset = offset
#         self.isdst = isdst
#         self.name = name
#     def utcoffset(self, dt):
#         return timedelta(hours=self.offset) + self.dst(dt)
#     def dst(self, dt):
#             return timedelta(hours=1) if self.isdst else timedelta(0)
#     def tzname(self,dt):
#          return self.name
# datetimeUtc = datetime.utcnow().strftime('%d/%m/%Y')
# # datetimeUtc = datetime.utcnow().strftime('%Y/%m/%d')


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
    if event.message.text[:11] == 'ขอข้อมูลบอล':
        bubble = BubbleContainer(
            direction='ltr',
            hero=ImageComponent(
                url='https://www.928betwin.com/wp-content/uploads/2017/03/%E0%B8%A3%E0%B8%B2%E0%B8%84%E0%B8%B2%E0%B8%9A%E0%B8%AD%E0%B8%A5%E0%B8%95%E0%B9%88%E0%B8%AD.jpg',
                size='full',
                aspect_ratio='20:13',
                aspect_mode='cover',
                action=URIAction(uri='http://example.com', label='label')
            ),
            body=BoxComponent(
                layout='vertical',
                contents=[
                    TextComponent(text='news football all', weight='bold', size='xl'),
                ],
            ),
            footer=BoxComponent(
                layout='vertical',
                spacing='sm',
                contents=[
                    SpacerComponent(size='sm'),
                    ButtonComponent(
                        style='primary',
                        height='sm',
                        action=MessageAction(label='Score Ball', text='ScoreBallLeagueAll'),
                    ),
                    ButtonComponent(
                        style='primary',
                        height='sm',
                        action=MessageAction(label='Table League', text='allTableLeague'),
                    ),
                    ButtonComponent(
                        style='primary',
                        height='sm',
                        action=MessageAction(label='Cup All', text='CupAll'),
                    ),
                    ButtonComponent(
                        style='primary',
                        height='sm',
                        action=MessageAction(label='news', text='NewsAll'),
                    )
                ]
            ),
        )
        message = FlexSendMessage(alt_text="hello", contents=bubble)
        line_bot_api.reply_message(
            event.reply_token,
            message
        )
        # (--------------------------------------------------button Score Ball-------------------------------------------------)\
    elif event.message.text[:18] == 'ScoreBallLeagueAll':
        apiScoreBall = ('https://scrape-score-ball.herokuapp.com/')
        homeTeamScoreBalls = requests.get(apiScoreBall).json()
        buttons = []
        texts = []
        listLeagueTeam = []
        notDeplicates = []
        for homeTeamScoreBall in homeTeamScoreBalls:
            awayTeam = homeTeamScoreBall['match']['awayTeam']
            homeTeam = homeTeamScoreBall['match']['homeTeam']
            leagueTeam = homeTeamScoreBall['match']['league']
            listLeagueTeam.append(leagueTeam)
        # ----------------------------------------------
        for element in listLeagueTeam:
            if element not in notDeplicates:
                notDeplicates.append(element)
        for leagueAll in notDeplicates:
            print(leagueAll)
            buttons.append(
                ButtonComponent(layout='horizontal',
                            style='primary', 
                            height='sm',
                            action=MessageAction(label=f'{leagueAll}', text=f'League {leagueAll}')
                ),
            )
        bubble = BubbleContainer(
            direction='ltr',
            hero=ImageComponent(
                url='https://www.928betwin.com/wp-content/uploads/2017/03/%E0%B8%A3%E0%B8%B2%E0%B8%84%E0%B8%B2%E0%B8%9A%E0%B8%AD%E0%B8%A5%E0%B8%95%E0%B9%88%E0%B8%AD.jpg',
                size='full',
                aspect_ratio='20:13',
                aspect_mode='cover',
                action=URIAction(uri='http://example.com', label='label')
            ),
            body=BoxComponent(
                layout='vertical',
                align='start',
                contents=[
                    TextComponent(text='name league:', weight='bold', size='xl'),
                ],
            ),
            footer=BoxComponent(
                layout='vertical',
                spacing='sm',

                contents=buttons
            ),
        )
        message = FlexSendMessage(alt_text="score-ball", contents=bubble)
        line_bot_api.reply_message(
            event.reply_token,
            message
        )

    elif event.message.text[:7] == 'League ':
        splitLeague = event.message.text.split('League ')
        splitLeagueTrue = splitLeague[1]
        print('splitLeagueTrue',splitLeagueTrue)
        apiScoreLeagueBall = ('https://scrape-score-ball.herokuapp.com/scoreball?league={}').format(splitLeagueTrue)
        print('apiScoreLeagueBall',apiScoreLeagueBall)
        leagueScoreBalls = requests.get(apiScoreLeagueBall).json()
        buttons = []
        for leagueScoreBall in leagueScoreBalls:
            awayTeam = leagueScoreBall['match']['awayTeam']
            homeTeam = leagueScoreBall['match']['homeTeam']
            # leagueTeam = leagueScoreBall['match']['league']

            print('awayTeam',awayTeam)
            print('homeTeam',homeTeam)
            # print('leagueTeam',leagueTeam)
            buttons.append(
                ButtonComponent(layout='horizontal',
                            style='primary', 
                            height='sm',
                            action=MessageAction(label=f'{homeTeam} vs {awayTeam}', text=f'Team {homeTeam}')
                ),
            )
        bubble = BubbleContainer(
            direction='ltr',
            hero=ImageComponent(
                url='https://www.928betwin.com/wp-content/uploads/2017/03/%E0%B8%A3%E0%B8%B2%E0%B8%84%E0%B8%B2%E0%B8%9A%E0%B8%AD%E0%B8%A5%E0%B8%95%E0%B9%88%E0%B8%AD.jpg',
                size='full',
                aspect_ratio='20:13',
                aspect_mode='cover',
                action=URIAction(uri='http://example.com', label='label')
            ),
            body=BoxComponent(
                layout='vertical',
                align='start',
                contents=[
                    TextComponent(text='name team:', weight='bold', size='xl'),
                ],
            ),
            footer=BoxComponent(
                layout='vertical',
                spacing='sm',

                contents=buttons
            ),
        )
        message = FlexSendMessage(alt_text="score-ball", contents=bubble)
        line_bot_api.reply_message(
            event.reply_token,
            message
        )


        # (--------------------------------------------------scoreball-------------------------------------------------)
    elif event.message.text[:5] == 'Team ':
        splitTeamLink = event.message.text.split('Team ')[1]
        print(splitTeamLink)
        apiScoreBall = ('https://scrape-score-ball.herokuapp.com/scoreball?homeTeam={}').format(splitTeamLink)
        homeTeamScoreBalls = requests.get(apiScoreBall).json()
        # print(homeTeamScoreBalls)
        carousel_container = CarouselContainer()
        listAllPlayer = []
        listAllTime = []
        for homeTeamScoreBall in homeTeamScoreBalls:
            awayTeam = homeTeamScoreBall['match']['awayTeam']
            dateTime = homeTeamScoreBall['match']['dateTime']
            homeTeam = homeTeamScoreBall['match']['homeTeam']
            league = homeTeamScoreBall['match']['league']
            penalty = homeTeamScoreBall['match']['penalty']
            timeStatus = homeTeamScoreBall['match']['timeStatus']
            playerRedCardHomes = homeTeamScoreBall['match']['playerRedCardHome']

        if playerRedCardHomes == None:
            HaveRedCardHome = None

        else:
            listNamePlayerRedCardHome = []
            listTimePlayerRedCardHome = []
            for playerRedCardHome in playerRedCardHomes:
                splitPlayerRedCardHome = playerRedCardHome.split("), ")
                lengthSplitPlayerRedCardHome = len(splitPlayerRedCardHome)
            for elementRedCardHome in range(0,lengthSplitPlayerRedCardHome):
                splitPlayerRedCardHomeTwo = splitPlayerRedCardHome[elementRedCardHome]
                splitPlayerRedCardHomeThree = splitPlayerRedCardHomeTwo.split(" (")
                namePlayerRedCardHome = splitPlayerRedCardHomeThree[0]
                timeNotCorretRedCardHome = splitPlayerRedCardHomeThree[1]
                timeCorretRedCardHome = timeNotCorretRedCardHome.split(")")[0]
                TimePlayerRedCardHome = timeCorretRedCardHome
                HaveRedCardHome = elementRedCardHome + 1
                namePlayerRedCardHomeTrue = "{}:RedCardHome".format(namePlayerRedCardHome)
                listNamePlayerRedCardHome.append(namePlayerRedCardHomeTrue)
                listTimePlayerRedCardHome.append(TimePlayerRedCardHome)
                listAllPlayer.append(namePlayerRedCardHomeTrue)
                listAllTime.append(TimePlayerRedCardHome)

        playerRedCardAways = homeTeamScoreBall['match']['playeRedCardAway']
        if playerRedCardAways == None:
            HaveRedCardAway = 0
        else:
            listNamePlayerRedCardAway = []
            listTimePlayerRedCardAway = []
            for playerRedCardAway in playerRedCardAways:
                splitPlayerRedCardAway = playerRedCardAway.split("), ")
                lengthSplitPlayerRedCardAway = len(splitPlayerRedCardAway)
            for elementRedCardAway in range(0,lengthSplitPlayerRedCardAway):
                splitPlayerRedCardAwayTwo = splitPlayerRedCardAway[elementRedCardAway]
                splitPlayerRedCardAwayThree = splitPlayerRedCardAwayTwo.split(" (")
                namePlayerRedCardAway = splitPlayerRedCardAwayThree[0]
                timeNotCorretRedCardAway = splitPlayerRedCardAwayThree[1]
                timeCorretRedCardAway = timeNotCorretRedCardAway.split(")")[0]
                TimePlayerRedCardAway = timeCorretRedCardAway
                HaveRedCardAway = elementRedCardAway + 1
                namePlayerRedCardAwayTrue = "{}:RedCardAway".format(namePlayerRedCardAway)
                listNamePlayerRedCardAway.append(namePlayerRedCardAwayTrue)
                listTimePlayerRedCardAway.append(TimePlayerRedCardAway)
                listAllPlayer.append(namePlayerRedCardAwayTrue)
                listAllTime.append(TimePlayerRedCardAway)
        
        listNamePlayerScoreAway = []
        listTimePlayerScoreAway = []
        
        playerScoreAways = homeTeamScoreBall['match']['playerScoreAway']

        if playerScoreAways == None:
            ScoreAway = 0
        else:
            for playerScoreAway in playerScoreAways:
                splitPlayerScoreAway = playerScoreAway.split("), ")
                lengthSplitPlayerScoreAway = len(splitPlayerScoreAway)
            for elementScoreAway in range(0,lengthSplitPlayerScoreAway):
                splitPlayerScoreAwayTwo = splitPlayerScoreAway[elementScoreAway]
                splitPlayerScoreAwayThree = splitPlayerScoreAwayTwo.split(" (")
                namePlayerScoreAway = splitPlayerScoreAwayThree[0]
                timeNotCorretScoreAway = splitPlayerScoreAwayThree[1]
                timeCorretScoreAway = timeNotCorretScoreAway.split(")")[0]
                TimePlayerScoreAway = timeCorretScoreAway
                ScoreAway = elementScoreAway + 1
                namePlayerScoreAwayTrue = "{}:ScoreAway".format(namePlayerScoreAway)
                listNamePlayerScoreAway.append(namePlayerScoreAwayTrue)
                listTimePlayerScoreAway.append(TimePlayerScoreAway)
                listAllPlayer.append(namePlayerScoreAwayTrue)
                listAllTime.append(TimePlayerScoreAway)
            
        playerScoreHome = homeTeamScoreBall['match']['playerScoreHome']
        if playerScoreHome == None:
            ScoreHome = 0
        else:
            splitPlayerScoreHome = playerScoreHome.split("), ")
            lengthSplitPlayerScoreHome = len(splitPlayerScoreHome)
            listNamePlayerScoreHome = []
            listTimePlayerScoreHome = []
            for elementScoreHome in range(0,lengthSplitPlayerScoreHome):
                splitPlayerScoreHomeTwo = splitPlayerScoreHome[elementScoreHome]
                splitPlayerScoreHomeThree = splitPlayerScoreHomeTwo.split(" (")
                namePlayerScoreHome = splitPlayerScoreHomeThree[0]
                timeNotCorretScoreHome = splitPlayerScoreHomeThree[1]
                timeCorretScoreHome = timeNotCorretScoreHome.split(")")[0]
                TimePlayerScoreHome = timeCorretScoreHome
                ScoreHome = elementScoreHome + 1
                namePlayerScoreHomeTrue = "{}:ScoreHome".format(namePlayerScoreHome)
                listNamePlayerScoreHome.append(namePlayerScoreHomeTrue)
                listTimePlayerScoreHome.append(TimePlayerScoreHome)
                listAllPlayer.append(namePlayerScoreHomeTrue)
                listAllTime.append(TimePlayerScoreHome)

        playerYellowCardAway = homeTeamScoreBall['match']['playerYellowCardAway']
        if playerYellowCardAway == None:
            haveYellowCardAway = 0
        else:
            listNamePlayerYellowCardAway = []
            listTimePlayerYellowCardAway = []
            splitPlayerYellowCardAway = playerYellowCardAway.split("), ")
            lengthSplitPlayerYellowCardAway = len(splitPlayerYellowCardAway)
            for elementYellowCardAway in range(0,lengthSplitPlayerYellowCardAway):
                splitPlayerYellowCardAwayTwo = splitPlayerYellowCardAway[elementYellowCardAway]
                splitPlayerYellowCardAwayThree = splitPlayerYellowCardAwayTwo.split(" (")
                namePlayerYellowCardAway = splitPlayerYellowCardAwayThree[0]
                timeNotCorretYellowCardAway = splitPlayerYellowCardAwayThree[1]
                timeCorretYellowCardAway = timeNotCorretYellowCardAway.split(")")[0]
                TimePlayerYellowCardAway = timeCorretYellowCardAway
                haveYellowCardAway = elementYellowCardAway + 1
                namePlayerYellowCardAwayTrue = "{}:YellowCardAway".format(namePlayerYellowCardAway)
                listNamePlayerYellowCardAway.append(namePlayerYellowCardAwayTrue)
                listTimePlayerYellowCardAway.append(TimePlayerYellowCardAway)
                listAllPlayer.append(namePlayerYellowCardAwayTrue)
                listAllTime.append(TimePlayerYellowCardAway)


        playerYellowCardHomes = homeTeamScoreBall['match']['playerYellowCardHome']
        if playerYellowCardHomes == None:
            playerYellowCardHomes = 0
        else:
            listNamePlayerYellowCardHome = []
            listTimePlayerYellowCardHome = []
            for playerYellowCardHome in playerYellowCardHomes:
                splitPlayerYellowCardHome = playerYellowCardHome.split("), ")
                lengthSplitPlayerYellowCardHome = len(splitPlayerYellowCardHome)
            for elementYellowCardHome in range(0,lengthSplitPlayerYellowCardHome):
                splitPlayerYellowCardHomeTwo = splitPlayerYellowCardHome[elementYellowCardHome]
                splitPlayerYellowCardHomeThree = splitPlayerYellowCardHomeTwo.split(" (")
                namePlayerYellowCardHome = splitPlayerYellowCardHomeThree[0]
                timeNotCorretYellowCardHome = splitPlayerYellowCardHomeThree[1]
                timeCorretYellowCardHome = timeNotCorretYellowCardHome.split(")")[0]             
                TimePlayerYellowCardHome = timeCorretYellowCardHome
                haveYellowCardHome = elementYellowCardHome + 1
                namePlayerYellowCardHomeTrue = "{}:YellowCardHome".format(namePlayerYellowCardHome)
                listNamePlayerYellowCardHome.append(namePlayerYellowCardHomeTrue)
                listTimePlayerYellowCardHome.append(TimePlayerYellowCardHome)
                listAllPlayer.append(namePlayerYellowCardHomeTrue)
                listAllTime.append(TimePlayerYellowCardHome)
        
        namePlayerSolution = []

        lengthEventPeople = len(listAllPlayer)
        for elementEventPlayer in range(0,lengthEventPeople):
            allTimeEvent = listAllTime[elementEventPlayer].split(",")
            lengthTimeForEvent = len(allTimeEvent)
            if lengthTimeForEvent == 1:
                namePlayerSolution.append(listAllPlayer[elementEventPlayer])
            elif lengthTimeForEvent == 2:
                namePlayerSolution.append(listAllPlayer[elementEventPlayer])
                namePlayerSolution.append(listAllPlayer[elementEventPlayer])
            elif lengthTimeForEvent == 3:
                namePlayerSolution.append(listAllPlayer[elementEventPlayer])
                namePlayerSolution.append(listAllPlayer[elementEventPlayer])
                namePlayerSolution.append(listAllPlayer[elementEventPlayer])
            elif lengthTimeForEvent == 4:
                namePlayerSolution.append(listAllPlayer[elementEventPlayer])
                namePlayerSolution.append(listAllPlayer[elementEventPlayer])
                namePlayerSolution.append(listAllPlayer[elementEventPlayer])
                namePlayerSolution.append(listAllPlayer[elementEventPlayer])
            elif lengthTimeForEvent == 5:
                namePlayerSolution.append(listAllPlayer[elementEventPlayer])
                namePlayerSolution.append(listAllPlayer[elementEventPlayer])
                namePlayerSolution.append(listAllPlayer[elementEventPlayer])
                namePlayerSolution.append(listAllPlayer[elementEventPlayer])
                namePlayerSolution.append(listAllPlayer[elementEventPlayer])
            elif lengthTimeForEvent == 6:
                namePlayerSolution.append(listAllPlayer[elementEventPlayer])
                namePlayerSolution.append(listAllPlayer[elementEventPlayer])
                namePlayerSolution.append(listAllPlayer[elementEventPlayer])
                namePlayerSolution.append(listAllPlayer[elementEventPlayer])
                namePlayerSolution.append(listAllPlayer[elementEventPlayer])
                namePlayerSolution.append(listAllPlayer[elementEventPlayer])
            elif lengthTimeForEvent == 7:
                namePlayerSolution.append(listAllPlayer[elementEventPlayer])
                namePlayerSolution.append(listAllPlayer[elementEventPlayer])
                namePlayerSolution.append(listAllPlayer[elementEventPlayer])
                namePlayerSolution.append(listAllPlayer[elementEventPlayer])
                namePlayerSolution.append(listAllPlayer[elementEventPlayer])
                namePlayerSolution.append(listAllPlayer[elementEventPlayer])
                namePlayerSolution.append(listAllPlayer[elementEventPlayer])
            elif lengthTimeForEvent == 8:
                namePlayerSolution.append(listAllPlayer[elementEventPlayer])
                namePlayerSolution.append(listAllPlayer[elementEventPlayer])
                namePlayerSolution.append(listAllPlayer[elementEventPlayer])
                namePlayerSolution.append(listAllPlayer[elementEventPlayer])
                namePlayerSolution.append(listAllPlayer[elementEventPlayer])
                namePlayerSolution.append(listAllPlayer[elementEventPlayer])
                namePlayerSolution.append(listAllPlayer[elementEventPlayer])
                namePlayerSolution.append(listAllPlayer[elementEventPlayer])
            elif lengthTimeForEvent == 9:
                namePlayerSolution.append(listAllPlayer[elementEventPlayer])
                namePlayerSolution.append(listAllPlayer[elementEventPlayer])
                namePlayerSolution.append(listAllPlayer[elementEventPlayer])
                namePlayerSolution.append(listAllPlayer[elementEventPlayer])
                namePlayerSolution.append(listAllPlayer[elementEventPlayer])
                namePlayerSolution.append(listAllPlayer[elementEventPlayer])
                namePlayerSolution.append(listAllPlayer[elementEventPlayer])
                namePlayerSolution.append(listAllPlayer[elementEventPlayer])
                namePlayerSolution.append(listAllPlayer[elementEventPlayer])
            elif lengthTimeForEvent == 10:
                namePlayerSolution.append(listAllPlayer[elementEventPlayer])
                namePlayerSolution.append(listAllPlayer[elementEventPlayer])
        countYellowCardAway = 0
        countYellowCardHome = 0
        countScoreHome = 0
        countScoreAway = 0
        countRedCardAway = 0
        countRedCardHome = 0
        for allNameEvent,element in zip(namePlayerSolution,range(0,len(namePlayerSolution))):
            
            if 'YellowCardAway' in allNameEvent:
                countYellowCardAway += 1
                namePlayerSolution[element] = "{}:{}".format(allNameEvent,countYellowCardAway)
            elif 'YellowCardHome' in allNameEvent:
                countYellowCardHome += 1
                namePlayerSolution[element] = "{}:{}".format(allNameEvent,countYellowCardHome)
            
            elif 'ScoreHome' in allNameEvent:
                countScoreHome += 1
                namePlayerSolution[element] = "{}:{} - {}".format(allNameEvent,countScoreHome,countScoreAway)
            elif 'ScoreAway' in allNameEvent:
                countScoreAway += 1
                namePlayerSolution[element] = "{}:{} - {}".format(allNameEvent,countScoreHome,countScoreAway)
            
            elif 'RedCardAway' in allNameEvent:
                countRedCardAway += 1
                namePlayerSolution[element] = "{}:{}".format(allNameEvent,countRedCardAway)
            elif 'RedCardHome' in allNameEvent:
                countRedCardHome += 1
                namePlayerSolution[element] = "{}:{}".format(allNameEvent,countRedCardHome)
        listAllTimeSolution = []
        for element in range(0,len(listAllTime)):
            allListSplitTime = listAllTime[element].split(" pen.")
            allListAddTime = allListSplitTime[0]
            allListAddTimeNotQuote = allListAddTime.split(", ")
            lenghtDataNotQuote = len(allListAddTimeNotQuote)
            for elementNotQuote in range(0,lenghtDataNotQuote):
                allTimeSolution = allListAddTimeNotQuote[elementNotQuote][:-1]
                listAllTimeSolution.append(allTimeSolution)
        listAllTimeSolution = list(map(int, listAllTimeSolution))
        nameAndNumber = []
        for allListElement in range(0,len(listAllTimeSolution)):
            nameAndNumber.append([namePlayerSolution[allListElement] ,listAllTimeSolution[allListElement]])
        def Sort(StringAndNumber): 
            return(sorted(StringAndNumber, key = lambda x: x[1]))     
        StringAndNumber = nameAndNumber
        allNameAndStringRank = Sort(StringAndNumber)
        listAllEventPlayer = []
        for elementAllEvent in range(0,len(allNameAndStringRank)):
            AllEvent = allNameAndStringRank[elementAllEvent][0]
            timeEvent = allNameAndStringRank[elementAllEvent][1]
            splitAllEvent = AllEvent.split(":")
            EventName = splitAllEvent[0]
            EventCategory = splitAllEvent[1]
            EventScore = splitAllEvent[2]
            if 'YellowCardAway' in EventCategory:
                awayPlayerYellowCard = """,{"type":"box","layout":"baseline","spacing":"sm","contents":[{"type":"text","text":" ","color":"#aaaaaa","size":"sm","flex":1},{"type":"icon","url":"https://upload.wikimedia.org/wikipedia/commons/thumb/b/b1/Yellow_card.svg/220px-Yellow_card.svg.png","size":"sm"},{"type":"text","text":"%s(%s)","wrap":true,"size":"sm","flex":1,"align":"end"}]}"""%(EventName,timeEvent)
                listAllEventPlayer.append(awayPlayerYellowCard)
            elif 'YellowCardHome' in EventCategory:
                homePlayerYellowCard = """,{"type":"box","layout":"baseline","spacing":"sm","contents":[{"type":"text","text":"%s(%s)","wrap":true,"size":"sm","flex":1},{"type":"icon","url":"https://upload.wikimedia.org/wikipedia/commons/thumb/b/b1/Yellow_card.svg/220px-Yellow_card.svg.png","size":"sm"},{"type":"text","text":" ","wrap":true,"size":"sm","flex":1,"align":"start"}]}"""%(EventName,timeEvent)
                listAllEventPlayer.append(homePlayerYellowCard)
            elif 'ScoreHome' in EventCategory:
                homePlayerScore = """,{"type":"box","layout":"baseline","spacing":"sm","contents":[{"type":"text","text":"%s(%s)","wrap":true,"size":"sm","flex":1},{"type":"text","text":"%s","wrap":true,"color":"#008000","weight":"bold","size":"sm","flex":1,"align":"center"},{"type":"text","text":" ","wrap":true,"size":"sm","flex":1,"align":"start"}]}"""%(EventName,timeEvent,EventScore)
                listAllEventPlayer.append(homePlayerScore)
            elif 'ScoreAway' in EventCategory:
                awayPlayerScore = """,{"type":"box","layout":"baseline","spacing":"sm","contents":[{"type":"text","text":" ","color":"#aaaaaa","size":"sm","flex":1},{"type":"text","text":"%s","wrap":true,"color":"#008000","weight":"bold","size":"sm","flex":1,"align":"center"},{"type":"text","text":"%s(%s)","wrap":true,"size":"sm","flex":1}]}"""%(EventScore,EventName,timeEvent)        
                listAllEventPlayer.append(awayPlayerScore)
            elif 'RedCardAway' in EventCategory:
                awayPlayerRedCard = """,{"type":"box","layout":"baseline","spacing":"sm","contents":[{"type":"text","text":" ","color":"#aaaaaa","size":"sm","flex":1},{"type":"icon","url":"https://upload.wikimedia.org/wikipedia/commons/thumb/e/e7/Red_card.svg/1200px-Red_card.svg.png","size":"sm"},{"type":"text","text":"%s(%s)","wrap":true,"size":"sm","flex":1,"align":"end"}]}"""%(EventName,timeEvent)      
                listAllEventPlayer.append(awayPlayerRedCard)
            elif 'RedCardHome' in EventCategory:
                homePlayerRedCard = """,{"type":"box","layout":"baseline","spacing":"sm","contents":[{"type":"text","text":"%s(%s)","wrap":true,"size":"sm","flex":1},{"type":"icon","url":"https://upload.wikimedia.org/wikipedia/commons/thumb/e/e7/Red_card.svg/1200px-Red_card.svg.png","size":"sm"},{"type":"text","text":" ","wrap":true,"size":"sm","flex":1,"align":"start"}]}"""%(EventName,timeEvent)
                listAllEventPlayer.append(homePlayerRedCard)
        allEventPlayer = "".join(listAllEventPlayer)
        homePlayerScore = """,{"type":"box","layout":"baseline","spacing":"sm","contents":[{"type":"text","text":"playerSc(40')","wrap":true,"size":"sm","flex":1},{"type":"text","text":"1 - 0","wrap":true,"color":"#008000","weight":"bold","size":"sm","flex":1,"align":"center"},{"type":"text","text":" ","wrap":true,"size":"sm","flex":1,"align":"start"}]}
        """
        homePlayerYellowCard = """,{"type":"box","layout":"baseline","spacing":"sm","contents":[{"type":"text","text":"YellowC(50')","wrap":true,"size":"sm","flex":1},{"type":"icon","url":"https://upload.wikimedia.org/wikipedia/commons/thumb/b/b1/Yellow_card.svg/220px-Yellow_card.svg.png","size":"sm"},{"type":"text","text":" ","wrap":true,"size":"sm","flex":1,"align":"start"}]}               
        """
        homePlayerRedCard = """,{"type":"box","layout":"baseline","spacing":"sm","contents":[{"type":"text","text":"YellowC(50')","wrap":true,"size":"sm","flex":1},{"type":"icon","url":"https://upload.wikimedia.org/wikipedia/commons/thumb/e/e7/Red_card.svg/1200px-Red_card.svg.png","size":"sm"},{"type":"text","text":" ","wrap":true,"size":"sm","flex":1,"align":"start"}]}            
        """
        awayPlayerScore = """,{"type":"box","layout":"baseline","spacing":"sm","contents":[{"type":"text","text":" ","color":"#aaaaaa","size":"sm","flex":1},{"type":"text","text":"1 - 1","wrap":true,"color":"#008000","weight":"bold","size":"sm","flex":1,"align":"center"},{"type":"text","text":"playerSc(20')","wrap":true,"size":"sm","flex":1}]}                
        """
        awayPlayerYellowCard = """,{"type":"box","layout":"baseline","spacing":"sm","contents":[{"type":"text","text":" ","color":"#aaaaaa","size":"sm","flex":1},{"type":"icon","url":"https://upload.wikimedia.org/wikipedia/commons/thumb/b/b1/Yellow_card.svg/220px-Yellow_card.svg.png","size":"sm"},{"type":"text","text":"YellowC(60')","wrap":true,"size":"sm","flex":1,"align":"end"}]}
        """
        awayPlayerRedCard = """,{"type":"box","layout":"baseline","spacing":"sm","contents":[{"type":"text","text":" ","color":"#aaaaaa","size":"sm","flex":1},{"type":"icon","url":"https://upload.wikimedia.org/wikipedia/commons/thumb/e/e7/Red_card.svg/1200px-Red_card.svg.png","size":"sm"},{"type":"text","text":"YellowC(60')","wrap":true,"size":"sm","flex":1,"align":"end"}]}           
        """
        penaltyTrue = """,{"type":"box","layout":"baseline","spacing":"sm","contents":[{"type":"text","text":"panelty:","color":"#008000","weight":"bold","size":"sm","flex":2},{"type":"text","text":"%s","wrap":true,"size":"sm","flex":4}]}"""%(penalty)
        # print(listAllTime[4])
        # print("penalty:",penalty)
        # print("homeTeam:",homeTeam)
        # print("awayTeam:",awayTeam)
        # print("dateTime:",dateTime)
        # print("league:",league)
        # print("timeStatus:",timeStatus)
        scoreBall = """
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
    "size": "lg",
    "color": "#008000"
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
        "color": "#008000",
        "weight": "bold",
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
            "text": "------------------event------------------",
            "color": "#008000",
            "size": "sm",
            "weight": "bold",
            "align": "center"
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
        "text": "league:",
        "color": "#008000",
        "weight": "bold",
        "size": "sm",
        "flex": 2
        },
        {
        "type": "text",
        "text": "%s",
        "wrap": true,
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
        "text": "Date:",
        "color": "#008000",
        "weight": "bold",
        "size": "sm",
        "flex": 2
        },
        {
        "type": "text",
        "text": "%s",
        "wrap": true,
        "size": "sm",
        "flex": 4
        }
    ]
    }
    %s
]
}
}
        """%(timeStatus,homeTeam,ScoreHome,ScoreAway,awayTeam,allEventPlayer,league,dateTime,penaltyTrue)
        scoreBall = json.loads(scoreBall)
        carousel_container.contents.append(scoreBall)
        line_bot_api.reply_message(event.reply_token, FlexSendMessage(alt_text='Fixtures', contents=carousel_container))
# (--------------------------------------------------Ball league-------------------------------------------------)
    elif event.message.text[:14] == 'allTableLeague':
        apiTable = ('https://scrape-league-ball.herokuapp.com/')
        allDataLinkTables = requests.get(apiTable).json()
        buttons = []
        for allDataLinkTable,element in zip(allDataLinkTables,range(0,len(allDataLinkTables))):
            leagueName = allDataLinkTable['leagueName']
            print('leagueName',leagueName)
            buttons.append(
                ButtonComponent(layout='horizontal',
                            style='primary', 
                            height='sm',
                            action=MessageAction(label=f'{leagueName}', text=f'Table {leagueName}')
                ),
            )
        bubble = BubbleContainer(
            direction='ltr',
            hero=ImageComponent(
                url='https://www.928betwin.com/wp-content/uploads/2017/03/%E0%B8%A3%E0%B8%B2%E0%B8%84%E0%B8%B2%E0%B8%9A%E0%B8%AD%E0%B8%A5%E0%B8%95%E0%B9%88%E0%B8%AD.jpg',
                size='full',
                aspect_ratio='20:13',
                aspect_mode='cover',
                action=URIAction(uri='http://example.com', label='label')
            ),
            body=BoxComponent(
                layout='vertical',
                align='start',
                contents=[
                    TextComponent(text='name league:', weight='bold', size='xl'),
                ],
            ),
            footer=BoxComponent(
                layout='vertical',
                spacing='sm',

                contents=buttons
            ),
        )
        message = FlexSendMessage(alt_text="score-ball", contents=bubble)
        line_bot_api.reply_message(
            event.reply_token,
            message
        )


        


    
    elif event.message.text[:6] == 'Table ':
        carousel_container = CarouselContainer()
        splitLeague = event.message.text.split("Table ")
        leagueCountry = splitLeague[1]
        apiNameLeague = ('https://scrape-league-ball.herokuapp.com/league?leagueName={}').format(leagueCountry)
        allDataLinkTables = requests.get(apiNameLeague).json()
        lengthDataTeams = len(allDataLinkTables[0])
        count = 0
        listRankTeam = []
        listTeam = []
        listPoint = []
        listGamePlay = []
        for element in range(1,lengthDataTeams):
            elementTeam = '{}'.format(element)
            rankTeam = allDataLinkTables[0]['{}'.format(elementTeam)]['rank']
            team = allDataLinkTables[0]['{}'.format(elementTeam)]['team']
            point = allDataLinkTables[0]['{}'.format(elementTeam)]['point']
            gamePlay = allDataLinkTables[0]['{}'.format(elementTeam)]['Gameplay']
            listRankTeam.append(rankTeam)
            listTeam.append(team)
            listPoint.append(point)
            listGamePlay.append(gamePlay)
            # print(rankTeam,team,point,gamePlay)
            count += 1
        if count >= 20:
            tableAllPageOne ='''{"type":"bubble","styles":{"header":{"backgroundColor":"#228B22"}},"header":{"type":"box","layout":"horizontal","contents":[{"type":"text","text":"League %s","color":"#FFFFFF","size":"md"}]},"body":{"type":"box","layout":"vertical","contents":[{"type":"box","layout":"vertical","margin":"xxl","spacing":"sm","contents":[{"type":"box","layout":"horizontal","contents":[{"type":"text","text":"#","weight":"bold","flex":1,"gravity":"center"},{"type":"text","text":"Team","weight":"bold","flex":5,"gravity":"center"},{"type":"text","weight":"bold","text":"P","flex":1,"gravity":"center"},{"type":"text","weight":"bold","text":"Pts","flex":1,"gravity":"center"}]},{"type":"separator","margin":"sm"},{"type":"box","layout":"horizontal","contents":[{"type":"text","text":"%s","flex":1,"gravity":"center"},{"type":"text","text":"%s","flex":5,"gravity":"center"},{"type":"text","text":"%s","flex":1,"gravity":"center"},{"type":"text","text":"%s","flex":1,"gravity":"center"}]},{"type":"box","layout":"horizontal","contents":[{"type":"text","text":"%s","flex":1,"gravity":"center"},{"type":"text","text":"%s","flex":5,"gravity":"center"},{"type":"text","text":"%s","flex":1,"gravity":"center"},{"type":"text","text":"%s","flex":1,"gravity":"center"}]},{"type":"box","layout":"horizontal","contents":[{"type":"text","text":"%s","flex":1,"gravity":"center"},{"type":"text","text":"%s","flex":5,"gravity":"center"},{"type":"text","text":"%s","flex":1,"gravity":"center"},{"type":"text","text":"%s","flex":1,"gravity":"center"}]},{"type":"box","layout":"horizontal","contents":[{"type":"text","text":"%s","flex":1,"gravity":"center"},{"type":"text","text":"%s","flex":5,"gravity":"center"},{"type":"text","text":"%s","flex":1,"gravity":"center"},{"type":"text","text":"%s","flex":1,"gravity":"center"}]},{"type":"box","layout":"horizontal","contents":[{"type":"text","text":"%s","flex":1,"gravity":"center"},{"type":"text","text":"%s","flex":5,"gravity":"center"},{"type":"text","text":"%s","flex":1,"gravity":"center"},{"type":"text","text":"%s","flex":1,"gravity":"center"}]},{"type":"box","layout":"horizontal","contents":[{"type":"text","text":"%s","flex":1,"gravity":"center"},{"type":"text","text":"%s","flex":5,"gravity":"center"},{"type":"text","text":"%s","flex":1,"gravity":"center"},{"type":"text","text":"%s","flex":1,"gravity":"center"}]},{"type":"box","layout":"horizontal","contents":[{"type":"text","text":"%s","flex":1,"gravity":"center"},{"type":"text","text":"%s","flex":5,"gravity":"center"},{"type":"text","text":"%s","flex":1,"gravity":"center"},{"type":"text","text":"%s","flex":1,"gravity":"center"}]},{"type":"box","layout":"horizontal","contents":[{"type":"text","text":"%s","flex":1,"gravity":"center"},{"type":"text","text":"%s","flex":5,"gravity":"center"},{"type":"text","text":"%s","flex":1,"gravity":"center"},{"type":"text","text":"%s","flex":1,"gravity":"center"}]},{"type":"box","layout":"horizontal","contents":[{"type":"text","text":"%s","flex":1,"gravity":"center"},{"type":"text","text":"%s","flex":5,"gravity":"center"},{"type":"text","text":"%s","flex":1,"gravity":"center"},{"type":"text","text":"%s","flex":1,"gravity":"center"}]},{"type":"box","layout":"horizontal","contents":[{"type":"text","text":"%s","flex":1,"gravity":"center"},{"type":"text","text":"%s","flex":5,"gravity":"center"},{"type":"text","text":"%s","flex":1,"gravity":"center"},{"type":"text","text":"%s","flex":1,"gravity":"center"}]}]}]}}'''%(leagueCountry,listRankTeam[0],listTeam[0],listGamePlay[0],listPoint[0],listRankTeam[1],listTeam[1],listGamePlay[1],listPoint[1],listRankTeam[2],listTeam[2],listGamePlay[2],listPoint[2],listRankTeam[3],listTeam[3],listGamePlay[3],listPoint[3],listRankTeam[4],listTeam[4],listGamePlay[4],listPoint[4],listRankTeam[5],listTeam[5],listGamePlay[5],listPoint[5],listRankTeam[6],listTeam[6],listGamePlay[6],listPoint[6],listRankTeam[7],listTeam[7],listGamePlay[7],listPoint[7],listRankTeam[8],listTeam[8],listGamePlay[8],listPoint[8],listRankTeam[9],listTeam[9],listGamePlay[9],listPoint[9])
            tableAllPageTwo ='''{"type":"bubble","styles":{"header":{"backgroundColor":"#228B22"}},"header":{"type":"box","layout":"horizontal","contents":[{"type":"text","text":"League %s","color":"#FFFFFF","size":"md"}]},"body":{"type":"box","layout":"vertical","contents":[{"type":"box","layout":"vertical","margin":"xxl","spacing":"sm","contents":[{"type":"box","layout":"horizontal","contents":[{"type":"text","text":"#","weight":"bold","flex":1,"gravity":"center"},{"type":"text","text":"Team","weight":"bold","flex":5,"gravity":"center"},{"type":"text","weight":"bold","text":"P","flex":1,"gravity":"center"},{"type":"text","weight":"bold","text":"Pts","flex":1,"gravity":"center"}]},{"type":"separator","margin":"sm"},{"type":"box","layout":"horizontal","contents":[{"type":"text","text":"%s","flex":1,"gravity":"center"},{"type":"text","text":"%s","flex":5,"gravity":"center"},{"type":"text","text":"%s","flex":1,"gravity":"center"},{"type":"text","text":"%s","flex":1,"gravity":"center"}]},{"type":"box","layout":"horizontal","contents":[{"type":"text","text":"%s","flex":1,"gravity":"center"},{"type":"text","text":"%s","flex":5,"gravity":"center"},{"type":"text","text":"%s","flex":1,"gravity":"center"},{"type":"text","text":"%s","flex":1,"gravity":"center"}]},{"type":"box","layout":"horizontal","contents":[{"type":"text","text":"%s","flex":1,"gravity":"center"},{"type":"text","text":"%s","flex":5,"gravity":"center"},{"type":"text","text":"%s","flex":1,"gravity":"center"},{"type":"text","text":"%s","flex":1,"gravity":"center"}]},{"type":"box","layout":"horizontal","contents":[{"type":"text","text":"%s","flex":1,"gravity":"center"},{"type":"text","text":"%s","flex":5,"gravity":"center"},{"type":"text","text":"%s","flex":1,"gravity":"center"},{"type":"text","text":"%s","flex":1,"gravity":"center"}]},{"type":"box","layout":"horizontal","contents":[{"type":"text","text":"%s","flex":1,"gravity":"center"},{"type":"text","text":"%s","flex":5,"gravity":"center"},{"type":"text","text":"%s","flex":1,"gravity":"center"},{"type":"text","text":"%s","flex":1,"gravity":"center"}]},{"type":"box","layout":"horizontal","contents":[{"type":"text","text":"%s","flex":1,"gravity":"center"},{"type":"text","text":"%s","flex":5,"gravity":"center"},{"type":"text","text":"%s","flex":1,"gravity":"center"},{"type":"text","text":"%s","flex":1,"gravity":"center"}]},{"type":"box","layout":"horizontal","contents":[{"type":"text","text":"%s","flex":1,"gravity":"center"},{"type":"text","text":"%s","flex":5,"gravity":"center"},{"type":"text","text":"%s","flex":1,"gravity":"center"},{"type":"text","text":"%s","flex":1,"gravity":"center"}]},{"type":"box","layout":"horizontal","contents":[{"type":"text","text":"%s","flex":1,"gravity":"center"},{"type":"text","text":"%s","flex":5,"gravity":"center"},{"type":"text","text":"%s","flex":1,"gravity":"center"},{"type":"text","text":"%s","flex":1,"gravity":"center"}]},{"type":"box","layout":"horizontal","contents":[{"type":"text","text":"%s","flex":1,"gravity":"center"},{"type":"text","text":"%s","flex":5,"gravity":"center"},{"type":"text","text":"%s","flex":1,"gravity":"center"},{"type":"text","text":"%s","flex":1,"gravity":"center"}]},{"type":"box","layout":"horizontal","contents":[{"type":"text","text":"%s","flex":1,"gravity":"center"},{"type":"text","text":"%s","flex":5,"gravity":"center"},{"type":"text","text":"%s","flex":1,"gravity":"center"},{"type":"text","text":"%s","flex":1,"gravity":"center"}]}]}]}}'''%(leagueCountry,listRankTeam[10],listTeam[10],listGamePlay[10],listPoint[10],listRankTeam[11],listTeam[11],listGamePlay[11],listPoint[11],listRankTeam[12],listTeam[12],listGamePlay[12],listPoint[12],listRankTeam[13],listTeam[13],listGamePlay[13],listPoint[13],listRankTeam[14],listTeam[14],listGamePlay[14],listPoint[14],listRankTeam[15],listTeam[15],listGamePlay[15],listPoint[15],listRankTeam[16],listTeam[16],listGamePlay[16],listPoint[16],listRankTeam[17],listTeam[17],listGamePlay[17],listPoint[17],listRankTeam[18],listTeam[18],listGamePlay[18],listPoint[18],listRankTeam[19],listTeam[19],listGamePlay[19],listPoint[19])
            tableAllPageOne = json.loads(tableAllPageOne)
            tableAllPageTwo = json.loads(tableAllPageTwo)
            carousel_container.contents.append(tableAllPageOne)
            carousel_container.contents.append(tableAllPageTwo)
            if count == 21:
                tableAllPageThree ='''{"type":"bubble","styles":{"header":{"backgroundColor":"#228B22"}},"header":{"type":"box","layout":"horizontal","contents":[{"type":"text","text":"League %s","color":"#FFFFFF","size":"md"}]},"body":{"type":"box","layout":"vertical","contents":[{"type":"box","layout":"vertical","margin":"xxl","spacing":"sm","contents":[{"type":"box","layout":"horizontal","contents":[{"type":"text","text":"#","weight":"bold","flex":1,"gravity":"center"},{"type":"text","text":"Team","weight":"bold","flex":5,"gravity":"center"},{"type":"text","weight":"bold","text":"P","flex":1,"gravity":"center"},{"type":"text","weight":"bold","text":"Pts","flex":1,"gravity":"center"}]},{"type":"separator","margin":"sm"},{"type":"box","layout":"horizontal","contents":[{"type":"text","text":"%s","flex":1,"gravity":"center"},{"type":"text","text":"%s","flex":5,"gravity":"center"},{"type":"text","text":"%s","flex":1,"gravity":"center"},{"type":"text","text":"%s","flex":1,"gravity":"center"}]}]}]}}'''%(leagueCountry,listRankTeam[20],listTeam[20],listGamePlay[20],listPoint[20])
                tableAllPageThree = json.loads(tableAllPageThree)
                carousel_container.contents.append(tableAllPageThree)
            if count == 22:
                tableAllPageThree ='''{"type":"bubble","styles":{"header":{"backgroundColor":"#228B22"}},"header":{"type":"box","layout":"horizontal","contents":[{"type":"text","text":"League %s","color":"#FFFFFF","size":"md"}]},"body":{"type":"box","layout":"vertical","contents":[{"type":"box","layout":"vertical","margin":"xxl","spacing":"sm","contents":[{"type":"box","layout":"horizontal","contents":[{"type":"text","text":"#","weight":"bold","flex":1,"gravity":"center"},{"type":"text","text":"Team","weight":"bold","flex":5,"gravity":"center"},{"type":"text","weight":"bold","text":"P","flex":1,"gravity":"center"},{"type":"text","weight":"bold","text":"Pts","flex":1,"gravity":"center"}]},{"type":"separator","margin":"sm"},{"type":"box","layout":"horizontal","contents":[{"type":"text","text":"%s","flex":1,"gravity":"center"},{"type":"text","text":"%s","flex":5,"gravity":"center"},{"type":"text","text":"%s","flex":1,"gravity":"center"},{"type":"text","text":"%s","flex":1,"gravity":"center"}]},{"type":"box","layout":"horizontal","contents":[{"type":"text","text":"%s","flex":1,"gravity":"center"},{"type":"text","text":"%s","flex":5,"gravity":"center"},{"type":"text","text":"%s","flex":1,"gravity":"center"},{"type":"text","text":"%s","flex":1,"gravity":"center"}]}]}]}}'''%(leagueCountry,listRankTeam[20],listTeam[20],listGamePlay[20],listPoint[20],listRankTeam[21],listTeam[21],listGamePlay[21],listPoint[21])
                tableAllPageThree = json.loads(tableAllPageThree)
                carousel_container.contents.append(tableAllPageThree)
            if count == 23:
                tableAllPageThree ='''{"type":"bubble","styles":{"header":{"backgroundColor":"#228B22"}},"header":{"type":"box","layout":"horizontal","contents":[{"type":"text","text":"League %s","color":"#FFFFFF","size":"md"}]},"body":{"type":"box","layout":"vertical","contents":[{"type":"box","layout":"vertical","margin":"xxl","spacing":"sm","contents":[{"type":"box","layout":"horizontal","contents":[{"type":"text","text":"#","weight":"bold","flex":1,"gravity":"center"},{"type":"text","text":"Team","weight":"bold","flex":5,"gravity":"center"},{"type":"text","weight":"bold","text":"P","flex":1,"gravity":"center"},{"type":"text","weight":"bold","text":"Pts","flex":1,"gravity":"center"}]},{"type":"separator","margin":"sm"},{"type":"box","layout":"horizontal","contents":[{"type":"text","text":"%s","flex":1,"gravity":"center"},{"type":"text","text":"%s","flex":5,"gravity":"center"},{"type":"text","text":"%s","flex":1,"gravity":"center"},{"type":"text","text":"%s","flex":1,"gravity":"center"}]},{"type":"box","layout":"horizontal","contents":[{"type":"text","text":"%s","flex":1,"gravity":"center"},{"type":"text","text":"%s","flex":5,"gravity":"center"},{"type":"text","text":"%s","flex":1,"gravity":"center"},{"type":"text","text":"%s","flex":1,"gravity":"center"}]},{"type":"box","layout":"horizontal","contents":[{"type":"text","text":"%s","flex":1,"gravity":"center"},{"type":"text","text":"%s","flex":5,"gravity":"center"},{"type":"text","text":"%s","flex":1,"gravity":"center"},{"type":"text","text":"%s","flex":1,"gravity":"center"}]}]}]}}'''%(leagueCountry,listRankTeam[20],listTeam[20],listGamePlay[20],listPoint[20],listRankTeam[21],listTeam[21],listGamePlay[21],listPoint[21],listRankTeam[22],listTeam[22],listGamePlay[22],listPoint[22])
                tableAllPageThree = json.loads(tableAllPageThree)
                carousel_container.contents.append(tableAllPageThree)
            if count == 24:
                tableAllPageThree ='''{"type":"bubble","styles":{"header":{"backgroundColor":"#228B22"}},"header":{"type":"box","layout":"horizontal","contents":[{"type":"text","text":"League %s","color":"#FFFFFF","size":"md"}]},"body":{"type":"box","layout":"vertical","contents":[{"type":"box","layout":"vertical","margin":"xxl","spacing":"sm","contents":[{"type":"box","layout":"horizontal","contents":[{"type":"text","text":"#","weight":"bold","flex":1,"gravity":"center"},{"type":"text","text":"Team","weight":"bold","flex":5,"gravity":"center"},{"type":"text","weight":"bold","text":"P","flex":1,"gravity":"center"},{"type":"text","weight":"bold","text":"Pts","flex":1,"gravity":"center"}]},{"type":"separator","margin":"sm"},{"type":"box","layout":"horizontal","contents":[{"type":"text","text":"%s","flex":1,"gravity":"center"},{"type":"text","text":"%s","flex":5,"gravity":"center"},{"type":"text","text":"%s","flex":1,"gravity":"center"},{"type":"text","text":"%s","flex":1,"gravity":"center"}]},{"type":"box","layout":"horizontal","contents":[{"type":"text","text":"%s","flex":1,"gravity":"center"},{"type":"text","text":"%s","flex":5,"gravity":"center"},{"type":"text","text":"%s","flex":1,"gravity":"center"},{"type":"text","text":"%s","flex":1,"gravity":"center"}]},{"type":"box","layout":"horizontal","contents":[{"type":"text","text":"%s","flex":1,"gravity":"center"},{"type":"text","text":"%s","flex":5,"gravity":"center"},{"type":"text","text":"%s","flex":1,"gravity":"center"},{"type":"text","text":"%s","flex":1,"gravity":"center"}]},{"type":"box","layout":"horizontal","contents":[{"type":"text","text":"%s","flex":1,"gravity":"center"},{"type":"text","text":"%s","flex":5,"gravity":"center"},{"type":"text","text":"%s","flex":1,"gravity":"center"},{"type":"text","text":"%s","flex":1,"gravity":"center"}]}]}]}}'''%(leagueCountry,listRankTeam[20],listTeam[20],listGamePlay[20],listPoint[20],listRankTeam[21],listTeam[21],listGamePlay[21],listPoint[21],listRankTeam[22],listTeam[22],listGamePlay[22],listPoint[22],listRankTeam[23],listTeam[23],listGamePlay[23],listPoint[23])
                tableAllPageThree = json.loads(tableAllPageThree)
                carousel_container.contents.append(tableAllPageThree)
            if count == 25:
                tableAllPageThree ='''{"type":"bubble","styles":{"header":{"backgroundColor":"#228B22"}},"header":{"type":"box","layout":"horizontal","contents":[{"type":"text","text":"League %s","color":"#FFFFFF","size":"md"}]},"body":{"type":"box","layout":"vertical","contents":[{"type":"box","layout":"vertical","margin":"xxl","spacing":"sm","contents":[{"type":"box","layout":"horizontal","contents":[{"type":"text","text":"#","weight":"bold","flex":1,"gravity":"center"},{"type":"text","text":"Team","weight":"bold","flex":5,"gravity":"center"},{"type":"text","weight":"bold","text":"P","flex":1,"gravity":"center"},{"type":"text","weight":"bold","text":"Pts","flex":1,"gravity":"center"}]},{"type":"separator","margin":"sm"},{"type":"box","layout":"horizontal","contents":[{"type":"text","text":"%s","flex":1,"gravity":"center"},{"type":"text","text":"%s","flex":5,"gravity":"center"},{"type":"text","text":"%s","flex":1,"gravity":"center"},{"type":"text","text":"%s","flex":1,"gravity":"center"}]},{"type":"box","layout":"horizontal","contents":[{"type":"text","text":"%s","flex":1,"gravity":"center"},{"type":"text","text":"%s","flex":5,"gravity":"center"},{"type":"text","text":"%s","flex":1,"gravity":"center"},{"type":"text","text":"%s","flex":1,"gravity":"center"}]},{"type":"box","layout":"horizontal","contents":[{"type":"text","text":"%s","flex":1,"gravity":"center"},{"type":"text","text":"%s","flex":5,"gravity":"center"},{"type":"text","text":"%s","flex":1,"gravity":"center"},{"type":"text","text":"%s","flex":1,"gravity":"center"}]},{"type":"box","layout":"horizontal","contents":[{"type":"text","text":"%s","flex":1,"gravity":"center"},{"type":"text","text":"%s","flex":5,"gravity":"center"},{"type":"text","text":"%s","flex":1,"gravity":"center"},{"type":"text","text":"%s","flex":1,"gravity":"center"}]},{"type":"box","layout":"horizontal","contents":[{"type":"text","text":"%s","flex":1,"gravity":"center"},{"type":"text","text":"%s","flex":5,"gravity":"center"},{"type":"text","text":"%s","flex":1,"gravity":"center"},{"type":"text","text":"%s","flex":1,"gravity":"center"}]}]}]}}'''%(leagueCountry,listRankTeam[20],listTeam[20],listGamePlay[20],listPoint[20],listRankTeam[21],listTeam[21],listGamePlay[21],listPoint[21],listRankTeam[22],listTeam[22],listGamePlay[22],listPoint[22],listRankTeam[23],listTeam[23],listGamePlay[23],listPoint[23],listRankTeam[24],listTeam[24],listGamePlay[24],listPoint[24])
                tableAllPageThree = json.loads(tableAllPageThree)
                carousel_container.contents.append(tableAllPageThree)
            if count == 26:
                tableAllPageThree ='''{"type":"bubble","styles":{"header":{"backgroundColor":"#228B22"}},"header":{"type":"box","layout":"horizontal","contents":[{"type":"text","text":"League %s","color":"#FFFFFF","size":"md"}]},"body":{"type":"box","layout":"vertical","contents":[{"type":"box","layout":"vertical","margin":"xxl","spacing":"sm","contents":[{"type":"box","layout":"horizontal","contents":[{"type":"text","text":"#","weight":"bold","flex":1,"gravity":"center"},{"type":"text","text":"Team","weight":"bold","flex":5,"gravity":"center"},{"type":"text","weight":"bold","text":"P","flex":1,"gravity":"center"},{"type":"text","weight":"bold","text":"Pts","flex":1,"gravity":"center"}]},{"type":"separator","margin":"sm"},{"type":"box","layout":"horizontal","contents":[{"type":"text","text":"%s","flex":1,"gravity":"center"},{"type":"text","text":"%s","flex":5,"gravity":"center"},{"type":"text","text":"%s","flex":1,"gravity":"center"},{"type":"text","text":"%s","flex":1,"gravity":"center"}]},{"type":"box","layout":"horizontal","contents":[{"type":"text","text":"%s","flex":1,"gravity":"center"},{"type":"text","text":"%s","flex":5,"gravity":"center"},{"type":"text","text":"%s","flex":1,"gravity":"center"},{"type":"text","text":"%s","flex":1,"gravity":"center"}]},{"type":"box","layout":"horizontal","contents":[{"type":"text","text":"%s","flex":1,"gravity":"center"},{"type":"text","text":"%s","flex":5,"gravity":"center"},{"type":"text","text":"%s","flex":1,"gravity":"center"},{"type":"text","text":"%s","flex":1,"gravity":"center"}]},{"type":"box","layout":"horizontal","contents":[{"type":"text","text":"%s","flex":1,"gravity":"center"},{"type":"text","text":"%s","flex":5,"gravity":"center"},{"type":"text","text":"%s","flex":1,"gravity":"center"},{"type":"text","text":"%s","flex":1,"gravity":"center"}]},{"type":"box","layout":"horizontal","contents":[{"type":"text","text":"%s","flex":1,"gravity":"center"},{"type":"text","text":"%s","flex":5,"gravity":"center"},{"type":"text","text":"%s","flex":1,"gravity":"center"},{"type":"text","text":"%s","flex":1,"gravity":"center"}]},{"type":"box","layout":"horizontal","contents":[{"type":"text","text":"%s","flex":1,"gravity":"center"},{"type":"text","text":"%s","flex":5,"gravity":"center"},{"type":"text","text":"%s","flex":1,"gravity":"center"},{"type":"text","text":"%s","flex":1,"gravity":"center"}]}]}]}}'''%(leagueCountry,listRankTeam[20],listTeam[20],listGamePlay[20],listPoint[20],listRankTeam[21],listTeam[21],listGamePlay[21],listPoint[21],listRankTeam[22],listTeam[22],listGamePlay[22],listPoint[22],listRankTeam[23],listTeam[23],listGamePlay[23],listPoint[23],listRankTeam[24],listTeam[24],listGamePlay[24],listPoint[24],listRankTeam[25],listTeam[25],listGamePlay[25],listPoint[25])
                tableAllPageThree = json.loads(tableAllPageThree)
                carousel_container.contents.append(tableAllPageThree)
            if count == 27:
                tableAllPageThree ='''{"type":"bubble","styles":{"header":{"backgroundColor":"#228B22"}},"header":{"type":"box","layout":"horizontal","contents":[{"type":"text","text":"League %s","color":"#FFFFFF","size":"md"}]},"body":{"type":"box","layout":"vertical","contents":[{"type":"box","layout":"vertical","margin":"xxl","spacing":"sm","contents":[{"type":"box","layout":"horizontal","contents":[{"type":"text","text":"#","weight":"bold","flex":1,"gravity":"center"},{"type":"text","text":"Team","weight":"bold","flex":5,"gravity":"center"},{"type":"text","weight":"bold","text":"P","flex":1,"gravity":"center"},{"type":"text","weight":"bold","text":"Pts","flex":1,"gravity":"center"}]},{"type":"separator","margin":"sm"},{"type":"box","layout":"horizontal","contents":[{"type":"text","text":"%s","flex":1,"gravity":"center"},{"type":"text","text":"%s","flex":5,"gravity":"center"},{"type":"text","text":"%s","flex":1,"gravity":"center"},{"type":"text","text":"%s","flex":1,"gravity":"center"}]},{"type":"box","layout":"horizontal","contents":[{"type":"text","text":"%s","flex":1,"gravity":"center"},{"type":"text","text":"%s","flex":5,"gravity":"center"},{"type":"text","text":"%s","flex":1,"gravity":"center"},{"type":"text","text":"%s","flex":1,"gravity":"center"}]},{"type":"box","layout":"horizontal","contents":[{"type":"text","text":"%s","flex":1,"gravity":"center"},{"type":"text","text":"%s","flex":5,"gravity":"center"},{"type":"text","text":"%s","flex":1,"gravity":"center"},{"type":"text","text":"%s","flex":1,"gravity":"center"}]},{"type":"box","layout":"horizontal","contents":[{"type":"text","text":"%s","flex":1,"gravity":"center"},{"type":"text","text":"%s","flex":5,"gravity":"center"},{"type":"text","text":"%s","flex":1,"gravity":"center"},{"type":"text","text":"%s","flex":1,"gravity":"center"}]},{"type":"box","layout":"horizontal","contents":[{"type":"text","text":"%s","flex":1,"gravity":"center"},{"type":"text","text":"%s","flex":5,"gravity":"center"},{"type":"text","text":"%s","flex":1,"gravity":"center"},{"type":"text","text":"%s","flex":1,"gravity":"center"}]},{"type":"box","layout":"horizontal","contents":[{"type":"text","text":"%s","flex":1,"gravity":"center"},{"type":"text","text":"%s","flex":5,"gravity":"center"},{"type":"text","text":"%s","flex":1,"gravity":"center"},{"type":"text","text":"%s","flex":1,"gravity":"center"}]},{"type":"box","layout":"horizontal","contents":[{"type":"text","text":"%s","flex":1,"gravity":"center"},{"type":"text","text":"%s","flex":5,"gravity":"center"},{"type":"text","text":"%s","flex":1,"gravity":"center"},{"type":"text","text":"%s","flex":1,"gravity":"center"}]}]}]}}'''%(leagueCountry,listRankTeam[20],listTeam[20],listGamePlay[20],listPoint[20],listRankTeam[21],listTeam[21],listGamePlay[21],listPoint[21],listRankTeam[22],listTeam[22],listGamePlay[22],listPoint[22],listRankTeam[23],listTeam[23],listGamePlay[23],listPoint[23],listRankTeam[24],listTeam[24],listGamePlay[24],listPoint[24],listRankTeam[25],listTeam[25],listGamePlay[25],listPoint[25],listRankTeam[26],listTeam[26],listGamePlay[26],listPoint[26])
                tableAllPageThree = json.loads(tableAllPageThree)
                carousel_container.contents.append(tableAllPageThree)
            if count == 28:
                tableAllPageThree ='''{"type":"bubble","styles":{"header":{"backgroundColor":"#228B22"}},"header":{"type":"box","layout":"horizontal","contents":[{"type":"text","text":"League %s","color":"#FFFFFF","size":"md"}]},"body":{"type":"box","layout":"vertical","contents":[{"type":"box","layout":"vertical","margin":"xxl","spacing":"sm","contents":[{"type":"box","layout":"horizontal","contents":[{"type":"text","text":"#","weight":"bold","flex":1,"gravity":"center"},{"type":"text","text":"Team","weight":"bold","flex":5,"gravity":"center"},{"type":"text","weight":"bold","text":"P","flex":1,"gravity":"center"},{"type":"text","weight":"bold","text":"Pts","flex":1,"gravity":"center"}]},{"type":"separator","margin":"sm"},{"type":"box","layout":"horizontal","contents":[{"type":"text","text":"%s","flex":1,"gravity":"center"},{"type":"text","text":"%s","flex":5,"gravity":"center"},{"type":"text","text":"%s","flex":1,"gravity":"center"},{"type":"text","text":"%s","flex":1,"gravity":"center"}]},{"type":"box","layout":"horizontal","contents":[{"type":"text","text":"%s","flex":1,"gravity":"center"},{"type":"text","text":"%s","flex":5,"gravity":"center"},{"type":"text","text":"%s","flex":1,"gravity":"center"},{"type":"text","text":"%s","flex":1,"gravity":"center"}]},{"type":"box","layout":"horizontal","contents":[{"type":"text","text":"%s","flex":1,"gravity":"center"},{"type":"text","text":"%s","flex":5,"gravity":"center"},{"type":"text","text":"%s","flex":1,"gravity":"center"},{"type":"text","text":"%s","flex":1,"gravity":"center"}]},{"type":"box","layout":"horizontal","contents":[{"type":"text","text":"%s","flex":1,"gravity":"center"},{"type":"text","text":"%s","flex":5,"gravity":"center"},{"type":"text","text":"%s","flex":1,"gravity":"center"},{"type":"text","text":"%s","flex":1,"gravity":"center"}]},{"type":"box","layout":"horizontal","contents":[{"type":"text","text":"%s","flex":1,"gravity":"center"},{"type":"text","text":"%s","flex":5,"gravity":"center"},{"type":"text","text":"%s","flex":1,"gravity":"center"},{"type":"text","text":"%s","flex":1,"gravity":"center"}]},{"type":"box","layout":"horizontal","contents":[{"type":"text","text":"%s","flex":1,"gravity":"center"},{"type":"text","text":"%s","flex":5,"gravity":"center"},{"type":"text","text":"%s","flex":1,"gravity":"center"},{"type":"text","text":"%s","flex":1,"gravity":"center"}]},{"type":"box","layout":"horizontal","contents":[{"type":"text","text":"%s","flex":1,"gravity":"center"},{"type":"text","text":"%s","flex":5,"gravity":"center"},{"type":"text","text":"%s","flex":1,"gravity":"center"},{"type":"text","text":"%s","flex":1,"gravity":"center"}]},{"type":"box","layout":"horizontal","contents":[{"type":"text","text":"%s","flex":1,"gravity":"center"},{"type":"text","text":"%s","flex":5,"gravity":"center"},{"type":"text","text":"%s","flex":1,"gravity":"center"},{"type":"text","text":"%s","flex":1,"gravity":"center"}]}]}]}}'''%(leagueCountry,listRankTeam[20],listTeam[20],listGamePlay[20],listPoint[20],listRankTeam[21],listTeam[21],listGamePlay[21],listPoint[21],listRankTeam[22],listTeam[22],listGamePlay[22],listPoint[22],listRankTeam[23],listTeam[23],listGamePlay[23],listPoint[23],listRankTeam[24],listTeam[24],listGamePlay[24],listPoint[24],listRankTeam[25],listTeam[25],listGamePlay[25],listPoint[25],listRankTeam[26],listTeam[26],listGamePlay[26],listPoint[26],listRankTeam[27],listTeam[27],listGamePlay[27],listPoint[27])
                tableAllPageThree = json.loads(tableAllPageThree)
                carousel_container.contents.append(tableAllPageThree)
            if count == 29:
                tableAllPageThree ='''{"type":"bubble","styles":{"header":{"backgroundColor":"#228B22"}},"header":{"type":"box","layout":"horizontal","contents":[{"type":"text","text":"League %s","color":"#FFFFFF","size":"md"}]},"body":{"type":"box","layout":"vertical","contents":[{"type":"box","layout":"vertical","margin":"xxl","spacing":"sm","contents":[{"type":"box","layout":"horizontal","contents":[{"type":"text","text":"#","weight":"bold","flex":1,"gravity":"center"},{"type":"text","text":"Team","weight":"bold","flex":5,"gravity":"center"},{"type":"text","weight":"bold","text":"P","flex":1,"gravity":"center"},{"type":"text","weight":"bold","text":"Pts","flex":1,"gravity":"center"}]},{"type":"separator","margin":"sm"},{"type":"box","layout":"horizontal","contents":[{"type":"text","text":"%s","flex":1,"gravity":"center"},{"type":"text","text":"%s","flex":5,"gravity":"center"},{"type":"text","text":"%s","flex":1,"gravity":"center"},{"type":"text","text":"%s","flex":1,"gravity":"center"}]},{"type":"box","layout":"horizontal","contents":[{"type":"text","text":"%s","flex":1,"gravity":"center"},{"type":"text","text":"%s","flex":5,"gravity":"center"},{"type":"text","text":"%s","flex":1,"gravity":"center"},{"type":"text","text":"%s","flex":1,"gravity":"center"}]},{"type":"box","layout":"horizontal","contents":[{"type":"text","text":"%s","flex":1,"gravity":"center"},{"type":"text","text":"%s","flex":5,"gravity":"center"},{"type":"text","text":"%s","flex":1,"gravity":"center"},{"type":"text","text":"%s","flex":1,"gravity":"center"}]},{"type":"box","layout":"horizontal","contents":[{"type":"text","text":"%s","flex":1,"gravity":"center"},{"type":"text","text":"%s","flex":5,"gravity":"center"},{"type":"text","text":"%s","flex":1,"gravity":"center"},{"type":"text","text":"%s","flex":1,"gravity":"center"}]},{"type":"box","layout":"horizontal","contents":[{"type":"text","text":"%s","flex":1,"gravity":"center"},{"type":"text","text":"%s","flex":5,"gravity":"center"},{"type":"text","text":"%s","flex":1,"gravity":"center"},{"type":"text","text":"%s","flex":1,"gravity":"center"}]},{"type":"box","layout":"horizontal","contents":[{"type":"text","text":"%s","flex":1,"gravity":"center"},{"type":"text","text":"%s","flex":5,"gravity":"center"},{"type":"text","text":"%s","flex":1,"gravity":"center"},{"type":"text","text":"%s","flex":1,"gravity":"center"}]},{"type":"box","layout":"horizontal","contents":[{"type":"text","text":"%s","flex":1,"gravity":"center"},{"type":"text","text":"%s","flex":5,"gravity":"center"},{"type":"text","text":"%s","flex":1,"gravity":"center"},{"type":"text","text":"%s","flex":1,"gravity":"center"}]},{"type":"box","layout":"horizontal","contents":[{"type":"text","text":"%s","flex":1,"gravity":"center"},{"type":"text","text":"%s","flex":5,"gravity":"center"},{"type":"text","text":"%s","flex":1,"gravity":"center"},{"type":"text","text":"%s","flex":1,"gravity":"center"}]},{"type":"box","layout":"horizontal","contents":[{"type":"text","text":"%s","flex":1,"gravity":"center"},{"type":"text","text":"%s","flex":5,"gravity":"center"},{"type":"text","text":"%s","flex":1,"gravity":"center"},{"type":"text","text":"%s","flex":1,"gravity":"center"}]}]}]}}'''%(leagueCountry,listRankTeam[20],listTeam[20],listGamePlay[20],listPoint[20],listRankTeam[21],listTeam[21],listGamePlay[21],listPoint[21],listRankTeam[22],listTeam[22],listGamePlay[22],listPoint[22],listRankTeam[23],listTeam[23],listGamePlay[23],listPoint[23],listRankTeam[24],listTeam[24],listGamePlay[24],listPoint[24],listRankTeam[25],listTeam[25],listGamePlay[25],listPoint[25],listRankTeam[26],listTeam[26],listGamePlay[26],listPoint[26],listRankTeam[27],listTeam[27],listGamePlay[27],listPoint[27],listRankTeam[28],listTeam[28],listGamePlay[28],listPoint[28])
                tableAllPageThree = json.loads(tableAllPageThree)
                carousel_container.contents.append(tableAllPageThree)

        elif count >= 10 and count < 20:
            tableAllPageOne ='''{"type":"bubble","styles":{"header":{"backgroundColor":"#228B22"}},"header":{"type":"box","layout":"horizontal","contents":[{"type":"text","text":"League %s","color":"#FFFFFF","size":"md"}]},"body":{"type":"box","layout":"vertical","contents":[{"type":"box","layout":"vertical","margin":"xxl","spacing":"sm","contents":[{"type":"box","layout":"horizontal","contents":[{"type":"text","text":"#","weight":"bold","flex":1,"gravity":"center"},{"type":"text","text":"Team","weight":"bold","flex":5,"gravity":"center"},{"type":"text","weight":"bold","text":"P","flex":1,"gravity":"center"},{"type":"text","weight":"bold","text":"Pts","flex":1,"gravity":"center"}]},{"type":"separator","margin":"sm"},{"type":"box","layout":"horizontal","contents":[{"type":"text","text":"%s","flex":1,"gravity":"center"},{"type":"text","text":"%s","flex":5,"gravity":"center"},{"type":"text","text":"%s","flex":1,"gravity":"center"},{"type":"text","text":"%s","flex":1,"gravity":"center"}]},{"type":"box","layout":"horizontal","contents":[{"type":"text","text":"%s","flex":1,"gravity":"center"},{"type":"text","text":"%s","flex":5,"gravity":"center"},{"type":"text","text":"%s","flex":1,"gravity":"center"},{"type":"text","text":"%s","flex":1,"gravity":"center"}]},{"type":"box","layout":"horizontal","contents":[{"type":"text","text":"%s","flex":1,"gravity":"center"},{"type":"text","text":"%s","flex":5,"gravity":"center"},{"type":"text","text":"%s","flex":1,"gravity":"center"},{"type":"text","text":"%s","flex":1,"gravity":"center"}]},{"type":"box","layout":"horizontal","contents":[{"type":"text","text":"%s","flex":1,"gravity":"center"},{"type":"text","text":"%s","flex":5,"gravity":"center"},{"type":"text","text":"%s","flex":1,"gravity":"center"},{"type":"text","text":"%s","flex":1,"gravity":"center"}]},{"type":"box","layout":"horizontal","contents":[{"type":"text","text":"%s","flex":1,"gravity":"center"},{"type":"text","text":"%s","flex":5,"gravity":"center"},{"type":"text","text":"%s","flex":1,"gravity":"center"},{"type":"text","text":"%s","flex":1,"gravity":"center"}]},{"type":"box","layout":"horizontal","contents":[{"type":"text","text":"%s","flex":1,"gravity":"center"},{"type":"text","text":"%s","flex":5,"gravity":"center"},{"type":"text","text":"%s","flex":1,"gravity":"center"},{"type":"text","text":"%s","flex":1,"gravity":"center"}]},{"type":"box","layout":"horizontal","contents":[{"type":"text","text":"%s","flex":1,"gravity":"center"},{"type":"text","text":"%s","flex":5,"gravity":"center"},{"type":"text","text":"%s","flex":1,"gravity":"center"},{"type":"text","text":"%s","flex":1,"gravity":"center"}]},{"type":"box","layout":"horizontal","contents":[{"type":"text","text":"%s","flex":1,"gravity":"center"},{"type":"text","text":"%s","flex":5,"gravity":"center"},{"type":"text","text":"%s","flex":1,"gravity":"center"},{"type":"text","text":"%s","flex":1,"gravity":"center"}]},{"type":"box","layout":"horizontal","contents":[{"type":"text","text":"%s","flex":1,"gravity":"center"},{"type":"text","text":"%s","flex":5,"gravity":"center"},{"type":"text","text":"%s","flex":1,"gravity":"center"},{"type":"text","text":"%s","flex":1,"gravity":"center"}]},{"type":"box","layout":"horizontal","contents":[{"type":"text","text":"%s","flex":1,"gravity":"center"},{"type":"text","text":"%s","flex":5,"gravity":"center"},{"type":"text","text":"%s","flex":1,"gravity":"center"},{"type":"text","text":"%s","flex":1,"gravity":"center"}]}]}]}}'''%(leagueCountry,listRankTeam[0],listTeam[0],listGamePlay[0],listPoint[0],listRankTeam[1],listTeam[1],listGamePlay[1],listPoint[1],listRankTeam[2],listTeam[2],listGamePlay[2],listPoint[2],listRankTeam[3],listTeam[3],listGamePlay[3],listPoint[3],listRankTeam[4],listTeam[4],listGamePlay[4],listPoint[4],listRankTeam[5],listTeam[5],listGamePlay[5],listPoint[5],listRankTeam[6],listTeam[6],listGamePlay[6],listPoint[6],listRankTeam[7],listTeam[7],listGamePlay[7],listPoint[7],listRankTeam[8],listTeam[8],listGamePlay[8],listPoint[8],listRankTeam[9],listTeam[9],listGamePlay[9],listPoint[9])
            tableAllPageOne = json.loads(tableAllPageOne)
            carousel_container.contents.append(tableAllPageOne)
            if count == 11:
                tableAllPageTwo ='''{"type":"bubble","styles":{"header":{"backgroundColor":"#228B22"}},"header":{"type":"box","layout":"horizontal","contents":[{"type":"text","text":"League %s","color":"#FFFFFF","size":"md"}]},"body":{"type":"box","layout":"vertical","contents":[{"type":"box","layout":"vertical","margin":"xxl","spacing":"sm","contents":[{"type":"box","layout":"horizontal","contents":[{"type":"text","text":"#","weight":"bold","flex":1,"gravity":"center"},{"type":"text","text":"Team","weight":"bold","flex":5,"gravity":"center"},{"type":"text","weight":"bold","text":"P","flex":1,"gravity":"center"},{"type":"text","weight":"bold","text":"Pts","flex":1,"gravity":"center"}]},{"type":"separator","margin":"sm"},{"type":"box","layout":"horizontal","contents":[{"type":"text","text":"%s","flex":1,"gravity":"center"},{"type":"text","text":"%s","flex":5,"gravity":"center"},{"type":"text","text":"%s","flex":1,"gravity":"center"},{"type":"text","text":"%s","flex":1,"gravity":"center"}]}]}]}}'''%(leagueCountry,listRankTeam[10],listTeam[10],listGamePlay[10],listPoint[10])
                tableAllPageTwo = json.loads(tableAllPageTwo)
                carousel_container.contents.append(tableAllPageTwo)
            if count == 12:
                tableAllPageTwo ='''{"type":"bubble","styles":{"header":{"backgroundColor":"#228B22"}},"header":{"type":"box","layout":"horizontal","contents":[{"type":"text","text":"League %s","color":"#FFFFFF","size":"md"}]},"body":{"type":"box","layout":"vertical","contents":[{"type":"box","layout":"vertical","margin":"xxl","spacing":"sm","contents":[{"type":"box","layout":"horizontal","contents":[{"type":"text","text":"#","weight":"bold","flex":1,"gravity":"center"},{"type":"text","text":"Team","weight":"bold","flex":5,"gravity":"center"},{"type":"text","weight":"bold","text":"P","flex":1,"gravity":"center"},{"type":"text","weight":"bold","text":"Pts","flex":1,"gravity":"center"}]},{"type":"separator","margin":"sm"},{"type":"box","layout":"horizontal","contents":[{"type":"text","text":"%s","flex":1,"gravity":"center"},{"type":"text","text":"%s","flex":5,"gravity":"center"},{"type":"text","text":"%s","flex":1,"gravity":"center"},{"type":"text","text":"%s","flex":1,"gravity":"center"}]},{"type":"box","layout":"horizontal","contents":[{"type":"text","text":"%s","flex":1,"gravity":"center"},{"type":"text","text":"%s","flex":5,"gravity":"center"},{"type":"text","text":"%s","flex":1,"gravity":"center"},{"type":"text","text":"%s","flex":1,"gravity":"center"}]}]}]}}'''%(leagueCountry,listRankTeam[10],listTeam[10],listGamePlay[10],listPoint[10],listRankTeam[11],listTeam[11],listGamePlay[11],listPoint[11])
                tableAllPageTwo = json.loads(tableAllPageTwo)
                carousel_container.contents.append(tableAllPageTwo)
            if count == 13:
                tableAllPageTwo ='''{"type":"bubble","styles":{"header":{"backgroundColor":"#228B22"}},"header":{"type":"box","layout":"horizontal","contents":[{"type":"text","text":"League %s","color":"#FFFFFF","size":"md"}]},"body":{"type":"box","layout":"vertical","contents":[{"type":"box","layout":"vertical","margin":"xxl","spacing":"sm","contents":[{"type":"box","layout":"horizontal","contents":[{"type":"text","text":"#","weight":"bold","flex":1,"gravity":"center"},{"type":"text","text":"Team","weight":"bold","flex":5,"gravity":"center"},{"type":"text","weight":"bold","text":"P","flex":1,"gravity":"center"},{"type":"text","weight":"bold","text":"Pts","flex":1,"gravity":"center"}]},{"type":"separator","margin":"sm"},{"type":"box","layout":"horizontal","contents":[{"type":"text","text":"%s","flex":1,"gravity":"center"},{"type":"text","text":"%s","flex":5,"gravity":"center"},{"type":"text","text":"%s","flex":1,"gravity":"center"},{"type":"text","text":"%s","flex":1,"gravity":"center"}]},{"type":"box","layout":"horizontal","contents":[{"type":"text","text":"%s","flex":1,"gravity":"center"},{"type":"text","text":"%s","flex":5,"gravity":"center"},{"type":"text","text":"%s","flex":1,"gravity":"center"},{"type":"text","text":"%s","flex":1,"gravity":"center"}]},{"type":"box","layout":"horizontal","contents":[{"type":"text","text":"%s","flex":1,"gravity":"center"},{"type":"text","text":"%s","flex":5,"gravity":"center"},{"type":"text","text":"%s","flex":1,"gravity":"center"},{"type":"text","text":"%s","flex":1,"gravity":"center"}]}]}]}}'''%(leagueCountry,listRankTeam[10],listTeam[10],listGamePlay[10],listPoint[10],listRankTeam[11],listTeam[11],listGamePlay[11],listPoint[11],listRankTeam[12],listTeam[12],listGamePlay[12],listPoint[12])
                tableAllPageTwo = json.loads(tableAllPageTwo)
                carousel_container.contents.append(tableAllPageTwo)
            if count == 14:
                tableAllPageTwo ='''{"type":"bubble","styles":{"header":{"backgroundColor":"#228B22"}},"header":{"type":"box","layout":"horizontal","contents":[{"type":"text","text":"League %s","color":"#FFFFFF","size":"md"}]},"body":{"type":"box","layout":"vertical","contents":[{"type":"box","layout":"vertical","margin":"xxl","spacing":"sm","contents":[{"type":"box","layout":"horizontal","contents":[{"type":"text","text":"#","weight":"bold","flex":1,"gravity":"center"},{"type":"text","text":"Team","weight":"bold","flex":5,"gravity":"center"},{"type":"text","weight":"bold","text":"P","flex":1,"gravity":"center"},{"type":"text","weight":"bold","text":"Pts","flex":1,"gravity":"center"}]},{"type":"separator","margin":"sm"},{"type":"box","layout":"horizontal","contents":[{"type":"text","text":"%s","flex":1,"gravity":"center"},{"type":"text","text":"%s","flex":5,"gravity":"center"},{"type":"text","text":"%s","flex":1,"gravity":"center"},{"type":"text","text":"%s","flex":1,"gravity":"center"}]},{"type":"box","layout":"horizontal","contents":[{"type":"text","text":"%s","flex":1,"gravity":"center"},{"type":"text","text":"%s","flex":5,"gravity":"center"},{"type":"text","text":"%s","flex":1,"gravity":"center"},{"type":"text","text":"%s","flex":1,"gravity":"center"}]},{"type":"box","layout":"horizontal","contents":[{"type":"text","text":"%s","flex":1,"gravity":"center"},{"type":"text","text":"%s","flex":5,"gravity":"center"},{"type":"text","text":"%s","flex":1,"gravity":"center"},{"type":"text","text":"%s","flex":1,"gravity":"center"}]},{"type":"box","layout":"horizontal","contents":[{"type":"text","text":"%s","flex":1,"gravity":"center"},{"type":"text","text":"%s","flex":5,"gravity":"center"},{"type":"text","text":"%s","flex":1,"gravity":"center"},{"type":"text","text":"%s","flex":1,"gravity":"center"}]}]}]}}'''%(leagueCountry,listRankTeam[10],listTeam[10],listGamePlay[10],listPoint[10],listRankTeam[11],listTeam[11],listGamePlay[11],listPoint[11],listRankTeam[12],listTeam[12],listGamePlay[12],listPoint[12],listRankTeam[13],listTeam[13],listGamePlay[13],listPoint[13])
                tableAllPageTwo = json.loads(tableAllPageTwo)
                carousel_container.contents.append(tableAllPageTwo)
            if count == 15:
                tableAllPageTwo ='''{"type":"bubble","styles":{"header":{"backgroundColor":"#228B22"}},"header":{"type":"box","layout":"horizontal","contents":[{"type":"text","text":"League %s","color":"#FFFFFF","size":"md"}]},"body":{"type":"box","layout":"vertical","contents":[{"type":"box","layout":"vertical","margin":"xxl","spacing":"sm","contents":[{"type":"box","layout":"horizontal","contents":[{"type":"text","text":"#","weight":"bold","flex":1,"gravity":"center"},{"type":"text","text":"Team","weight":"bold","flex":5,"gravity":"center"},{"type":"text","weight":"bold","text":"P","flex":1,"gravity":"center"},{"type":"text","weight":"bold","text":"Pts","flex":1,"gravity":"center"}]},{"type":"separator","margin":"sm"},{"type":"box","layout":"horizontal","contents":[{"type":"text","text":"%s","flex":1,"gravity":"center"},{"type":"text","text":"%s","flex":5,"gravity":"center"},{"type":"text","text":"%s","flex":1,"gravity":"center"},{"type":"text","text":"%s","flex":1,"gravity":"center"}]},{"type":"box","layout":"horizontal","contents":[{"type":"text","text":"%s","flex":1,"gravity":"center"},{"type":"text","text":"%s","flex":5,"gravity":"center"},{"type":"text","text":"%s","flex":1,"gravity":"center"},{"type":"text","text":"%s","flex":1,"gravity":"center"}]},{"type":"box","layout":"horizontal","contents":[{"type":"text","text":"%s","flex":1,"gravity":"center"},{"type":"text","text":"%s","flex":5,"gravity":"center"},{"type":"text","text":"%s","flex":1,"gravity":"center"},{"type":"text","text":"%s","flex":1,"gravity":"center"}]},{"type":"box","layout":"horizontal","contents":[{"type":"text","text":"%s","flex":1,"gravity":"center"},{"type":"text","text":"%s","flex":5,"gravity":"center"},{"type":"text","text":"%s","flex":1,"gravity":"center"},{"type":"text","text":"%s","flex":1,"gravity":"center"}]},{"type":"box","layout":"horizontal","contents":[{"type":"text","text":"%s","flex":1,"gravity":"center"},{"type":"text","text":"%s","flex":5,"gravity":"center"},{"type":"text","text":"%s","flex":1,"gravity":"center"},{"type":"text","text":"%s","flex":1,"gravity":"center"}]}]}]}}'''%(leagueCountry,listRankTeam[10],listTeam[10],listGamePlay[10],listPoint[10],listRankTeam[11],listTeam[11],listGamePlay[11],listPoint[11],listRankTeam[12],listTeam[12],listGamePlay[12],listPoint[12],listRankTeam[13],listTeam[13],listGamePlay[13],listPoint[13],listRankTeam[14],listTeam[14],listGamePlay[14],listPoint[14])
                tableAllPageTwo = json.loads(tableAllPageTwo)
                carousel_container.contents.append(tableAllPageTwo)
            if count == 16:
                tableAllPageTwo ='''{"type":"bubble","styles":{"header":{"backgroundColor":"#228B22"}},"header":{"type":"box","layout":"horizontal","contents":[{"type":"text","text":"League %s","color":"#FFFFFF","size":"md"}]},"body":{"type":"box","layout":"vertical","contents":[{"type":"box","layout":"vertical","margin":"xxl","spacing":"sm","contents":[{"type":"box","layout":"horizontal","contents":[{"type":"text","text":"#","weight":"bold","flex":1,"gravity":"center"},{"type":"text","text":"Team","weight":"bold","flex":5,"gravity":"center"},{"type":"text","weight":"bold","text":"P","flex":1,"gravity":"center"},{"type":"text","weight":"bold","text":"Pts","flex":1,"gravity":"center"}]},{"type":"separator","margin":"sm"},{"type":"box","layout":"horizontal","contents":[{"type":"text","text":"%s","flex":1,"gravity":"center"},{"type":"text","text":"%s","flex":5,"gravity":"center"},{"type":"text","text":"%s","flex":1,"gravity":"center"},{"type":"text","text":"%s","flex":1,"gravity":"center"}]},{"type":"box","layout":"horizontal","contents":[{"type":"text","text":"%s","flex":1,"gravity":"center"},{"type":"text","text":"%s","flex":5,"gravity":"center"},{"type":"text","text":"%s","flex":1,"gravity":"center"},{"type":"text","text":"%s","flex":1,"gravity":"center"}]},{"type":"box","layout":"horizontal","contents":[{"type":"text","text":"%s","flex":1,"gravity":"center"},{"type":"text","text":"%s","flex":5,"gravity":"center"},{"type":"text","text":"%s","flex":1,"gravity":"center"},{"type":"text","text":"%s","flex":1,"gravity":"center"}]},{"type":"box","layout":"horizontal","contents":[{"type":"text","text":"%s","flex":1,"gravity":"center"},{"type":"text","text":"%s","flex":5,"gravity":"center"},{"type":"text","text":"%s","flex":1,"gravity":"center"},{"type":"text","text":"%s","flex":1,"gravity":"center"}]},{"type":"box","layout":"horizontal","contents":[{"type":"text","text":"%s","flex":1,"gravity":"center"},{"type":"text","text":"%s","flex":5,"gravity":"center"},{"type":"text","text":"%s","flex":1,"gravity":"center"},{"type":"text","text":"%s","flex":1,"gravity":"center"}]},{"type":"box","layout":"horizontal","contents":[{"type":"text","text":"%s","flex":1,"gravity":"center"},{"type":"text","text":"%s","flex":5,"gravity":"center"},{"type":"text","text":"%s","flex":1,"gravity":"center"},{"type":"text","text":"%s","flex":1,"gravity":"center"}]}]}]}}'''%(leagueCountry,listRankTeam[10],listTeam[10],listGamePlay[10],listPoint[10],listRankTeam[11],listTeam[11],listGamePlay[11],listPoint[11],listRankTeam[12],listTeam[12],listGamePlay[12],listPoint[12],listRankTeam[13],listTeam[13],listGamePlay[13],listPoint[13],listRankTeam[14],listTeam[14],listGamePlay[14],listPoint[14],listRankTeam[15],listTeam[15],listGamePlay[15],listPoint[15])
                tableAllPageTwo = json.loads(tableAllPageTwo)
                carousel_container.contents.append(tableAllPageTwo)
            if count == 17:
                tableAllPageTwo ='''{"type":"bubble","styles":{"header":{"backgroundColor":"#228B22"}},"header":{"type":"box","layout":"horizontal","contents":[{"type":"text","text":"League %s","color":"#FFFFFF","size":"md"}]},"body":{"type":"box","layout":"vertical","contents":[{"type":"box","layout":"vertical","margin":"xxl","spacing":"sm","contents":[{"type":"box","layout":"horizontal","contents":[{"type":"text","text":"#","weight":"bold","flex":1,"gravity":"center"},{"type":"text","text":"Team","weight":"bold","flex":5,"gravity":"center"},{"type":"text","weight":"bold","text":"P","flex":1,"gravity":"center"},{"type":"text","weight":"bold","text":"Pts","flex":1,"gravity":"center"}]},{"type":"separator","margin":"sm"},{"type":"box","layout":"horizontal","contents":[{"type":"text","text":"%s","flex":1,"gravity":"center"},{"type":"text","text":"%s","flex":5,"gravity":"center"},{"type":"text","text":"%s","flex":1,"gravity":"center"},{"type":"text","text":"%s","flex":1,"gravity":"center"}]},{"type":"box","layout":"horizontal","contents":[{"type":"text","text":"%s","flex":1,"gravity":"center"},{"type":"text","text":"%s","flex":5,"gravity":"center"},{"type":"text","text":"%s","flex":1,"gravity":"center"},{"type":"text","text":"%s","flex":1,"gravity":"center"}]},{"type":"box","layout":"horizontal","contents":[{"type":"text","text":"%s","flex":1,"gravity":"center"},{"type":"text","text":"%s","flex":5,"gravity":"center"},{"type":"text","text":"%s","flex":1,"gravity":"center"},{"type":"text","text":"%s","flex":1,"gravity":"center"}]},{"type":"box","layout":"horizontal","contents":[{"type":"text","text":"%s","flex":1,"gravity":"center"},{"type":"text","text":"%s","flex":5,"gravity":"center"},{"type":"text","text":"%s","flex":1,"gravity":"center"},{"type":"text","text":"%s","flex":1,"gravity":"center"}]},{"type":"box","layout":"horizontal","contents":[{"type":"text","text":"%s","flex":1,"gravity":"center"},{"type":"text","text":"%s","flex":5,"gravity":"center"},{"type":"text","text":"%s","flex":1,"gravity":"center"},{"type":"text","text":"%s","flex":1,"gravity":"center"}]},{"type":"box","layout":"horizontal","contents":[{"type":"text","text":"%s","flex":1,"gravity":"center"},{"type":"text","text":"%s","flex":5,"gravity":"center"},{"type":"text","text":"%s","flex":1,"gravity":"center"},{"type":"text","text":"%s","flex":1,"gravity":"center"}]},{"type":"box","layout":"horizontal","contents":[{"type":"text","text":"%s","flex":1,"gravity":"center"},{"type":"text","text":"%s","flex":5,"gravity":"center"},{"type":"text","text":"%s","flex":1,"gravity":"center"},{"type":"text","text":"%s","flex":1,"gravity":"center"}]}]}]}}'''%(leagueCountry,listRankTeam[10],listTeam[10],listGamePlay[10],listPoint[10],listRankTeam[11],listTeam[11],listGamePlay[11],listPoint[11],listRankTeam[12],listTeam[12],listGamePlay[12],listPoint[12],listRankTeam[13],listTeam[13],listGamePlay[13],listPoint[13],listRankTeam[14],listTeam[14],listGamePlay[14],listPoint[14],listRankTeam[15],listTeam[15],listGamePlay[15],listPoint[15],listRankTeam[16],listTeam[16],listGamePlay[16],listPoint[16])
                tableAllPageTwo = json.loads(tableAllPageTwo)
                carousel_container.contents.append(tableAllPageTwo)
            if count == 18:
                tableAllPageTwo ='''{"type":"bubble","styles":{"header":{"backgroundColor":"#228B22"}},"header":{"type":"box","layout":"horizontal","contents":[{"type":"text","text":"League %s","color":"#FFFFFF","size":"md"}]},"body":{"type":"box","layout":"vertical","contents":[{"type":"box","layout":"vertical","margin":"xxl","spacing":"sm","contents":[{"type":"box","layout":"horizontal","contents":[{"type":"text","text":"#","weight":"bold","flex":1,"gravity":"center"},{"type":"text","text":"Team","weight":"bold","flex":5,"gravity":"center"},{"type":"text","weight":"bold","text":"P","flex":1,"gravity":"center"},{"type":"text","weight":"bold","text":"Pts","flex":1,"gravity":"center"}]},{"type":"separator","margin":"sm"},{"type":"box","layout":"horizontal","contents":[{"type":"text","text":"%s","flex":1,"gravity":"center"},{"type":"text","text":"%s","flex":5,"gravity":"center"},{"type":"text","text":"%s","flex":1,"gravity":"center"},{"type":"text","text":"%s","flex":1,"gravity":"center"}]},{"type":"box","layout":"horizontal","contents":[{"type":"text","text":"%s","flex":1,"gravity":"center"},{"type":"text","text":"%s","flex":5,"gravity":"center"},{"type":"text","text":"%s","flex":1,"gravity":"center"},{"type":"text","text":"%s","flex":1,"gravity":"center"}]},{"type":"box","layout":"horizontal","contents":[{"type":"text","text":"%s","flex":1,"gravity":"center"},{"type":"text","text":"%s","flex":5,"gravity":"center"},{"type":"text","text":"%s","flex":1,"gravity":"center"},{"type":"text","text":"%s","flex":1,"gravity":"center"}]},{"type":"box","layout":"horizontal","contents":[{"type":"text","text":"%s","flex":1,"gravity":"center"},{"type":"text","text":"%s","flex":5,"gravity":"center"},{"type":"text","text":"%s","flex":1,"gravity":"center"},{"type":"text","text":"%s","flex":1,"gravity":"center"}]},{"type":"box","layout":"horizontal","contents":[{"type":"text","text":"%s","flex":1,"gravity":"center"},{"type":"text","text":"%s","flex":5,"gravity":"center"},{"type":"text","text":"%s","flex":1,"gravity":"center"},{"type":"text","text":"%s","flex":1,"gravity":"center"}]},{"type":"box","layout":"horizontal","contents":[{"type":"text","text":"%s","flex":1,"gravity":"center"},{"type":"text","text":"%s","flex":5,"gravity":"center"},{"type":"text","text":"%s","flex":1,"gravity":"center"},{"type":"text","text":"%s","flex":1,"gravity":"center"}]},{"type":"box","layout":"horizontal","contents":[{"type":"text","text":"%s","flex":1,"gravity":"center"},{"type":"text","text":"%s","flex":5,"gravity":"center"},{"type":"text","text":"%s","flex":1,"gravity":"center"},{"type":"text","text":"%s","flex":1,"gravity":"center"}]},{"type":"box","layout":"horizontal","contents":[{"type":"text","text":"%s","flex":1,"gravity":"center"},{"type":"text","text":"%s","flex":5,"gravity":"center"},{"type":"text","text":"%s","flex":1,"gravity":"center"},{"type":"text","text":"%s","flex":1,"gravity":"center"}]}]}]}}'''%(leagueCountry,listRankTeam[10],listTeam[10],listGamePlay[10],listPoint[10],listRankTeam[11],listTeam[11],listGamePlay[11],listPoint[11],listRankTeam[12],listTeam[12],listGamePlay[12],listPoint[12],listRankTeam[13],listTeam[13],listGamePlay[13],listPoint[13],listRankTeam[14],listTeam[14],listGamePlay[14],listPoint[14],listRankTeam[15],listTeam[15],listGamePlay[15],listPoint[15],listRankTeam[16],listTeam[16],listGamePlay[16],listPoint[16],listRankTeam[17],listTeam[17],listGamePlay[17],listPoint[17])
                tableAllPageTwo = json.loads(tableAllPageTwo)
                carousel_container.contents.append(tableAllPageTwo)
            if count == 19:
                tableAllPageTwo ='''{"type":"bubble","styles":{"header":{"backgroundColor":"#228B22"}},"header":{"type":"box","layout":"horizontal","contents":[{"type":"text","text":"League %s","color":"#FFFFFF","size":"md"}]},"body":{"type":"box","layout":"vertical","contents":[{"type":"box","layout":"vertical","margin":"xxl","spacing":"sm","contents":[{"type":"box","layout":"horizontal","contents":[{"type":"text","text":"#","weight":"bold","flex":1,"gravity":"center"},{"type":"text","text":"Team","weight":"bold","flex":5,"gravity":"center"},{"type":"text","weight":"bold","text":"P","flex":1,"gravity":"center"},{"type":"text","weight":"bold","text":"Pts","flex":1,"gravity":"center"}]},{"type":"separator","margin":"sm"},{"type":"box","layout":"horizontal","contents":[{"type":"text","text":"%s","flex":1,"gravity":"center"},{"type":"text","text":"%s","flex":5,"gravity":"center"},{"type":"text","text":"%s","flex":1,"gravity":"center"},{"type":"text","text":"%s","flex":1,"gravity":"center"}]},{"type":"box","layout":"horizontal","contents":[{"type":"text","text":"%s","flex":1,"gravity":"center"},{"type":"text","text":"%s","flex":5,"gravity":"center"},{"type":"text","text":"%s","flex":1,"gravity":"center"},{"type":"text","text":"%s","flex":1,"gravity":"center"}]},{"type":"box","layout":"horizontal","contents":[{"type":"text","text":"%s","flex":1,"gravity":"center"},{"type":"text","text":"%s","flex":5,"gravity":"center"},{"type":"text","text":"%s","flex":1,"gravity":"center"},{"type":"text","text":"%s","flex":1,"gravity":"center"}]},{"type":"box","layout":"horizontal","contents":[{"type":"text","text":"%s","flex":1,"gravity":"center"},{"type":"text","text":"%s","flex":5,"gravity":"center"},{"type":"text","text":"%s","flex":1,"gravity":"center"},{"type":"text","text":"%s","flex":1,"gravity":"center"}]},{"type":"box","layout":"horizontal","contents":[{"type":"text","text":"%s","flex":1,"gravity":"center"},{"type":"text","text":"%s","flex":5,"gravity":"center"},{"type":"text","text":"%s","flex":1,"gravity":"center"},{"type":"text","text":"%s","flex":1,"gravity":"center"}]},{"type":"box","layout":"horizontal","contents":[{"type":"text","text":"%s","flex":1,"gravity":"center"},{"type":"text","text":"%s","flex":5,"gravity":"center"},{"type":"text","text":"%s","flex":1,"gravity":"center"},{"type":"text","text":"%s","flex":1,"gravity":"center"}]},{"type":"box","layout":"horizontal","contents":[{"type":"text","text":"%s","flex":1,"gravity":"center"},{"type":"text","text":"%s","flex":5,"gravity":"center"},{"type":"text","text":"%s","flex":1,"gravity":"center"},{"type":"text","text":"%s","flex":1,"gravity":"center"}]},{"type":"box","layout":"horizontal","contents":[{"type":"text","text":"%s","flex":1,"gravity":"center"},{"type":"text","text":"%s","flex":5,"gravity":"center"},{"type":"text","text":"%s","flex":1,"gravity":"center"},{"type":"text","text":"%s","flex":1,"gravity":"center"}]},{"type":"box","layout":"horizontal","contents":[{"type":"text","text":"%s","flex":1,"gravity":"center"},{"type":"text","text":"%s","flex":5,"gravity":"center"},{"type":"text","text":"%s","flex":1,"gravity":"center"},{"type":"text","text":"%s","flex":1,"gravity":"center"}]}]}]}}'''%(leagueCountry,listRankTeam[10],listTeam[10],listGamePlay[10],listPoint[10],listRankTeam[11],listTeam[11],listGamePlay[11],listPoint[11],listRankTeam[12],listTeam[12],listGamePlay[12],listPoint[12],listRankTeam[13],listTeam[13],listGamePlay[13],listPoint[13],listRankTeam[14],listTeam[14],listGamePlay[14],listPoint[14],listRankTeam[15],listTeam[15],listGamePlay[15],listPoint[15],listRankTeam[16],listTeam[16],listGamePlay[16],listPoint[16],listRankTeam[17],listTeam[17],listGamePlay[17],listPoint[17],listRankTeam[18],listTeam[18],listGamePlay[18],listPoint[18])
                tableAllPageTwo = json.loads(tableAllPageTwo)
                carousel_container.contents.append(tableAllPageTwo)
        line_bot_api.reply_message(event.reply_token, FlexSendMessage(alt_text='Fixtures', contents=carousel_container))
# (--------------------------------------------------ball cup-------------------------------------------------)
    if event.message.text[:6] == 'CupAll':
        bubble = BubbleContainer(
            direction='ltr',
            hero=ImageComponent(
                url='https://www.928betwin.com/wp-content/uploads/2017/03/%E0%B8%A3%E0%B8%B2%E0%B8%84%E0%B8%B2%E0%B8%9A%E0%B8%AD%E0%B8%A5%E0%B8%95%E0%B9%88%E0%B8%AD.jpg',
                size='full',
                aspect_ratio='20:13',
                aspect_mode='cover',
                action=URIAction(uri='http://example.com', label='label')
            ),
            body=BoxComponent(
                layout='vertical',
                contents=[
                    TextComponent(text='news football all', weight='bold', size='xl'),
                ],
            ),
            footer=BoxComponent(
                layout='vertical',
                spacing='sm',
                contents=[
                    SpacerComponent(size='sm'),
                    ButtonComponent(
                        style='primary',
                        height='sm',
                        action=MessageAction(label='AFC-Asian-Cup', text='Cup AFC-Asian-Cup'),
                    ),
                    ButtonComponent(
                        style='primary',
                        height='sm',
                        action=MessageAction(label='UEFA-Champions-League', text='Cup UEFA-Champions-League'),
                    ),
                    ButtonComponent(
                        style='primary',
                        height='sm',
                        action=MessageAction(label='UEFA-Europa-League', text='Cup UEFA-Europa-League'),
                    ),
                    ButtonComponent(
                        style='primary',
                        height='sm',
                        action=MessageAction(label='African-Nations-Cup-Qualifying', text='Cup African-Nations-Cup-Qualifying'),
                    )
                ]
            ),
        )
        message = FlexSendMessage(alt_text="hello", contents=bubble)
        line_bot_api.reply_message(
            event.reply_token,
            message
        )

    carousel_container = CarouselContainer()
    if event.message.text[:4] == 'Cup ':
        splitLeagueCup = event.message.text.split(" ")
        categoryCup = splitLeagueCup[1]
        apiNameLeague = ('https://scrape-football-cup.herokuapp.com/cup?leagueName={}').format(categoryCup)
        allDataLinkCup = requests.get(apiNameLeague).json()
        listGroup = allDataLinkCup[0]
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
        if categoryCup in 'AFC-Asian-Cup':
            listTopPage = ['GroupA','GroupC','GroupE']
            lengthGroupTop = len(listTopPage)
            # print(lengthGroupTop)
            listButtomPage = ['GroupB','GroupD','GroupF']
            lengthGroupBottom = len(listButtomPage)

        elif categoryCup in 'UEFA-Champions-League':
            listTopPage = ['GroupA','GroupC','GroupE','GroupG']
            lengthGroupTop = len(listTopPage)
            # print(lengthGroupTop)
            listButtomPage = ['GroupB','GroupD','GroupF','GroupH']
            lengthGroupBottom = len(listButtomPage)
        elif categoryCup in 'UEFA-Europa-League' or 'African-Nations-Cup-Qualifying':      
            listTopPage = ['GroupA','GroupC','GroupE','GroupG','GroupI','GroupK']
            lengthGroupTop = len(listTopPage)
            # print(lengthGroupTop)
            listButtomPage = ['GroupB','GroupD','GroupF','GroupH','GroupJ','GroupL']
            lengthGroupBottom = len(listButtomPage)
            print(lengthGroupBottom)
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
            tableGroupTop = '''{"type":"bubble","styles":{"header":{"backgroundColor":"#228B22"}},"header":{"type":"box","layout":"horizontal","contents":[{"type":"text","text":"%s","color":"#FFFFFF","size":"lg"}]},"body":{"type":"box","layout":"vertical","contents":[{"type":"box","layout":"vertical","margin":"xxl","spacing":"sm","contents":[{"type":"text","text":"%s","size":"lg"},{"type":"separator","margin":"sm"},{"type":"box","layout":"horizontal","contents":[{"type":"text","text":"#","weight":"bold","flex":1,"gravity":"center"},{"type":"text","text":"Team","weight":"bold","flex":5,"gravity":"center"},{"type":"text","weight":"bold","text":"P","flex":1,"gravity":"center"},{"type":"text","weight":"bold","text":"W","flex":1,"gravity":"center"},{"type":"text","weight":"bold","text":"D","flex":1,"gravity":"center"},{"type":"text","weight":"bold","text":"L","flex":1,"gravity":"center"},{"type":"text","weight":"bold","text":"Pt","flex":1,"gravity":"center"}]},{"type":"separator","margin":"sm"},{"type":"box","layout":"horizontal","contents":[{"type":"text","text":"%s","flex":1,"gravity":"center"},{"type":"text","text":"%s","flex":5,"gravity":"center"},{"type":"text","text":"%s","flex":1,"gravity":"center"},{"type":"text","text":"%s","flex":1,"gravity":"center"},{"type":"text","text":"%s","flex":1,"gravity":"center"},{"type":"text","text":"%s","flex":1,"gravity":"center"},{"type":"text","text":"%s","flex":1,"gravity":"center"}]},{"type":"box","layout":"horizontal","contents":[{"type":"text","text":"%s","flex":1,"gravity":"center"},{"type":"text","text":"%s","flex":5,"gravity":"center"},{"type":"text","text":"%s","flex":1,"gravity":"center"},{"type":"text","text":"%s","flex":1,"gravity":"center"},{"type":"text","text":"%s","flex":1,"gravity":"center"},{"type":"text","text":"%s","flex":1,"gravity":"center"},{"type":"text","text":"%s","flex":1,"gravity":"center"}]},{"type":"box","layout":"horizontal","contents":[{"type":"text","text":"%s","flex":1,"gravity":"center"},{"type":"text","text":"%s","flex":5,"gravity":"center"},{"type":"text","text":"%s","flex":1,"gravity":"center"},{"type":"text","text":"%s","flex":1,"gravity":"center"},{"type":"text","text":"%s","flex":1,"gravity":"center"},{"type":"text","text":"%s","flex":1,"gravity":"center"},{"type":"text","text":"%s","flex":1,"gravity":"center"}]},{"type":"box","layout":"horizontal","contents":[{"type":"text","text":"%s","flex":1,"gravity":"center"},{"type":"text","text":"%s","flex":5,"gravity":"center"},{"type":"text","text":"%s","flex":1,"gravity":"center"},{"type":"text","text":"%s","flex":1,"gravity":"center"},{"type":"text","text":"%s","flex":1,"gravity":"center"},{"type":"text","text":"%s","flex":1,"gravity":"center"},{"type":"text","text":"%s","flex":1,"gravity":"center"}]}]},{"type":"separator","margin":"xl"},{"type":"box","layout":"vertical","margin":"xxl","spacing":"sm","contents":[{"type":"text","text":"%s","size":"lg"},{"type":"separator","margin":"sm"},{"type":"box","layout":"horizontal","contents":[{"type":"text","text":"#","weight":"bold","flex":1,"gravity":"center"},{"type":"text","text":"Team","weight":"bold","flex":5,"gravity":"center"},{"type":"text","weight":"bold","text":"P","flex":1,"gravity":"center"},{"type":"text","weight":"bold","text":"W","flex":1,"gravity":"center"},{"type":"text","weight":"bold","text":"D","flex":1,"gravity":"center"},{"type":"text","weight":"bold","text":"L","flex":1,"gravity":"center"},{"type":"text","weight":"bold","text":"Pt","flex":1,"gravity":"center"}]},{"type":"separator","margin":"sm"},{"type":"box","layout":"horizontal","contents":[{"type":"text","text":"%s","flex":1,"gravity":"center"},{"type":"text","text":"%s","flex":5,"gravity":"center"},{"type":"text","text":"%s","flex":1,"gravity":"center"},{"type":"text","text":"%s","flex":1,"gravity":"center"},{"type":"text","text":"%s","flex":1,"gravity":"center"},{"type":"text","text":"%s","flex":1,"gravity":"center"},{"type":"text","text":"%s","flex":1,"gravity":"center"}]},{"type":"box","layout":"horizontal","contents":[{"type":"text","text":"%s","flex":1,"gravity":"center"},{"type":"text","text":"%s","flex":5,"gravity":"center"},{"type":"text","text":"%s","flex":1,"gravity":"center"},{"type":"text","text":"%s","flex":1,"gravity":"center"},{"type":"text","text":"%s","flex":1,"gravity":"center"},{"type":"text","text":"%s","flex":1,"gravity":"center"},{"type":"text","text":"%s","flex":1,"gravity":"center"}]},{"type":"box","layout":"horizontal","contents":[{"type":"text","text":"%s","flex":1,"gravity":"center"},{"type":"text","text":"%s","flex":5,"gravity":"center"},{"type":"text","text":"%s","flex":1,"gravity":"center"},{"type":"text","text":"%s","flex":1,"gravity":"center"},{"type":"text","text":"%s","flex":1,"gravity":"center"},{"type":"text","text":"%s","flex":1,"gravity":"center"},{"type":"text","text":"%s","flex":1,"gravity":"center"}]},{"type":"box","layout":"horizontal","contents":[{"type":"text","text":"%s","flex":1,"gravity":"center"},{"type":"text","text":"%s","flex":5,"gravity":"center"},{"type":"text","text":"%s","flex":1,"gravity":"center"},{"type":"text","text":"%s","flex":1,"gravity":"center"},{"type":"text","text":"%s","flex":1,"gravity":"center"},{"type":"text","text":"%s","flex":1,"gravity":"center"},{"type":"text","text":"%s","flex":1,"gravity":"center"}]}]}]}}'''%(categoryCup,listTopPage[elementBubble],RankGroupOneTop[elementBubble],teamGroupOneTop[elementBubble],GamePlayGroupOneTop[elementBubble],winsGroupOneTop[elementBubble],drawGroupOneTop[elementBubble],lossesGroupOneTop[elementBubble],pointGroupOneTop[elementBubble],            
            RankGroupTwoTop[elementBubble],teamGroupTwoTop[elementBubble],GamePlayGroupTwoTop[elementBubble],winsGroupTwoTop[elementBubble],drawGroupTwoTop[elementBubble],lossesGroupTwoTop[elementBubble],pointGroupTwoTop[elementBubble],
            RankGroupThreeTop[elementBubble],teamGroupThreeTop[elementBubble],GamePlayGroupThreeTop[elementBubble],winsGroupThreeTop[elementBubble],drawGroupThreeTop[elementBubble],lossesGroupThreeTop[elementBubble],pointGroupThreeTop[elementBubble],
            RankGroupFourTop[elementBubble],teamGroupFourTop[elementBubble],GamePlayGroupFourTop[elementBubble],winsGroupFourTop[elementBubble],drawGroupFourTop[elementBubble],lossesGroupFourTop[elementBubble],pointGroupFourTop[elementBubble],            
            listButtomPage[elementBubble],RankGroupOne[elementBubble],teamGroupOne[elementBubble],GamePlayGroupOne[elementBubble],winsGroupOne[elementBubble],drawGroupOne[elementBubble],lossesGroupOne[elementBubble],pointGroupOne[elementBubble],
            RankGroupTwo[elementBubble],teamGroupTwo[elementBubble],GamePlayGroupTwo[elementBubble],winsGroupTwo[elementBubble],drawGroupTwo[elementBubble],lossesGroupTwo[elementBubble],pointGroupTwo[elementBubble],
            RankGroupThree[elementBubble],teamGroupThree[elementBubble],GamePlayGroupThree[elementBubble],winsGroupThree[elementBubble],drawGroupThree[elementBubble],lossesGroupThree[elementBubble],pointGroupThree[elementBubble],
            RankGroupFour[elementBubble],teamGroupFour[elementBubble],GamePlayGroupFour[elementBubble],winsGroupFour[elementBubble],drawGroupFour[elementBubble],lossesGroupFour[elementBubble],pointGroupFour[elementBubble])
            tableGroupTop = json.loads(tableGroupTop)
            carousel_container.contents.append(tableGroupTop)
        line_bot_api.reply_message(event.reply_token, FlexSendMessage(alt_text='Fixtures', contents=carousel_container))
        # (--------------------------------------------------News Thai-------------------------------------------------)
    if event.message.text[:7] == 'NewsAll':
        bubble = BubbleContainer(
            direction='ltr',
            hero=ImageComponent(
                url='https://www.928betwin.com/wp-content/uploads/2017/03/%E0%B8%A3%E0%B8%B2%E0%B8%84%E0%B8%B2%E0%B8%9A%E0%B8%AD%E0%B8%A5%E0%B8%95%E0%B9%88%E0%B8%AD.jpg',
                size='full',
                aspect_ratio='20:13',
                aspect_mode='cover',
                action=URIAction(uri='http://example.com', label='label')
            ),
            body=BoxComponent(
                layout='vertical',
                contents=[
                    TextComponent(text='news category', weight='bold', size='xl'),
                ],
            ),
            footer=BoxComponent(
                layout='vertical',
                spacing='sm',
                contents=[
                    SpacerComponent(size='sm'),
                    ButtonComponent(
                        style='primary',
                        height='sm',
                        action=MessageAction(label='News England', text='News England'),
                    ),
                    ButtonComponent(
                        style='primary',
                        height='sm',
                        action=MessageAction(label='News National', text='News National'),
                    ),
                    ButtonComponent(
                        style='primary',
                        height='sm',
                        action=MessageAction(label='News Thai', text='News Thai'),
                    ),
                    ButtonComponent(
                        style='primary',
                        height='sm',
                        action=MessageAction(label='NewsBBC', text='NewsBBC'),
                    ),

                ]
            ),
        )
        message = FlexSendMessage(alt_text="hello", contents=bubble)
        line_bot_api.reply_message(
            event.reply_token,
            message
        )
    if event.message.text[:5] == 'News ':
        splitWord = event.message.text.split(" ")
        inWordChoice = splitWord[1]
        if inWordChoice[:7] == 'England':
            apiNewThai = ('https://scrape-football-news-thai.herokuapp.com/listcategory?category=england-news')
        elif inWordChoice[:8] == 'National':
            apiNewThai = ('https://scrape-football-news-thai.herokuapp.com/listcategory?category=national-news')
        elif inWordChoice[:4] == 'Thai':
            apiNewThai = ('https://scrape-football-news-thai.herokuapp.com/listcategory?category=thai-news')
        else:
            print('Error')
        allDataNewsThais = requests.get(apiNewThai).json()
        carousel_container = CarouselContainer()
        for allDataNewsThai in allDataNewsThais[0:5]:
            categoryNewsThai = allDataNewsThai['category']
            dayTimeNewsThai = allDataNewsThai['day']
            descriptionNewsThai = allDataNewsThai['description']
            headerNewsThai = allDataNewsThai['header']
            linkWebNewsThai = allDataNewsThai['link']
            minuesTimesNewsThai = allDataNewsThai['time']
            photoNewThai = allDataNewsThai['photo']
            # เข้าไปเปลี่ยนเป็นบรรทัดเดียวได้ทีได้ที่ https://codebeautify.org/jsonviewer/cb7f415d
            newsThai = """{"type":"bubble","styles":{"header":{"backgroundColor":"#228B22"}},"header":{"type":"box","layout":"vertical","contents":[{"type":"text","wrap":true,"text":"วันที่:%s เวลา:%s","color":"#FFFFFF","size":"sm"},{"type":"filler"},{"type":"text","wrap":true,"text":"category: %s","color":"#FFFFFF","size":"lg"}]},"hero":{"type":"image","url":"%s","size":"full","aspectRatio":"20:13","aspectMode":"cover","action":{"type":"uri","uri":"%s"}},"body":{"type":"box","layout":"horizontal","spacing":"sm","flex":4,"contents":[{"type":"box","layout":"vertical","spacing":"xl","contents":[{"type":"text","wrap":false,"text":"%s","size":"lg"},{"type":"text","wrap":true,"text":"%s","size":"md"}]}]},"footer":{"type":"box","layout":"vertical","spacing":"sm","contents":[{"type":"button","style":"primary","action":{"type":"uri","label":"see more","uri":"%s"}}]}}
            """%(dayTimeNewsThai,minuesTimesNewsThai,categoryNewsThai,photoNewThai,linkWebNewsThai,headerNewsThai,descriptionNewsThai,linkWebNewsThai)
            newsThai = json.loads(newsThai)
            carousel_container.contents.append(newsThai)
        seeMorePageNewThai = '''{"type":"bubble","body":{"type":"box","layout":"vertical","spacing":"sm","contents":[{"type":"button","flex":1,"gravity":"center","action":{"type":"uri","label":"See more","uri":"https://www.sanook.com/sport"}}]}}'''
        seeMorePageNewThai = json.loads(seeMorePageNewThai)
        carousel_container.contents.append(seeMorePageNewThai)
        line_bot_api.reply_message(event.reply_token, FlexSendMessage(alt_text='Fixtures', contents=carousel_container))
        # (--------------------------------------------------News eng-------------------------------------------------)
    apiNewEng = ('https://scrape-news-football-eng.herokuapp.com/')
    allDataNewsEngs = requests.get(apiNewEng).json()
    carousel_container = CarouselContainer()       
    if event.message.text[:7] == 'NewsBBC':
        for allDataNewsEng in allDataNewsEngs[0:5]:
            categoryNewsEng = allDataNewsEng['category']
            dayTimeNewsEng = allDataNewsEng['dayTimeNews']
            descriptionNewsEng = allDataNewsEng['description']
            headerNewsEng = allDataNewsEng['header']
            linkWebNewsEng = allDataNewsEng['linkWeb']
            minuesTimesNewsEng = allDataNewsEng['minuesNewTimes']
            photoNewEng = allDataNewsEng['photo']
            # print(allDataNewsEng)
            # เข้าไปเปลี่ยนเป็นบรรทัดเดียวได้ทีได้ที่ https://codebeautify.org/jsonviewer/cb7f415d
            newsEng = """{"type":"bubble","styles":{"header":{"backgroundColor":"#228B22"}},"header":{"type":"box","layout":"vertical","contents":[{"type":"text","wrap":true,"text":"Day:%s Time:%s","weight":"bold","color":"#FFFFFF","size":"sm"},{"type":"filler"},{"type":"text","wrap":true,"text":"%s","weight":"bold","color":"#FFFFFF","size":"xl"}]},"hero":{"type":"image","url":"%s","size":"full","aspectRatio":"20:13","aspectMode":"cover","action":{"type":"uri","uri":"http://linecorp.com/"}},"body":{"type":"box","layout":"horizontal","spacing":"sm","flex":4,"contents":[{"type":"box","layout":"vertical","margin":"lg","spacing":"xl","contents":[{"type":"text","wrap":false,"text":"%s","size":"lg"},{"type":"filler"},{"type":"text","wrap":true,"text":"%s","size":"md"}]}]},"footer":{"type":"box","layout":"vertical","spacing":"sm","contents":[{"type":"button","style":"primary","action":{"type":"uri","label":"See more","uri":"%s"}}]}}"""%(dayTimeNewsEng,minuesTimesNewsEng,categoryNewsEng,photoNewEng,headerNewsEng,descriptionNewsEng,linkWebNewsEng)
            newsEng = json.loads(newsEng)
            carousel_container.contents.append(newsEng)
        seeMorePageNewEng = '''{"type":"bubble","body":{"type":"box","layout":"vertical","spacing":"sm","contents":[{"type":"button","flex":1,"gravity":"center","action":{"type":"uri","label":"See more","uri":"https://linecorp.com"}}]}}'''
        seeMorePageNewEng = json.loads(seeMorePageNewEng)
        carousel_container.contents.append(seeMorePageNewEng)
        line_bot_api.reply_message(event.reply_token, FlexSendMessage(alt_text='Fixtures', contents=carousel_container))
    # else:
    #     line_bot_api.reply_message(event.reply_token, TextSendMessage(text=event.message.text))

# run in heroku
if __name__ == '__main__':
    app.run(debug=True)
# run in ngrok
# if __name__ == '__main__':
#     app.run(debug=True, port=80)