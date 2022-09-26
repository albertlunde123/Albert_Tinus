import os
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
import time

driver =  webdriver.Firefox()

urlpage = "https://www.soccer24.com/"
driver.get(urlpage)

time.sleep(4)

driver.find_element(By.ID, "onetrust-accept-btn-handler").click()
# ids = "event__match event__match--scheduled event__match--twoLine"
ids = "g_1_IuTwo3v4"
# results =  driver.find_elements_by_xpath("//*[@class=" + ids +"]")
results = driver.find_element(By.ID, ids).click()
# results =  driver.find_elements_by_xpath("//*[@class=" + ids +"]")


time.sleep(10)
print(results)
time.sleep(10)
# Vi bruger følgende hjemmeside.

# baseUrl = "https://www.soccer24.com/denmark/superliga/"
# soup = BeautifulSoup(requests.get(baseUrl).content, "html.parser")

# Så skal vi søge siden igennem efter URL'er som opfylder at kampen er færdig.
# Det kan vi ikke umiddelbart gøre med bs4 på denne side. Der er en masse ting
# som ikke dukker i HTML'en. Vi skal nok bruge selenium til det.

# tabel = soup.find(id="g_1_UqY8kEVh")
# kampe = soup.findAll('title' == 'Click for match detail!')
# print(tabel.prettify())

#######

# Vi prøver nu at se om vi kan hive noget information ud af en af
# resultatsiderne.

# resultUrl = 'https://www.soccer24.com/match/bJxDlYpa/#/match-summary/match-summary'
# soup = BeautifulSoup(requests.get(resultUrl).content, "html.parser")

# print(soup.prettify())
