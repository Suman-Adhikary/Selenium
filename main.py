import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time

chrome_option = Options()
chrome_option.add_experimental_option("detach", True)
driver_service = Service(executable_path=r"C:\Users\suman\Documents\chromedriver.exe")
driver = webdriver.Chrome(options=chrome_option, service=driver_service)

header = {
    'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36',
    'Accept-Language' : 'en-US,en;q=0.9'
}

response = requests.get('https://www.zillow.com/homes/for_rent/?searchQueryState=%7B%22pagination%22%3A%7B%7D%2C%22mapBounds%22%3A%7B%22west%22%3A-123.44681776953125%2C%22east%22%3A-121.84006728125%2C%22south%22%3A37.127712863228716%2C%22north%22%3A38.02669258235875%7D%2C%22isMapVisible%22%3Atrue%2C%22filterState%22%3A%7B%22price%22%3A%7B%22max%22%3A872627%7D%2C%22beds%22%3A%7B%22min%22%3A1%7D%2C%22fore%22%3A%7B%22value%22%3Afalse%7D%2C%22mp%22%3A%7B%22max%22%3A3000%7D%2C%22auc%22%3A%7B%22value%22%3Afalse%7D%2C%22nc%22%3A%7B%22value%22%3Afalse%7D%2C%22fr%22%3A%7B%22value%22%3Atrue%7D%2C%22fsbo%22%3A%7B%22value%22%3Afalse%7D%2C%22cmsn%22%3A%7B%22value%22%3Afalse%7D%2C%22fsba%22%3A%7B%22value%22%3Afalse%7D%7D%2C%22isListVisible%22%3Atrue%7D', headers=header)
As_text = response.text
soup = BeautifulSoup(As_text, 'html.parser')
zillow = 'https://www.zillow.com/'

all_link_element = soup.find_all(name='div', class_='StyledPropertyCardDataWrapper-c11n-8-73-8__sc-1omp4c3-0 gXNuqr property-card-data')
all_links = []
all_addresses = []
for link in all_link_element:
    links = link.find('a')
    all_links.append(zillow+links.get('href'))
for link in all_link_element:
    links = link.find('address')
    all_addresses.append(links.getText().split('|')[-1])
all_price_element = soup.find_all(name='div', class_='StyledPropertyCardDataArea-c11n-8-73-8__sc-yipmu-0 hRqIYX')
all_prices = [price.getText().split('+')[0] for price in all_price_element]

for n in range(len(all_links)):
    # Substitute your own Google Form URL here 👇
    driver.get('https://docs.google.com/forms/d/e/1FAIpQLScmpkN07sZicUQ7nG7l5JUTkOCbxemL0KTlSRN-xZ-elpzn8w/viewform?usp=sf_link')

    time.sleep(2)
    address = driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div[1]/input')
    price = driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/input')
    link = driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div/div[1]/input')
    submit_button = driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div[1]/div/span')

    address.send_keys(all_addresses[n])
    price.send_keys(all_prices[n])
    link.send_keys(all_links[n])
    submit_button.click()