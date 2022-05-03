import numpy as np
import pandas as pd
import requests
from bs4 import BeautifulSoup

# Lad os prøve at se om vi kan finde ud af hvor mange gule kort de dansk
# fodboldhold får pr. kamp

URLbase = 'https://fbref.com/en/country/clubs/DEN/Denmark-Football-Clubs'
page1 = requests.get(URLbase)
soup = BeautifulSoup(page1.content, "html.parser")

table = soup.find(id = 'clubs').find('tbody')

teams_url = []
for entry in table.find_all('tr'):
    url = entry.find('a').get('href')
    url = url.split('history/')
    url = url[0] + url[1].split('-and')[0]
    teams_url.append(url)

URLbase2 = 'https://fbref.com'

for teams in teams_url:
    print(URLbase2 + teams)

def misc_stats(url):
    soup = BeautifulSoup(requests.get(url).content, "html.parser")
    table = soup.find(id = "all_stats_misc").find("table")
    rows = table.find('tbody').find_all('tr')
    # player_names = [r.find('data_stat' == 'player').text for r in rows]
    players_stats = [r.find_all('td') for r in rows]

    # matches = [r.find('data_stat' == 'minutes_90s')for r in players_stats]
    # yellow_cards = [r.find('data_stat' == 'cards_yellow').text for r in players_stats]
    return players_stats




# print(misc_stats(URLbase2 + teams_url[1])[0].find('data_stat' == 'player').text)
print(misc_stats(URLbase2 + teams_url[1]))








