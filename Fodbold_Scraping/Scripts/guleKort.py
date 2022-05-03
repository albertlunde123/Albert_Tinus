import numpy as np
import pandas as pd
import requests
from bs4 import BeautifulSoup
import csv


# Lad os prøve at se om vi kan finde ud af hvor mange gule kort de dansk
# fodboldhold får pr. kamp

URLbase = 'https://fbref.com/en/country/clubs/DEN/Denmark-Football-Clubs'
page1 = requests.get(URLbase)
soup = BeautifulSoup(page1.content, "html.parser")


# Finder tabellen med klubberne
table = soup.find(id = 'clubs').find('tbody')


# Nu løber vi tabellen igennem og gemmer url'erne
teams_url = []
for entry in table.find_all('tr'):
    url = entry.find('a').get('href')
 # Det er de forkerte url'er... men vi kan lige formattere dem så de passer
    url = url.split('history/')
    url = url[0] + url[1].split('-and')[0]
    teams_url.append(url)

# Nu skal vi kigge på hver af de enkelte sider.
URLbase2 = 'https://fbref.com'

def misc_stats(url):

    # Vi hiver lige holdnavnet ud af URL'en

    team = url.split('/')[-1].split('-S')[0]

    soup = BeautifulSoup(requests.get(url).content, "html.parser")

    # misc-stats tabellen.
    table = soup.find(id = "all_stats_misc").find("table")

    # navne-rækkerne er 'tr' mønster
    name_rows = table.find('tbody').find_all('tr')
    player_names = [r.find('data_stat' == 'player').text for r in name_rows]

    # de resterende kolonner er 'td' mønster. Vi gemmer resten af rækkerne og
    # kolonnerne.

    players_stats = [r.find_all('td') for r in name_rows]

    # nu looper vi igennem rækkerne og vælger kolonne 3 og 4. De indeholder det
    # data vi er interesseret i. Nemlig antal minutter de har spillet samt
    # antal gule kort de har fået.

    matches = [r[3].text for r in players_stats] # minutter spillet delt med 90.
    yellow_cards = [r[4].text for r in players_stats] # antal kort i alt.
    return list(zip(player_names, matches, yellow_cards, [team]*len(player_names)))

# Nu skal vi til at gemme dataet.
def update():
    with open('spillere.csv', 'w', newline='') as spillere:
        wri = csv.writer(spillere, delimiter = ',')

        header = ['navn', '90s', 'gule kort', 'hold']
        wri.writerow(header)

        for team in teams_url:
            for row in misc_stats(URLbase2 + team):
                wri.writerow(row)

database = pd.read_csv('spillere.csv')
print(database)

    # print(misc_stats(URLbase2 + teams_url[1])[0].find('data_stat' == 'player').text)
# print(misc_stats(URLbase2 + teams_url[3]))








