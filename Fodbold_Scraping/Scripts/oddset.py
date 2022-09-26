import os
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
import time

# Dette program finder odds og hold givet den relevante bet365-side

driver =  webdriver.Firefox()

URL = "https://www.bet365.dk/#/AC/B1/C1/D8/E117979865/F3/I4/"
driver.get(URL)

time.sleep(5)

#########

hold = driver.find_element(By.CLASS_NAME, "sph-EventHeader_Label ").find_element(By.XPATH, 'span').text
print(hold)
#########

id_top = "gl-MarketGroupButton_Text"
results = driver.find_elements(By.CLASS_NAME, id_top)
parent = results[0].find_element(By.XPATH, '..')
neighbor_child = parent.find_element(By.XPATH, '../div[2]').find_element(By.XPATH, 'div')

relevant_children = neighbor_child.find_elements(By.XPATH, 'div')

cards_odds = [] 
for d in relevant_children[1:]:
    bot = d.find_elements(By.XPATH, 'div')
    #print(bot[0].text)
    cards_odds.append([bot[0].text, bot[1].find_element(By.XPATH, 'span').text])

print("oddsene er: ", cards_odds)     

# results = driver.find_elements_by_xpath('.//span[@class = "gl-MarketGroupButton_Text"]')
print(len(relevant_children))#.get_attribute('class'))




