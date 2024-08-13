import json
import random
import time
#from extracting_player_stats import *
import pandas as pd
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

FAILED_TRANSFER_DATA = []
LAST_PAGE = 20
PROXY_LST = ["138.68.60.8:3128", '54.66.104.168:80', '80.48.119.28:8080', '157.100.26.69:80',
             '198.59.191.234:8080', '198.49.68.80:80', '169.57.1.85:8123', '219.78.228.211:80',
             '88.215.9.208:80', '130.41.55.190:8080', '88.210.37.28:80', '128.199.202.122:8080',
             '2.179.154.157:808', '165.154.226.12:80', '200.103.102.18:80']
USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Safari/605.1.15',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 13_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Safari/605.1.15'
]


def find_player_id(url):
    # Split the URL by '/'
    url_parts = url.split('/')

    # The player ID is the last part of the URL
    player_id = url_parts[-1]
    return player_id


def extract_transfer_history(driver,player_name):
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight / 2);")
    WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'transfer-history')]"))
    )
    transfer_history = []
    # Wait for each transfer element individually
    transfer_elements = WebDriverWait(driver, 15).until(
        EC.presence_of_all_elements_located(
            (By.XPATH, "//tm-transfer-history/div/div[@class='grid tm-player-transfer-history-grid']"))
    )

    for transfer_element in transfer_elements:
        transfer_details = {
            "Player": player_name,
            "Season": transfer_element.find_element_by_xpath('./div[contains(@class,"season")]').text,
            "From Club": transfer_element.find_element_by_xpath('./div[contains(@class,"old-club")]/a[2]').text,
            "To Club": transfer_element.find_element_by_xpath('./div[contains(@class,"new-club")]/a[2]').text,
            "Market Value": transfer_element.find_element_by_xpath('./div[contains(@class,"market-value")]').text,
            "Transfer Fee": transfer_element.find_element_by_xpath('./div[contains(@class,"fee")]').text
        }
        transfer_history.append(transfer_details)

    return transfer_history

def handle_popup_window(driver):
    try:
        iframe = driver.find_element_by_xpath("//*[@id='sp_message_iframe_953358']")
        driver.switch_to.frame(iframe)
        button = driver.find_element_by_xpath("//button[contains(@title, 'Accept')]")
        button.click()
        driver.switch_to.default_content()

    except NoSuchElementException:
        pass
    return

def extract_data(driver, xpath, feature_name, player_name=None):
    try:
        value = driver.find_element_by_xpath(xpath).text
        return value
    except Exception as e:
        if player_name and feature_name != "Outfitter":
            print(f"Error while extracting {feature_name} data for player {player_name}: {e}")
        return None

