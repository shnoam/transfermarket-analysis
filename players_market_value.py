import json

import requests as requests
from selenium.webdriver.common.alert import Alert
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import Select
import time
import random
proxy_lst = ["138.68.60.8:3128",'54.66.104.168:80', '80.48.119.28:8080', '157.100.26.69:80',
            '198.59.191.234:8080', '198.49.68.80:80', '169.57.1.85:8123','219.78.228.211:80' ,
            '88.215.9.208:80', '130.41.55.190:8080', '88.210.37.28:80', '128.199.202.122:8080',
            '2.179.154.157:808', '165.154.226.12:80', '200.103.102.18:80']
user_agents = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Safari/605.1.15',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 13_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Safari/605.1.15'
]
def find_player_id(url):
    # Split the URL by '/'
    url_parts = url.split('/')

    # The player ID is the last part of the URL
    player_id = url_parts[-1]
    return player_id
def extract_transfer_history():
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight / 2);")
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'transfer-history')]"))
    )
    transfer_history = []
    # Wait for each transfer element individually
    transfer_elements = WebDriverWait(driver, 15).until(
        EC.presence_of_all_elements_located(
            (By.XPATH, "//tm-transfer-history/div/div[@class='grid tm-player-transfer-history-grid']"))
    )
    #transfer_elements = driver.find_elements_by_xpath("//tm-transfer-history/div/div[@class='grid tm-player-transfer-history-grid']")

    for transfer_element in transfer_elements:
        transfer_details = {
            "season": transfer_element.find_element_by_xpath('./div[contains(@class,"season")]').text,
            "from_club": transfer_element.find_element_by_xpath('./div[contains(@class,"old-club")]/a[2]').text,
            "to_club": transfer_element.find_element_by_xpath('./div[contains(@class,"new-club")]/a[2]').text,
            "market_value": transfer_element.find_element_by_xpath('./div[contains(@class,"market-value")]').text,
            "transfer_fee": transfer_element.find_element_by_xpath('./div[contains(@class,"fee")]').text
        }
        transfer_history.append(transfer_details)

    return transfer_history
# Set up ChromeOptions to use a specific user agent
options = Options()  # Initialize an instance of the Options class
#options.headless = True  # True -> Headless mode activated
options.add_argument('window-size=1920x1080')  # Set a big window size, so all the data will be displayed

options.add_argument(f'user-agent={random.choice(user_agents)}')
#options.add_argument(f"--proxy-server=%s" % {random.choice(proxy_lst)})

#options.add_argument(f"--proxy-server=http://{random.choice(proxy_lst)}")
options.add_argument("--disable-notifications")

# Set up WebDriver with the specified options
path = 'C:/Users/User/Downloads/chromedriver-win64/chromedriver.exe'
driver = webdriver.Chrome(path, chrome_options=options)

website = 'https://www.transfermarkt.com/spieler-statistik/wertvollstespieler/marktwertetop'
driver.get(website)
driver.maximize_window()

# Check if the popup window is present
try:
    iframe = driver.find_element_by_xpath("//*[@id='sp_message_iframe_953358']")
    driver.switch_to.frame(iframe)
    button = driver.find_element_by_xpath("//button[contains(@title, 'Accept')]")
    button.click()
    driver.switch_to.default_content()

except NoSuchElementException:
    pass

pagination =  WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.XPATH, '//ul[@class="tm-pagination"]'))
)
next_page = pagination.find_element_by_xpath('./li[contains(@class,"next-page")]')
players_data_global = []
additional_data_by_player = []

