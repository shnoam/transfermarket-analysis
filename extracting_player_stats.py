from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.support.ui import Select
# def extract_career_stats(driver):
#     try:
#         driver.find_element_by_xpath("//a[@class='content-link' and contains(text(), 'full stats')]").click()
#
#         # Click on the dropdown to open it
#         driver.find_element_by_class_name("chzn-container-single").click()
#
#         # Locate the option you want to select and click on it
#         option_to_select = driver.find_element_by_xpath(
#             "//div[@class='chzn-drop']/ul/li[contains(text(), 'Overall')]")
#         option_to_select.click()
#         # Locate and click on the "show" button
#         show_button = driver.find_element_by_xpath("//input[@type='submit' and @value='Show']")
#         show_button.click()
#         time.sleep(2)
#         driver.execute_script("window.scrollTo(0, document.body.scrollHeight / 4);")
#         # Find the table element
#         player_info = {}
#         table_element = driver.find_element_by_xpath("//*[@id='yw1']/table/tbody")
#
#         # Find all the table rows (tr elements) within the table
#         rows = table_element.find_elements_by_tag_name("tr")
#         career_stats = []
#         # Iterate over each row
#         for row in rows:
#             # Extract data from each cell in the row
#             # Find all td elements within the row
#             cells = row.find_elements_by_tag_name("td")
#             # Extract text from each cell starting from the second one
#             competition = cells[1].find_element_by_tag_name("a").text
#             appearences = cells[2].find_element_by_tag_name("a").text
#             goals = cells[3].text
#             assists = cells[4].text
#             yellow_cards = cells[5].text
#             second_yellow_cards = cells[6].text
#             red_cards = cells[7].text
#             career_stats.append({
#                 "Competition": competition,
#                 "Appearances": appearences,
#                 "Goals": goals,
#                 "Assists": assists,
#                 "Yellow Cards": yellow_cards,
#                 "Second Yellow Cards": second_yellow_cards,
#                 "Red Cards": red_cards
#             })
#         # Find all rows under the h2 element with text 'Positions'
#         rows = driver.find_elements_by_xpath(
#             "//h2[contains(text(), 'Positions')]/following-sibling::table/tbody/tr")
#
#         # Initialize an empty list to store the extracted data
#         position_stats = []
#
#         # Iterate over each row
#         for row in rows:
#             # Find all td elements within the row
#             cells = row.find_elements_by_tag_name("td")
#
#             position = cells[0].find_element_by_tag_name("a").text
#             appearences = cells[1].find_element_by_tag_name("a").text
#             goals = cells[0].find_element_by_tag_name("a").text
#             assists = cells[1].find_element_by_tag_name("a").text
#             position_stats.append({
#                 "Position": position,
#                 "Appearances": appearences,
#                 "Goals": goals,
#                 "Assists": assists
#             })
#         # Find all rows under the h2 element with text 'Stats by club'
#         rows = driver.find_elements_by_xpath(
#             "//h2[contains(text(), 'Stats by club')]/following-sibling::table/tbody/tr")
#
#         # Initialize an empty list to store the extracted data
#         stats_by_club = []
#
#         # Iterate over each row
#         for row in rows:
#             # Find all td elements within the row
#             cells = row.find_elements_by_tag_name("td")
#
#             club = cells[0].find_element_by_tag_name("a").text
#             appearances = cells[1].find_element_by_tag_name("a").text
#             goals = cells[2].text
#             assists = cells[3].text
#
#             # Append a dictionary with extracted data to the list
#             stats_by_club.append({
#                 "Club": club,
#                 "Appearances": appearances,
#                 "Goals": goals,
#                 "Assists": assists
#             })
#         # Find all rows under the h2 element with text 'NATIONAL TEAM CAREER'
#         row= driver.find_element_by_xpath(
#             "//h2[contains(text(), 'National team')]/following-sibling::table/tbody/tr[2]")
#
#         # Initialize an empty list to store the extracted data
#         national_team_career = []
#
#         # Iterate over each row
#
#         # Find all td elements within the row
#         cells = row.find_elements_by_tag_name("td")
#
#         team = cells[3].find_element_by_tag_name("a").text
#         debut = cells[4].find_element_by_tag_name("a").text
#         appearances = cells[5].find_element_by_tag_name("a").text
#         goals = cells[6].find_element_by_tag_name("a").text
#
#         # Append a dictionary with extracted data to the list
#         national_team_career.append({
#             "Team": team,
#             "Debut": debut,
#             "Appearances": appearances,
#             "Goals": goals,
#         })
#         player_info.update({
#             "Career Stats": career_stats,
#             "Positions Played":position_stats ,
#             "Stats by Club": stats_by_club,
#             "National Team":national_team_career
#         })
#
#     except:
#         print(f"{player_name} stats failed")
#         pass
def extract_career_stats(driver):
    player_info = {}
    try:
        # Clicking on 'Full Stats' link
        full_stats_link = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//a[@class='content-link' and contains(text(), 'full stats')]")))

        # Click on the 'Full Stats' link
        full_stats_link.click()

        # Waiting for the dropdown to load
        dropdown_element =Select(driver.find_element_by_xpath("//select[@class = 'chzn-select chzn-done']"))
        # Wait for the option with value 'ges' to be visible and selectable
        # WebDriverWait(driver, 10).until(
        #     EC.visibility_of_element_located((By.XPATH, "//option[@value='ges']"))
        # )
        # Clicking on the dropdown to open it
        element = driver.find_element_by_xpath("//option[@value='ges']")
        driver.execute_script("arguments[0].scrollIntoView(true);", element)

        dropdown_element.select_by_value('ges')

        # Clicking on 'Show' button
        show_button = driver.find_element_by_xpath("//input[@type='submit' and @value='Show']")
        show_button.click()

        # Waiting for the table to load
        table_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//*[@id='yw1']/table/tbody")))

        # Extracting career stats
        career_stats = extract_table_data(table_element)

        # Extracting position stats
        position_stats = extract_position_stats(driver)

        # Extracting stats by club
        stats_by_club = extract_stats_by_club(driver)

        # Extracting national team career
        national_team_career = extract_national_team_career(driver)

        # Updating player_info dictionary
        player_info.update({
            "Career Stats": career_stats,
            "Positions Played": position_stats,
            "Stats by Club": stats_by_club,
            "National Team": national_team_career
        })

    except Exception as e:
        print(f"Failed to extract career stats: {e}")

    return player_info


