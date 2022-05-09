import os
from tkinter import W
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
import time

driver =  webdriver.Firefox()

URL = "https://www.bet365.dk/#/AS/B1"
driver.get(URL)

time.sleep(4)

# Nu navigerer vi ind på den rigtige side
driver.find_elements(By.CLASS_NAME, "sm-UpComingFixturesMultipleParticipants ")[1].click()

time.sleep(2)

knapper = driver.find_elements(By.CLASS_NAME, "rcl-ParticipantFixtureDetails_LhsContainer ")

print(len(knapper))