i=0
while next_page:
    time.sleep(5)
    try:
        iframe = driver.find_element_by_xpath("//*[@id='sp_message_iframe_953358']")
        driver.switch_to.frame(iframe)
        button = driver.find_element_by_xpath("//button[contains(@title, 'Accept')]")
        button.click()
        driver.switch_to.default_content()

    except NoSuchElementException:
        pass

    players_links = []
    players_data_curr_page = []  # List to store player data from current iteration
    players_table = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.XPATH,"//table[@class='items']"))
    )
       # driver.find_element_by_xpath("//table[@class='items']")
    all_players_in_page = WebDriverWait(players_table, 10).until(
    EC.presence_of_all_elements_located((By.XPATH, "./tbody/tr"))
    )
    WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located(
            (By.XPATH, '//table[@class="items"]/tbody/tr//td[2]/table/tbody/tr[1]/td[2]/a'))
    )

    for player in all_players_in_page:
        try:
            player_link = player.find_element_by_xpath('./td[2]/table/tbody/tr[1]/td[2]/a').get_attribute("href")
            player_name = player.find_element_by_xpath('./td[2]/table/tbody/tr[1]/td[2]/a').text
            current_value = player.find_element_by_xpath('./td[contains(@class,"rechts")]/a').text

            players_links.append(player_link)  # Store player link

            current_player_data = {
                'Name': player_name,
                'Current Value': current_value
            }
            players_data_curr_page.append(current_player_data)
        except Exception as e:
            print(f"Error occurred while extracting  data: {e}")
            pass
    # Loop through player links

    for idx,player in enumerate(all_players_in_page):
        driver.get(players_links[idx])
        player_name = players_data_curr_page[idx].get('Name')
        time.sleep(2)
        try:
            iframe = driver.find_element_by_xpath("//*[@id='sp_message_iframe_953358']")
            driver.switch_to.frame(iframe)
            button = driver.find_element_by_xpath("//button[contains(@title, 'Accept')]")
            button.click()
            driver.switch_to.default_content()

        except NoSuchElementException:
            pass
        time.sleep(2)
        try:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight / 4);")
            main_position = driver.find_element_by_xpath("//dt[contains(text(), 'Main position')]/following-sibling::dd[1]").text
            # todo : maybe other position as well

            #todo: maybe highst as well
            #nationality = driver.find_element_by_xpath('//*[@id="main"]/main/header/div[5]/div/ul[1]/li[3]/span').text
            nationality = driver.find_element_by_xpath('//li[contains(text(), "Current international")]/span[1]/a').text
            date_of_birth = driver.find_element_by_xpath('//span[contains(text(), "Date of")]/following-sibling::span[1]/a').text
            city_of_birth = driver.find_element_by_xpath('//span[contains(text(), "Place of")]/following-sibling::span[1]/span').text
            country_of_birth = driver.find_element_by_xpath('//span[contains(text(), "Place of")]/following-sibling::span[1]/span/img').get_attribute('title')
            height = driver.find_element_by_xpath('//span[contains(text(), "Height")]/following-sibling::span[1]').text
            # todo: maybe other nationality
            foot = driver.find_element_by_xpath('//span[contains(text(), "Foot")]/following-sibling::span[1]').text
            current_club = driver.find_element_by_xpath('//span[contains(text(), "club")]/following-sibling::span[1]/a[2]').text
            contract_expires = driver.find_element_by_xpath('//span[contains(text(), "expires")]/following-sibling::span[1]').text
            outfitter = driver.find_element_by_xpath('//span[contains(text(), "Outfitter")]/following-sibling::span[1]').text
            players_data_curr_page[idx].update({
                'Main Position': main_position,
                'Nationality': nationality,
                'Date of Birth': date_of_birth,
                'City of Birth': city_of_birth,
                'Country of Birth': country_of_birth,
                'Height': height,
                'Current Club': current_club,
                "Contract Expires": contract_expires,
                'Foot': foot,
                'Outfitter': outfitter
            })
        except:
            print(f"{player_name} has missing values or data didnt loaded")
            pass
        try:
            transfers_data = extract_transfer_history() #returns a dict
            player_id = find_player_id(players_links[idx])
            driver.get(f'https://www.transfermarkt.com/ceapi/marketValueDevelopment/graph/{player_id}')
            mv_development = json.loads(driver.find_element_by_xpath('//html/body/pre').text)
            print(transfers_data)
            additional_data_by_player.append({
                player_name:{
                    "Transfers": transfers_data,
                    "Market Value development": mv_development
                }
            })
        except:
            print(f"{player_name} transfer data or mv development failed")
            pass
        


        print(f"{player_name} data loaded successfully")
        i+=1
        if i == 2:
            break

    players_data_global.extend(players_data_curr_page)
    break
driver.quit()
df_players = pd.DataFrame(players_data_global)
df_players.to_csv('df_players.csv', index=False,encoding='utf-8-sig')
with open("transfers.json", "w") as json_file:
    json.dump(additional_data_by_player, json_file)
