from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import time
import csv

#Creating the web scraper
chrome_options = Options()
chrome_options.add_experimental_option("detach", True)

def lookup_instructor(instructor_name):

    #Formatting the website to match the professor
    chrome_options = Options()
    chrome_options.add_experimental_option("detach", True)
    browser = webdriver.Chrome(options=chrome_options)
    initial_url = "https://www.google.com/search?q="
    add_on = instructor_name.split()
    for term in add_on:
        initial_url += term + "+"
    url = initial_url + "cpp"

    #Going to the website
    browser.get(url)

    time.sleep(2)
    #Switching to tthe images path
    browser.find_element(By.XPATH,"/html/body/div[6]/div/div[2]/div/div/div/div/div/div/div[1]/div[1]/a/div/span").click()

    #Scraping the first image
    browser.find_element(By.XPATH,"/html/body/div[5]/div/div[2]/div/div/div/div/div/div/div[1]/div[1]/a/div")

lookup_instructor("Qichao Dong")