def scrape_batch(driver, start_page, end_page):
    website = f"https://www.transfermarkt.com/spieler-statistik/wertvollstespieler/marktwertetop?ajax=yw1&page={start_page}"
    driver.get(website)
    driver.maximize_window()
    handle_popup_window(driver)

    players_data_global = []
    all_transfers_data = []
    mv_data_by_player = []
    for page in range(start_page, end_page + 1):
        time.sleep(3)
        handle_popup_window(driver)
        players_links = []
        players_data_curr_page = []  # list to store player data from current iteration
        players_table = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//table[@class='items']"))
        )

        all_players_in_page = WebDriverWait(players_table, 10).until(
            EC.presence_of_all_elements_located((By.XPATH, "./tbody/tr"))
        )


        for player in all_players_in_page:
            try:
                player_link = player.find_element_by_xpath('./td[2]/table/tbody/tr[1]/td[2]/a').get_attribute("href")
                player_name = player.find_element_by_xpath('./td[2]/table/tbody/tr[1]/td[2]/a').text
                current_value = player.find_element_by_xpath('./td[contains(@class,"rechts")]/a').text

                players_links.append(player_link)  # store player link

                current_player_data = {
                    'player': player_name,
                    'current_value': current_value
                }
                players_data_curr_page.append(current_player_data)
            except Exception as e:
                print(f"Error occurred while extracting data: {e}")
                pass
        # loop through player links
        for idx, player_link in enumerate(players_links):
            driver.get(player_link)
            player_name = players_data_curr_page[idx].get('Name')
            time.sleep(2)
            try:
                iframe = driver.find_element_by_xpath("//*[@id='sp_message_iframe_953358']")
                driver.switch_to.frame(iframe)
                button = driver.find_element_by_xpath("//button[contains(@title, 'Accept')]")
                button.click()
                driver.switch_to.default_content()

            except NoSuchElementException as e:
                pass
            time.sleep(2)

            driver.execute_script("window.scrollTo(0, document.body.scrollHeight / 4);")
            try:
                if driver.find_element_by_xpath('//*[@id="main"]/main/header/div[1]/a/span[contains(text(),"loan")]'):
                    on_loan = True
            except:
                on_loan = None
                on_loan_from = '-'
                pass

            main_position_xpath = "//dt[contains(text(), 'Main position')]/following-sibling::dd[1]"
            nationality_xpath = '//li[contains(text(), "Current international")]/span[1]/a | //li[contains(text(), "National")]/span[1]/a | //li[contains(text(), "International")]/span[1]/a'
            date_of_birth_xpath = '//span[contains(text(), "Date of")]/following-sibling::span[1]/a'
            city_of_birth_xpath = '//span[contains(text(), "Place of")]/following-sibling::span[1]/span'
            height_xpath = '//span[contains(text(), "Height")]/following-sibling::span[1]'
            foot_xpath = '//span[contains(text(), "Foot")]/following-sibling::span[1]'
            current_club_xpath = '//span[contains(text(), "club")]/following-sibling::span[1]/a[2]'
            contract_expires_xpath = '//span[contains(text(), "expires")]/following-sibling::span[1]'
            on_loan_from_xpath ='//span[contains(text(), "loan from")]/following-sibling::span[1]/a'
            contract_there_expires_xpath ='//span[contains(text(), "there expires")]/following-sibling::span[1]'
            number_xpath = "//span[contains(@class, 'shirt-number')]"
            outfitter_xpath = '//span[contains(text(), "Outfitter")]/following-sibling::span[1]'

            # Usage example:
            main_position = extract_data(driver, main_position_xpath, "Main_Position", player_name)
            nationality = extract_data(driver, nationality_xpath, "Nationality", player_name)
            date_of_birth = extract_data(driver, date_of_birth_xpath, "Date_Of_Birth", player_name)
            city_of_birth = extract_data(driver, city_of_birth_xpath, "City_Of_Birth", player_name)
            height = extract_data(driver, height_xpath, "Height", player_name)
            foot = extract_data(driver, foot_xpath, "Foot", player_name)
            current_club = extract_data(driver, current_club_xpath, "Current_Club", player_name)
            contract_expires = extract_data(driver, contract_expires_xpath, "Contract_Expires", player_name)
            number = extract_data(driver, number_xpath, "Number", player_name)
            outfitter = extract_data(driver, outfitter_xpath, "Outfitter", player_name)
            if on_loan != None:
                on_loan_from = extract_data(driver, on_loan_from_xpath, "on_loan_from", player_name)
                contract_there_expires = extract_data(driver, contract_there_expires_xpath, "Contract_There_Expires", player_name)

            try:
                country_of_birth = driver.find_element_by_xpath(
                    '//span[contains(text(), "Place of")]/following-sibling::span[1]/span/img').get_attribute(
                    'title')
            except Exception as e:
                print(f"Error while extracting country_of_birth for player {player_name}: {e}")
                country_of_birth = None
            try:
                other_positions_elements = driver.find_elements_by_xpath(
                            "//dt[contains(text(), 'Other position')]/following-sibling::dd")
                other_positions = [element.text for element in other_positions_elements]
            except Exception as e:
                print(f"Error while extracting other_positions for player {player_name}: {e}")
                other_positions = None

            players_data_curr_page[idx].update({
                'main_position': main_position,
                "other_positions": other_positions,
                'nationality': nationality,
                'date_of_birth': date_of_birth,
                'city_of_birth': city_of_birth,
                'country_of_birth': country_of_birth,
                'height': height,
                'current_club': current_club,
                "contract_expires": contract_expires,
                "on_loan_from": on_loan_from if on_loan else '-',
                "contract_there_expires": contract_there_expires if on_loan else '-',
                "number": number,
                'foot': foot,
                'outfitter': outfitter
            })
            try:
                player_transfers_data = extract_transfer_history(driver, player_name)  # returns a dict
                for transfer in player_transfers_data:
                    all_transfers_data.append(transfer)
            except Exception as e:
                print(f"{player_name} transfer data error:{e}")
                FAILED_TRANSFER_DATA.append(player_name)
                pass
            # try:
            #     career_data = extract_career_stats(driver)
            # except Exception as e:
            #     print(e)
            #     print(f"{player_name} stats failed")

            try:
                player_id = find_player_id(player_link)
                driver.get(f'https://www.transfermarkt.com/ceapi/marketValueDevelopment/graph/{player_id}')
                mv_development = json.loads(driver.find_element_by_xpath('//html/body/pre').text)
                mv_data_by_player.append({
                    player_name: mv_development
                })
            except Exception as e:
                print(f"{player_name} mv development failed")
                print(e)
                pass
        players_data_global.extend(players_data_curr_page)
        print(f"page {page} is finished")

        try:
            next_page_url = f"https://www.transfermarkt.com/spieler-statistik/wertvollstespieler/marktwertetop/mw/ajax/yw1/page/{page+1}"
            driver.get(next_page_url)

        except Exception as e: # last page
            print(e)
            print(f"page {page+1} url error")

    return players_data_global, all_transfers_data, mv_data_by_player

def main():
    # Define batch size
    batch_size = 4
    num_batches = 5
    total_pages = 20

    # Iterate over batches
    for batch_index in range(3,num_batches): #num_batches
        start_page = batch_index * batch_size + 1
        end_page = min((batch_index + 1) * batch_size, total_pages)

        print(f"Scraping batch {batch_index + 1}: pages {start_page}-{end_page}")
        options = Options()
        options.add_argument('window-size=1920x1080')  # Set a big window size, so all the data will be displayed
        options.add_argument(f'user-agent={random.choice(USER_AGENTS)}')  #USER_AGENTS[batch_index]
        options.add_argument("--disable-notifications")

        # Set up WebDriver with the specified options
        path = 'C:/Users/User/Downloads/chromedriver-win64/chromedriver.exe'
        driver = webdriver.Chrome(path, options=options)

        players_data, transfers_data, mv_data = scrape_batch(driver, start_page, end_page)
        driver.quit()
        # Save data to CSV and JSON
        df_players = pd.DataFrame(players_data)
        df_players.to_csv(f'df_players_batch_{batch_index + 1}.csv', index=False, encoding='utf-8-sig')

        with open(f"transfers_batch_{batch_index + 1}.json", "w") as json_file:
            json.dump(transfers_data, json_file)
        with open(f"mv_batch_{batch_index + 1}.json", "w") as json_file:
            json.dump(mv_data, json_file)
    try:
        print(FAILED_TRANSFER_DATA)
    except:
        pass

if __name__ == "__main__":
    main()
