from bs4 import BeautifulSoup
import requests
from datetime import date
import discord
from discord.ext import commands
from discord import app_commands
"""
class Client(discord.Client):
    async def on_ready(self):
        print(f"Logged on as{self.user}")

    async def on_message(self, message):
        if message.content[0:6] == '/score':
            out = get_score(message.content[6:].strip(" "))
            await message.channel.send(f'{out}')"""

bot = commands.Bot(command_prefix="!", intents = discord.Intents.all())


teams = {
'hawks':'ATL',
'celtics' :'BOS',
'nets' : 'BKN',
'hornets' : 'CHA',
'bulls' : 'CHI',
'cavaliers' : 'CLE',
'mavericks' :'DAL',
'nuggets' : 'DEN',
'pistons': 'DET',
'warriors' :'GSW',
'rockets' : 'HOU',
'pacers' :'IND',
'clippers' : 'LAC',
'lakers ':'LAL',
'grizzlies' :'MEM',
'heat' : 'MIA',
'bucks ':'MIL',
'timberwolves' : 'MIN',
'pelicans': 'NO',
'knicks' : 'NYK',
'thunder' : 'OKC',
'magic' :'ORL',
'76ers' : 'PHI',
'suns' : 'PHO',
'blazers' : 'POR',
'kings' : 'SAC',
'spurs' : 'SA',
'raptors' : 'TOR',
'jazz' : 'UTA',
'wizards' : 'WAS'
}

def get_score(query):
    today = date.today().strftime("%Y%m%d")




    page = requests.get('https://www.cbssports.com/nba/scoreboard/')

    soup = BeautifulSoup(page.text, "html.parser")

    tp = soup.findAll("a", {"class":"team-name-link"})

    totals = soup.findAll("td", {"class":"total"})

    teamsplaying = [x.text.lower() for x in tp]




    if query in teamsplaying:
        for i in range(len(teamsplaying)):
            if teamsplaying[i]== query:
                if i%2 ==0:

                    output_teams = f'{teamsplaying[i].upper()} vs {teamsplaying[i+1].upper()}'
                    page2 = requests.get(f'https://www.cbssports.com/nba/gametracker/live/NBA_{today}_{teams[teamsplaying[i]]}@{teams[teamsplaying[i+1]]}/')
                    soup2 = BeautifulSoup(page2.text, "html.parser")
                
                
                    totals = soup2.findAll("div", {"class":"score-text"})
                    scores = [x.text for x in totals]

                    t = soup2.findAll("div", {"class":"time"})
                    time = [x.text for x in t]
                
                    quarter = soup2.findAll("div", {"class":"quarter"})
                    if quarter[0].text != 'End':
                        output_score = f'{time[0]} {quarter[0].text} {scores[0]} - {scores[1]}'
                    elif time[0] == '2nd':
                            output_score = f"HALFTIME: {scores[0]} - {scores[1]}"
                    else:
                        output_score = f"FINAL: {scores[0]} - {scores[1]}"

                else:
                    output_teams = f'{teamsplaying[i-1].upper()} vs {teamsplaying[i].upper()}'
                    page2 = requests.get(f'https://www.cbssports.com/nba/gametracker/live/NBA_{today}_{teams[teamsplaying[i-1]]}@{teams[teamsplaying[i]]}/')
                    soup2 = BeautifulSoup(page2.text, "html.parser")
                
                    totals = soup2.findAll("div", {"class":"score-text"})
                    scores = [x.text for x in totals]

                    t = soup2.findAll("div", {"class":"time"})
                    time = [x.text for x in t]
                
                    quarter = soup2.findAll("div", {"class":"quarter"})
                    if quarter[0].text != 'End':
                        output_score = f'{time[0]} {quarter[0].text} {scores[0]} - {scores[1]}'
                    elif time[0] == '2nd':
                            output_score = f"HALFTIME: {scores[0]} - {scores[1]}"
                    elif time[0] == '4th':
                        output_score = f"FINAL: {scores[0]} - {scores[1]}"
                    else:
                        output_score = f"End of {time[0]}: {scores[0]} - {scores[1]}"
    return f'{output_teams}\n{output_score}'




@bot.command(name="getscore", description="Get the score and time of a Game")
async def getscore(ctx: commands.Context, query: str):
    score = get_score(query)
    await ctx.send(f"`{score}`")

@bot.command(name="hello")
async def hello(ctx: commands.Context):
    await ctx.send("helloo")

bot.run('')