def extract_table_data(driver):
    # Initialize an empty list to store the extracted data
    table_element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//*[@id='yw1']/table/tbody")))
    data = []

    # Find all the table rows (tr elements) within the table
    rows = table_element.find_elements_by_tag_name("tr")

    # Iterate over each row
    for row in rows:
        # Find all td elements within the row
        cells = row.find_elements_by_tag_name("td")

        # Extract text from each cell starting from the second one
        data.append({
            "Competition": cells[1].find_element_by_tag_name("a").text,
            "Appearances": cells[2].find_element_by_tag_name("a").text,
            "Goals": cells[3].text,
            "Assists": cells[4].text
            # "Yellow Cards": cells[5].text,
            # "Second Yellow Cards": cells[6].text,
            # "Red Cards": cells[7].text
        })

    return data


def extract_position_stats(driver):
    # Find all rows under the h2 element with text 'Positions'
    rows = driver.find_elements_by_xpath("//h2[contains(text(), 'Positions')]/following-sibling::table/tbody/tr")

    # Initialize an empty list to store the extracted data
    data = []

    # Iterate over each row
    for row in rows:
        # Find all td elements within the row
        cells = row.find_elements_by_tag_name("td")

        # Extracting data from cells
        data.append({
            "Position": cells[0].find_element_by_tag_name("a").text,
            "Appearances": cells[1].find_element_by_tag_name("a").text,
            "Goals": cells[2].text,
            "Assists": cells[3].text
        })

    return data


def extract_stats_by_club(driver):
    try:
        # Find all rows under the h2 element with text 'Stats by club'
        rows = driver.find_elements_by_xpath("//h2[contains(text(), 'Stats by club')]/following-sibling::table/tbody/tr")

        # Initialize an empty list to store the extracted data
        stats_by_club = []

        # Iterate over each row
        for row in rows:
            # Find all td elements within the row
            cells = row.find_elements_by_tag_name("td")

            # Extracting data from cells
            club = cells[0].find_element_by_tag_name("a").text
            appearances = cells[1].find_element_by_tag_name("a").text
            goals = cells[2].text
            assists = cells[3].text

            # Append extracted data to the list
            stats_by_club.append({
                "Club": club,
                "Appearances": appearances,
                "Goals": goals,
                "Assists": assists
            })
    except Exception as e:
        print(f"Failed to extract stats by club: {e}")
        stats_by_club = []

    return stats_by_club

def extract_national_team_career(driver):
    try:
        # Find all rows under the h2 element with text 'National team'
        rows = driver.find_elements_by_xpath("//h2[contains(text(), 'National team')]/following-sibling::table/tbody/tr")

        # Initialize an empty list to store the extracted data
        national_team_career = []

        # Iterate over each row
        for row in rows:
            # Find all td elements within the row
            cells = row.find_elements_by_tag_name("td")

            # Extracting data from cells
            team = cells[3].find_element_by_tag_name("a").text
            debut = cells[4].find_element_by_tag_name("a").text
            appearances = cells[5].find_element_by_tag_name("a").text
            goals = cells[6].find_element_by_tag_name("a").text

            # Append extracted data to the list
            national_team_career.append({
                "Team": team,
                "Debut": debut,
                "Appearances": appearances,
                "Goals": goals
            })
    except Exception as e:
        print(f"Failed to extract national team career: {e}")
        national_team_career = []

    return national_team_career
